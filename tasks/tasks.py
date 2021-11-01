import celery
from celery import shared_task, Task
from django.apps import apps
from django_celery_results.models import TaskResult
from django.conf import settings
from .patterns import get_command, TRAIN
from tqdm import tqdm
import jsonlines
import prodigy
import logging
import socket
import time
import os

class TaskSessionBase(Task):
    def update_session(self, session_id):
        Session = apps.get_model('tasks', 'Session')
        self.session = Session.objects.get(pk=session_id)
        time.sleep(2)
        task = TaskResult.objects.get(task_id=self.request.id)
        self.session.task = task
        self.session.save()
    
    def generate_source(self):
        """Generate source file from dataset's collection"""
        collection = self.session.dataset.get_collection()
        products = collection.product_choice()
        source_path = os.path.join(settings.SOURCE_DIR, str(collection.id)) + '.jsonl'
        if not os.path.isfile(source_path):
            # if not already filled, fill
            logging.info('No source file for collection found, creating one now...(this may take a while)')
            with jsonlines.open(source_path, 'w') as writer:
                for p in tqdm(products):
                    writer.write({
                        'text': p.name + p.description,
                        'meta': {
                            'id': p.id,
                            'category': p.product_category.name
                        }
                    })
        else:
            logging.info('Using cached source file for this collection.')
        return source_path
    
    def generate_command(self):
        source_path = self.generate_source()
        meta = self.session.meta
        meta.update({
            'recipe': self.session.recipe,
            'dataset': self.session.dataset.name,
            'source': source_path
            # TODO: add model, source to meta_dict
        })
        command = get_command(**meta)
        self.update_state(state="PROGRESS", meta={'command': command})
        return command

class RunFailure(Exception):
    pass

def find_open_port(start_socket=8000):
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex(('0.0.0.0', start_socket))

        if result != 0:
            # port is NOT open
            return start_socket
        s.close()
        logging.info(f'Socket {start_socket} is open, trying {start_socket + 1}')

        start_socket += 1

@shared_task(bind=True, base=TaskSessionBase)
def serve_prodigy(self, session_id):
    self.update_state(state='PROGRESS')
    self.update_session(session_id)
    command = self.generate_command()

    class UvicornHandler(logging.StreamHandler):
        def emit(_, record):
            record = str(record)
            if 'CORS: initialized with wildcard "*" CORS origins' in record:
                logging.info('Prodigy session started, setting state to STARTED.')
                self.update_state(state='STARTED')

    logger = logging.getLogger('prodigy')
    logger.addHandler(UvicornHandler())

    port = find_open_port()
    os.environ['PRODIGY_LOGGING'] = 'basic'
    os.environ['PRODIGY_PORT'] = str(port)

    self.session.port = port # set the port value
    self.session.save()

    try:
        prodigy.serve(command, port=port)
    except Exception as err:
        self.update_state(state='FAILURE', meta={'error': err})
        raise RunFailure()

class TrainTaskBase(Task):
    def update_train(self, train_id):
        Train = apps.get_model('tasks', 'Train')
        self.train = Train.objects.get(pk=train_id)
        time.sleep(2)
        task = TaskResult.objects.get(task_id=self.request.id)
        self.train.task = task
        self.train.save()
    
    def generate_meta(self):
        meta = self.train.input_meta
        meta.update()

@shared_task(bind=True, base=TrainTaskBase)
def train_prodigy(self, train_id):
    self.update_state(state='PROGRESS')
    self.update_train(train_id)
    # train_input = TRAIN()(self.train.input_meta)
    prodigy.recipes.train.train(**self.train.input_meta)


@shared_task
def add(x, y):
    return x + y

@shared_task
def delay_add(x, y, delay):
    time.sleep(delay)
    return x + y

@shared_task(bind=True)
def long_task(self, x, y):
    i = 0
    while True:
        self.update_state(state='PROGRESS', meta={'done': i})
        time.sleep(10)
        print('still running...')
        i += 1