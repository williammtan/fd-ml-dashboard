from django.test import TestCase, override_settings
from django.conf import settings
from celery.result import AsyncResult
import spacy
import os

from .models import Model, Prediction, PredictionResult
from collection.models import Collection, Product
from labeling.models import Modes

@override_settings(MODEL_DIR=settings.TEST_MODEL_DIR, SOURCE_DIR=settings.TEST_SOURCE_DIR)
class ModelTests(TestCase):
    databases = ['ml', 'food']

    def test_default_model_path(self):
        model = Model(name='test model', mode=Modes.NER)
        model.save()
        self.assertEqual(model.path, model.name)
    
    def test_create_model_path(self):
        model = Model(name='test model', mode=Modes.NER, path='test_create_dir')
        if os.path.isdir(model.file_path):
            os.rmdir(model.file_path) # remove the dir first
        model.save()
        self.assertTrue(os.path.isdir(model.file_path)) # then check if the dir is created
    
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
    

@override_settings(MODEL_DIR=settings.TEST_MODEL_DIR, SOURCE_DIR=settings.TEST_SOURCE_DIR)
class PredictionModelTests(TestCase):
    databases = {'ml', 'food'}
    fixtures = ['collection_fixtures',]

    def setUp(self):
        print(Product._meta.managed)
        self.collection = Collection.objects.get(pk=1) # load collection fixtures
        print(self.collection)
    
    def test_pass(self):
        self.assertEqual(1,1)

    # def test_prediction_ner(self):
    #     model = Model(name='test_ner_model', path=os.path.join(settings.TEST_SOURCE_DIR, 'buah_sayur_model'), mode=Modes.NER)
    #     model.save()

    #     prediction = Prediction(model=model, collection_id=self.collection.id)
    #     prediction.start()
    #     self.assertIsNotNone(prediction.task) # this might check if the task is never run, or might be waiting in some queue

    #     prediction_task = AsyncResult(prediction.task.task_id)
    #     prediction_task.get() # wait until finish

    #     prediction_result = prediction.prediction_result_choice.all()
    #     self.assertNotEqual(len(prediction_result), 0) # assert not empty results
    
#     def test_prediction_textcat(self):
#         model = Model(name='test_ner_model', path=os.path.join(settings.TEST_SOURCE_DIR, 'buah_sayur_model'), mode=Modes.TEXTCAT)
#         model.save()

#         prediction = Prediction(model=model, collection_id=self.collection.id)
#         prediction.start()
#         self.assertIsNotNone(prediction.task) # this might check if the task is never run, or might be waiting in some queue

#         prediction_task = AsyncResult(prediction.task.task_id)
#         prediction_task.get() # wait until finish

#         prediction_result = prediction.prediction_result_choice.all()
#         self.assertNotEqual(len(prediction_result), 0) # assert not empty results

