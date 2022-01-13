import os

from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ml_dashboard.settings')

app = Celery('ml_dashboard')
app.conf.broker_url = f'redis://localhost:{settings.REDIS_PORT}/0'
app.conf.result_backend = f'redis://localhost:{settings.REDIS_PORT}/0'
# app.conf.broker_url = 'sqla+sqlite:///db.sqlite3'
# app.conf.result_backend = 'db+sqlite:///db.sqlite3'

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')