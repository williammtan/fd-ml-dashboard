from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer
import pickle

class Command(BaseCommand):
    help = 'Downloads and saves a pickled file of SentenceTransformer model (example: "./manage.py save_sbert paraphrase-multilingual-MiniLM-L12-v2 -o data/models/sbert.pkl")'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='Path to model or name of pretrained model (https://www.sbert.net/docs/pretrained_models.html#multi-lingual-models)')
        parser.add_argument('-o', '--output', help='Path to store pickled model')

    def handle(self, *args, **options):
        sbert = SentenceTransformer(options['model'])
        with open(options['output'], 'wb') as f:
            pickle.dump(sbert, f)
            self.stdout.write(self.style.SUCCESS(f'Successfully saved sbert model {options["model"]} to {options["output"]}'))

