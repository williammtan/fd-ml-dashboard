from django.db import models
from taggit.managers import TaggableManager
from django_celery_results.models import TaskResult
from django.conf import settings
from django.utils import timezone
import spacy
import json
import time
import os

from ml_dashboard.celery import app
from labeling.models import Dataset, Modes
from collection.models import Collection, Product
from .tasks import train_prodigy, prediction, commit_predictions

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
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def file_path(self):
        return os.path.join(settings.MODEL_DIR, self.path)

    def save(self, *args, **kwargs):
        if not self.path:
            self.path = self.name
        
        if not os.path.isdir(self.file_path):
            os.makedirs(self.file_path)

        super(Model, self).save(*args, **kwargs)
    
    def load(self):
        """Load spacy model from file"""
        try:
            return spacy.load(self.file_path)
        except OSError:
            return spacy.load(os.path.join(self.file_path, 'model-best'))
    
    def dump(self, nlp):
        return nlp.to_disk(self.file_path)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'models'

class Train(models.Model):
    """Model for all training sessions"""
    class Statuses(models.TextChoices):
        not_started = 'Not Started'
        pending = 'Pending'
        running = 'Running'
        failed = 'Failed'
        cancelled = 'Cancelled'
        done = 'Done'

    name = models.CharField(max_length=200)
    model = models.ForeignKey(Model, on_delete=models.DO_NOTHING, null=True) # allow null, so that we can fill the model after we have finished training
    dataset = models.ForeignKey(Dataset, on_delete=models.DO_NOTHING, null=False, blank=False)
    task = models.OneToOneField(TaskResult, on_delete=models.CASCADE, null=True, blank=True)
    input_meta = models.JSONField(default=dict, blank=True) # input parameters to the model training
    train_meta = models.JSONField(default=dict, blank=True) # training results meta (like accuracy)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def status(self):
        if self.task is not None:
            if self.task.status == 'PENDING':
                return self.Statuses.pending
            elif self.task.status == 'PROGRESS':
                return self.Statuses.running
            elif self.task.status == 'SUCCESS':
                return self.Statuses.done
            elif self.task.status == 'FAILURE':
                return self.Statuses.failed
            elif self.task.status == 'REVOKED':
                return self.Statuses.cancelled
        elif (timezone.now() - self.created_at).seconds > settings.TRAIN_TIMEOUT:
            return self.Statuses.failed
        else:
            return self.Statuses.not_started

    def time_taken(self):
        """Time taken to run the training task"""
        if self.task:
            return self.task.date_done - self.task.date_created
    
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
    
    def get_input_meta(self):
        return json.dumps(self.input_meta, indent=4, sort_keys=True)
    
    def get_train_meta(self):
        return json.dumps(self.train_meta, indent=4, sort_keys=True)
    
    def __str__(self):
        if self.model is not None:
            return f'{self.model.name} - {self.dataset.name}'
        elif self.id is not None:
            return str(self.id)
    
    class Meta:
        db_table = 'trains'


class Prediction(models.Model):
    """Model for prediction tasks"""
    model = models.ForeignKey(Model, on_delete=models.DO_NOTHING)
    collection = models.IntegerField(null=False, blank=False)
    task = models.OneToOneField(TaskResult, on_delete=models.CASCADE, null=True, blank=True)
    meta = models.JSONField(default=dict, blank=True) # might contain "label": "some label for classification"
    commit_task = models.OneToOneField(TaskResult, on_delete=models.CASCADE, null=True, blank=True, related_name='commit_task')
    created_at = models.DateTimeField(auto_now_add=True)

    class Statuses(models.TextChoices):
        not_started = 'Not Started'
        pending = 'Pending'
        running = 'Running'
        failed = 'Failed'
        cancelled = 'Cancelled'
        done = 'Done'

    def start(self):
        task = prediction.delay(self.id)
        time.sleep(5)
        self.refresh_from_db()
        return task.id

    def close(self):
        """Terminate prediction"""
        task_id = self.task.task_id
        app.control.revoke(task_id, terminate=True)
        time.sleep(2)
        self.refresh_from_db()
    
    def start_commit(self):
        task = commit_predictions.delay(self.id)
        time.sleep(5)
        self.refresh_from_db()
    
    def close(self):
        """Terminate commit_prediction"""
        task_id = self.commit_task.task_id
        app.control.revoke(task_id, terminate=True)
        time.sleep(2)
        self.refresh_from_db()
    
    @property
    def status(self):
        if self.task is not None:
            if self.task.status == 'PENDING':
                return self.Statuses.pending
            elif self.task.status == 'PROGRESS':
                return self.Statuses.running
            elif self.task.status == 'SUCCESS':
                return self.Statuses.done
            elif self.task.status == 'FAILURE':
                return self.Statuses.failed
            elif self.task.status == 'REVOKED':
                return self.Statuses.cancelled
        # elif (timezone.now() - self.created_at).seconds > settings.PREDICTION_TIMEOUT:
        #     return self.Statuses.failed
        else:
            return self.Statuses.not_started
    
    @property
    def commit_status(self):
        if self.commit_task is not None:
            if self.commit_task.status == 'PENDING':
                return self.Statuses.pending
            elif self.commit_task.status == 'PROGRESS':
                return self.Statuses.running
            elif self.commit_task.status == 'SUCCESS':
                return self.Statuses.done
            elif self.commit_task.status == 'FAILURE':
                return self.Statuses.failed
            elif self.commit_task.status == 'REVOKED':
                return self.Statuses.cancelled
        # elif (timezone.now() - self.created_at).seconds > settings.PREDICTION_TIMEOUT:
        #     return self.Statuses.failed
        else:
            return self.Statuses.not_started
    
    def get_meta(self):
        return json.dumps(self.meta, indent=4, sort_keys=True)

    def get_collection(self):
        return Collection.objects.get(pk=self.collection)

    def time_taken(self):
        """Time taken to run the training task"""
        return self.task.date_done - self.task.date_created
    
    class Meta:
        db_table = 'predictions'

class PredictionResult(models.Model):
    """Model for prediction results"""
    product_id = models.IntegerField(blank=False, null=False)
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE, related_name='results')
    label = models.CharField(max_length=100, blank=False, null=False)
    topic = models.CharField(max_length=100, blank=False, null=False)

    @property
    def product(self):
        return Product.objects.get(pk=self.product_id)

    class Meta:
        db_table = 'prediction_results'

