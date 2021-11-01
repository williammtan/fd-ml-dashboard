from django.db import models
from django_celery_results.models import TaskResult
from taggit.managers import TaggableManager
from ml_dashboard.celery import app
from celery.result import AsyncResult
import time
import json

from .tasks import serve_prodigy, train_prodigy
from labeling.models import Dataset, Modes

class ModelTags(models.TextChoices):
    spacy = 'spacy'
    bert = 'bert'

class Session(models.Model):
    class Recipes(models.TextChoices):
        ner_manual = 'ner.manual'
        ner_correct = 'ner.correct'
        ner_teach = 'ner.teach'

    class Statuses(models.TextChoices):
        active = 'Active'
        pending = 'Pending'
        disabled = 'Disabled'

    name = models.CharField(max_length=100, blank=False)
    recipe = models.CharField(max_length=40, blank=False, null=False, choices=Recipes.choices) # required
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='sessions')
    meta = models.JSONField(default=dict, blank=True)
    port = models.IntegerField(blank=False, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.OneToOneField(TaskResult, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def status(self):
        if self.task is not None:
            return self.Statuses['active'] if self.task.status == 'STARTED' else self.Statuses['disabled']
        else:
            return self.Statuses['disabled']
    
    @property
    def active(self):
        return self.status == 'Active'
    
    @property
    def disabled(self):
        return self.status == 'Disabled'
    
    def get_meta(self):
        return json.dumps(self.meta, indent=4, sort_keys=True)
    
    def get_command(self):
        if self.task:
            task = AsyncResult(self.task.task_id)
            if task:
                return task.meta.get('command')
            
    
    def close(self):
        """Close prodigy session"""
        task_id = self.task.task_id
        app.control.revoke(task_id, terminate=True)
        time.sleep(2)
        self.refresh_from_db()
    
    def setup_prodigy_session(self):
        """Create dataset and run prodigy command"""
        task = serve_prodigy.delay(self.id) # run serve_prodigy with our full command
        time.sleep(5)
        self.refresh_from_db()
        return task.id
    
    class Meta:
        db_table = 'session'

class Model(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    path = models.CharField(max_length=100, blank=False, null=False)
    mode = models.CharField(
        max_length=50,
        choices=Modes.choices,
        default=Modes.NER,
        blank=True,
        null=True
    ) # we have modes for each model and dataset. The model's tag and dataset need to match
    tags = TaggableManager("Model Tags")
    # input_meta = models.JSONField(default=dict, blank=True) # input parameters to the model training
    # train_meta = models.JSONField(default=dict, blank=True) # training results

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'models'

class Train(models.Model):
    """Model for all training sessions"""
    model = models.ForeignKey(Model, on_delete=models.DO_NOTHING, null=True) # allow null, so that we can fill the model after we have finished training
    dataset = models.ForeignKey(Dataset, on_delete=models.DO_NOTHING, null=False, blank=False)
    task = models.OneToOneField(TaskResult, on_delete=models.CASCADE, null=True, blank=True)
    input_meta = models.JSONField(default=dict, blank=True) # input parameters to the model training
    train_meta = models.JSONField(default=dict, blank=True) # training results meta (like accuracy)

    def time_taken(self):
        """Time taken to run the training task"""
        return self.task.date_created - self.task.date_done
    
    def start(self):
        task = train_prodigy.delay(self.id)
        time.sleep(5)
        self.refresh_from_db()
        return task.id
    
    def close(self):
        """Terminate training"""
        task_id = self.task.task_id
        app.control.revoke(task_id, terminate=True)
        time.sleep(2)
        self.refresh_from_db()
    
    def __str__(self):
        if self.model is not None:
            return f'{self.model.name} - {self.dataset.name}'
        elif self.id is not None:
            return self.id
    
    class Meta:
        db_table = 'trains'

# class Prediction(models.Model):
#     model = models.ForeignKey(Model, on_delete=models.DO_NOTHING)
#     task = models.OneToOneField(TaskResult, on_delete=models.CASCADE, null=True, blank=True)

#     def time_taken(self):
#         """Time taken to run the training task"""
#         return self.task.date_created - self.task.date_done
    
#     def teset(self):
#         return PeriodicTask()
