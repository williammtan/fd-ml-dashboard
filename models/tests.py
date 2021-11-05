from django.test import TestCase
import spacy

from .models import Model
from labeling.models import Modes

class ModelTests(TestCase):
    databases = ['ml', 'food']

    def test_default_model_path(self):
        model = Model(name='test model', mode=Modes.NER)
        model.save()
        self.assertEqual(model.path, model.name)
    
    def test_model_tags(self):
        model = Model(name='test model', mode=Modes.NER)
        model.save()

        model.tags.add('test tag')
        model.save()
        self.assertListEqual([t.name for t in model.tags.only('name')], ['test tag'])
    
    def is_nlp_identical(self, nlp1, nlp2):
        """Given the idea that if 2 models are identical, and have the same weights, they must also have the same output"""
        doc1 = nlp1('test doc')
        doc2 = nlp2('test doc')
        return doc1.similarity(doc2) == 1
    
    def test_model_dump(self):
        model = Model(name='test blank model', mode=Modes.NER)
        nlp = spacy.load('blank:id')
        model.dump(nlp) # test saving the blank model

        new_nlp = spacy.load(model.file_path)
        self.assertTrue(self.is_nlp_identical(nlp, new_nlp))

    def test_model_load(self):
        model = Model(name='test blank model', mode=Modes.NER)
        nlp = spacy.load('blank:id')
        nlp.to_disk(model.file_path) # save the blank model without using model.dump

        new_nlp = model.load() # test loading
        self.assertTrue(self.is_nlp_identical(nlp, new_nlp))
    
