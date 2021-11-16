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

from labeling.models import Modes

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

    with transaction.atomic(using='ml'):
        for p in products:
            text = p.name + '\n' + p.description
            label_dict = self.PREDICT_FUNCTIONS[self.prediction.model.mode](self, nlp, text, label=self.prediction.meta.get('label'))
            for label, topics in label_dict.items():
                for t in topics:
                    prediction_result = PredictionResult(product_id=p.id, prediction=self.prediction, label=label, topic=t)
                    prediction_result.save()
