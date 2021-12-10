import celery
from celery import shared_task, Task
from django.apps import apps
from django_celery_results.models import TaskResult
from collections import defaultdict
from django.db import transaction
from django.conf import settings
import numpy as np
import prodigy
import time
import os
from tqdm import tqdm

from labeling.models import Modes
from collection.models import Product
from topics.models import ProductTopic, Topic, Label, TopicStatus, TopicSourceStatus

class TrainTaskBase(Task):
    def update_train(self, train_id):
        Train = apps.get_model('models', 'Train')
        self.train = Train.objects.get(pk=train_id)
        time.sleep(2)
        task = TaskResult.objects.get(task_id=self.request.id)
        self.train.task = task
        self.train.save()
    
    def generate_meta(self):
        meta = self.train.input_meta
        meta.update({ # add output dir, mode, and database
            'output_dir': os.path.join(settings.MODEL_DIR, self.train.model.path),
            self.train.model.mode.lower(): self.train.dataset.name # for mode flag --ner test_ner

        })
        return meta

@shared_task(bind=True, base=TrainTaskBase)
def train_prodigy(self, train_id):
    self.update_state(state='PROGRESS')
    self.update_train(train_id)

    self.train.train_meta = {} # reset train meta
    self.train.save()

    meta = self.generate_meta()
    baseline, scores = prodigy.recipes.train.train(**meta)

    self.update_state(state='SUCCESS', meta={'baseline': baseline, 'scores': scores})
    self.train.train_meta = {'baseline': baseline, 'scores': scores}
    self.train.save()

class PredictionTaskBase(Task):
    def update_prediction(self, prediction_id):
        Prediction = apps.get_model('models', 'Prediction')
        self.prediction = Prediction.objects.get(pk=prediction_id)
        time.sleep(2)
        task = TaskResult.objects.get(task_id=self.request.id)
        self.prediction.task = task
        self.prediction.save()
    
    def predict_ner(self, nlp, text, label=None):
        """Predict Named Entity Recognition"""
        doc = nlp(text)
        label_dict = defaultdict(list)
        
        for label in nlp.get_pipe('ner').labels:
            label_dict[label.lower()] = []
            
        for ent in doc.ents:
            token_name = ent.text.strip().lower()
            if token_name not in label_dict[ent.label_.lower()]:
                label_dict[ent.label_.lower()].append(token_name)

        return label_dict

    def predict_textcat(self, nlp, text, label):
        """Predict textcat (exclusive, not multilabel)"""
        doc = nlp(text)

        classes = np.array(list(doc.cats.keys()))
        preds = np.array(list(doc.cats.values()))
        output = classes[np.argmax(preds)]

        return {label: [output]}

    def predict_textcat_multilabel(self, nlp, text, label):
        """Predict textcat multilabel"""
        doc = nlp(text)

        classes = np.array(list(doc.cats.keys()))
        preds = np.array(list(doc.cats.values()))
        output = classes[preds > 0.5]

        return {label: [output]}

    PREDICT_FUNCTIONS = {
        Modes.NER: predict_ner,
        Modes.TEXTCAT: predict_textcat,
        Modes.TEXTCAT_MULTILABEL: predict_textcat_multilabel
    }

@shared_task(bind=True, base=PredictionTaskBase)
def prediction(self, prediction_id):
    self.update_state(state='PROGRESS')
    self.update_prediction(prediction_id)

    PredictionResult = apps.get_model('models', 'PredictionResult')
    
    products = self.prediction.get_collection().product_choice()
    nlp = self.prediction.model.load()

    # find the model's labels
    if self.prediction.model.mode == Modes.NER:
        entity_recognizer = nlp.get_pipe('ner')
        labels = entity_recognizer.labels
    elif self.prediction.model.mode == Modes.TEXTCAT or self.prediction.model.mode == Modes.TEXTCAT_MULTILABEL:
        if self.prediction.meta.get('label') is None:
            raise Exception('If the model is of mode TEXTCAT or TEXTCAT_MULTILABEL, it must contain the "label" metadata field.')
        
        labels = [self.prediction.meta.get('label')]

    with transaction.atomic(using='ml'):
        self.prediction.results.all().delete()

        for p in tqdm(products):
            if self.prediction.ignore_committed:
                topics_assigned = p.producttopic_set.filter(label__name__in=labels)
                if len(topics_assigned) != 0: # if we find that there are topics assigned to this product in the given labels:
                    continue # skip this product

            text = p.name + '\n' + p.description
            label_dict = self.PREDICT_FUNCTIONS[self.prediction.model.mode](self, nlp, text, label=self.prediction.meta.get('label'))
            for label, topics in label_dict.items():
                for t in topics:
                    prediction_result = PredictionResult(product_id=p.id, prediction=self.prediction, label=label, topic=t)
                    prediction_result.save()

@shared_task(bind=True)
def commit_predictions(self, prediction_id):
    self.update_state(state='PROGRESS')
    Prediction = apps.get_model('models', 'Prediction')
    PredictionResult = apps.get_model('models', 'PredictionResult')
    prediction = Prediction.objects.get(pk=prediction_id)

    task = TaskResult.objects.get(task_id=self.request.id)
    prediction.commit_task = task
    prediction.save()

    results = PredictionResult.objects.filter(prediction=prediction)

    status = TopicStatus.objects.get(slug='ml-generated')
    sources = TopicSourceStatus.to_dict()
    source = sources['ner'] if prediction.model.mode == Modes.NER else sources['classification']

    skipped = []
    created_topics = []
    created_labels = []
    created_pts = []

    with transaction.atomic(using='food'):

        # create topic and labels beforehand
        topics = results.values('topic').distinct()
        labels = results.values('label').distinct()

        for t in topics:
            topic, created_topic = Topic.objects.get_or_create(name=t['topic'])

            if created_topic:
                created_topics.append(topic)
            
        for l in labels:
            label, created_label = Label.objects.get_or_create(name=l['label'])

            if created_label:
                created_labels.append(label)

        for r in tqdm(results):
            topic = Topic.objects.get(name=r.topic)
            label = Label.objects.get(name=r.label)
            try:
                product = Product.objects.get(pk=r.product_id)
            except Product.DoesNotExist:
                print(f'product with id {r.product_id} is not found') # don't throw error, just log
                skipped += 1
            
            product_topic, created_pt = ProductTopic.objects.get_or_create(
                topic=topic,
                label=label,
                product=product,
                status=status,
                source=source
            )
            
            if created_pt:
                created_pts.append(product_topic)

    print(f'Created {len(created_topics)} topics')
    print(f'Created {len(created_labels)} labels')
    print(f'Created {len(created_pts)} product_topics')

            
