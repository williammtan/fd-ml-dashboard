import celery
from celery import shared_task, Task
from django.apps import apps
from django_celery_results.models import TaskResult
from django.conf import settings
import prodigy
import time
import os

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