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
    content = models.BinaryField()

    class Meta:
        db_table = 'example'

class Link(models.Model):
    example = models.ForeignKey(Example, models.DO_NOTHING, default=0)
    dataset = models.ForeignKey(Dataset, models.DO_NOTHING, default=0)

    class Meta:
        db_table = 'link'

