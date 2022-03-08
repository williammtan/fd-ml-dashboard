from django.core.exceptions import ValidationError
from django.db import models
from django.apps import apps
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.db.models import Q
import time
import json

class IntegerDatetimeField(models.IntegerField):
    def pre_save(self, model_instance, add):
        return int(time.time())

def validate_dataset_name(name):
    if any([char in name for char in (",", " ")]):
        raise ValidationError(_('Invalid name, name cannot contain whitespaces or commas'))

class Modes(models.TextChoices):
    NER = 'NER',
    TEXTCAT = 'TEXTCAT'
    TEXTCAT_MULTILABEL = 'textcat_multilabel'

class Dataset(models.Model):

    name = models.CharField(max_length=100, unique=True, validators=[validate_dataset_name])
    created = IntegerDatetimeField('date created at', default=0)
    meta = models.JSONField(default=dict, blank=True)
    session = models.IntegerField(default=0)
    collection = models.IntegerField(default=0, blank=False, null=True)
    mode = models.CharField(
        max_length=50,
        choices=Modes.choices,
        default=Modes.NER,
        blank=True,
        null=True
    )

    def get_mode(self) -> Modes:
        return Modes[self.mode]
    
    def get_examples(self):
        return Example.objects.filter(link__dataset=self)
    
    def get_collection(self):
        Collection = apps.get_model('collection', 'Collection')
        return Collection.objects.get(pk=self.collection)
    
    def get_meta(self):
        return json.dumps(self.meta, indent=4, sort_keys=True)
    
    def get_active_sessions(self):
        Session = apps.get_model('tasks', 'Session')
        return Session.objects.filter(Q(task__status='STARTED') & Q(dataset=self)) # get sessions which have status STARTED and use this dataset
    
    def get_absolute_url(self):
        return reverse_lazy('labeling:detail', kwargs={'pk': self.id})
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'dataset'

class Example(models.Model):
    input_hash = models.IntegerField()
    task_hash = models.IntegerField()
    content = models.JSONField()

    def get_results(self):
        results = []

        if self.content['answer'] == 'accept':

            # add ner labels
            if self.content.get('spans') is not None:
                if self.content.get('tokens') is None:
                    return
                
                tokens = [t['text'] for t in self.content['tokens']]
                for span in self.content['spans']:
                    if span.get('token_start') is None or span.get('token_end') is None:
                        continue

                    topic_name = ' '.join(tokens[span['token_start']:span['token_end']+1])

                    results.append({
                        "topic": topic_name,
                        "label": span['label'].strip().lower(),
                    })
            
            # add classification labels
            if self.content.get('options') is not None:
                classes = self.clean_classes(self.content['options'])

                for label_id in self.content['accept']:
                    topic_name = [c['text'] for c in classes if c['id'] == label_id][0]

                    results.append({
                        "topic": topic_name,
                        "label": None,
                    })
            if self.content.get('user_input') is not None:
                for topic_name in self.content['user_input'].split('\n'):

                    results.append({
                        "topic": topic_name,
                        "label": None,
                    })
        
        # binary classification labels, skip if self.content['answer'] == 'accept'
        if self.content.get('label') is not None:
            label = self.content['label']

            if self.content['answer'] == 'accept':
                answer = 1
            elif self.content['answer'] == 'reject':
                answer = 0
            
            results.append({
                "topic": answer, # 1 or 0
                "label": label,
            })
    
        return results
    
    def get_product(self):
        meta = self.content.get('meta')
        if meta and type(meta) == dict:
            return meta.get('id')

    class Meta:
        db_table = 'example'

class Link(models.Model):
    example = models.ForeignKey(Example, models.CASCADE, default=0)
    dataset = models.ForeignKey(Dataset, models.CASCADE, default=0)

    class Meta:
        db_table = 'link'

