from django.db import models
from taggit.managers import TaggableManager
from django_celery_results.models import TaskResult
from ml_dashboard.celery import app
import time

from labeling.models import Dataset, Modes
from .tasks import train_prodigy


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

    def save(self, *args, **kwargs):
        if not self.path:
            self.path = self.name
        super(Model, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'models'

class Train(models.Model):
    """Model for all training sessions"""
    class Statuses(models.TextChoices):
        pending = 'Pending'
        running = 'Running'
        failed = 'Failed'
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
                return self.Statuses.failed
            elif self.task.status == 'FAILURE':
                return self.Statuses.failed
        else:
            return self.Statuses.pending

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
            return str(self.id)
    
    class Meta:
        db_table = 'trains'
