from django.conf import settings
from django.db import transaction
import pandas as pd
from celery import shared_task
from collections import defaultdict
import numpy as np
from gensim.models import Word2Vec
from sentence_transformers import SentenceTransformer
import pickle
from elasticsearch.helpers import bulk

from collection.models import Product
from models.tasks import PredictionTaskBase
from models.models import Model
from labeling.models import Modes
from topics.models import Topic, Label, ProductTopic, TopicSourceStatus, TopicStatus

@shared_task(bind=True)
def reindex(self, sbert_model, word2vec_save, w2v_size=100):
    self.update_state(state='PROGRESS')

    products = Product.objects.filter(is_deleted__exact=0)
    sentences = [list(set(p.topics.all().values_list('name', flat=True))) for p in products]

    word2vec = Word2Vec(sentences, min_count=1, vector_size=w2v_size)
    word2vec.save(word2vec_save)
    vocab = list(word2vec.wv.key_to_index.keys())
    w2v_embedding = np.zeros((len(products), word2vec.vector_size))
    product_index_embedding = {id: idx for idx, id in enumerate(products.values_list('id', flat=True))}

    for p in products:
        topics = list(p.producttopic_set.all().values_list('topic__name', flat=True))
        product_vec = np.average(np.array([
            word2vec.wv.get_vector(t)
            for t in topics
            if t in vocab
        ]), axis=0)
        w2v_embedding[product_index_embedding[p.id]] = product_vec
        

    with open(sbert_model, 'rb') as f:
        sbert = pickle.load(f)

    names = [p.name for p in products]
    sbert_embedding = sbert.encode(names, show_progress_bar=True)

    embedding = np.nan_to_num(np.concatenate((w2v_embedding, sbert_embedding), axis=1))

    SOURCE = {
        "mappings": {
            "dynamic": "true",
            "_source": {
                "enabled": "true"
            },
            "properties": {
                "category": {
                    "type": "long"
                },
                "outlet_id": {
                    "type": "long"
                },
                "is_active": {
                    "type": "byte"
                },
                "outlet_locale": {
                    "type": "keyword"
                },
                "delivery_area": {
                    "type": "long"
                },
                "vector": {
                    "type": "dense_vector",
                    "dims": embedding.shape[1],
                    "index": "true",
                    "similarity": "l2_norm"
                }
            }
        }
    }

    settings.ES.indices.delete(settings.ES_INDEX, ignore=[404])
    settings.ES.indices.create(index=settings.ES_INDEX, body=SOURCE)

    docs = []
    for p in products:
        outlet_locale = list(p.get_localizations().values_list('code', flat=True)) # we only need to store the code of the localization
        delivery_areas = p.get_delivery_cities()
        delivery_area = list()

        for da in delivery_areas:
            delivery_area.append(da.id)

        vec = embedding[product_index_embedding[p.id]]
        if np.any(vec):
            parent_category = p.get_parent_category()
            child_category = p.product_category

            category = [
                parent_category.id if parent_category else 0, 
                child_category.id if child_category else 0
            ] # category lvl 1, category lvl 2
            docs.append({
                '_id': p.id,
                'vector': vec,
                "category": category,
                'outlet_id': p.outlet.id,
                'is_active': p.is_active,
                'outlet_locale': outlet_locale,
                'delivery_area': delivery_area,
                '_op_type': 'index',
                '_index': settings.ES_INDEX
            })
    bulk(settings.ES, docs)
    settings.ES.indices.refresh(index=settings.ES_INDEX)

@shared_task(bind=True, base=PredictionTaskBase)
def update_index(self, product_ids, word2vec_model, sbert_model, batch_size=32):
    # self.update_state(state='PROGRESS')
    products = Product.objects.filter(id__in=product_ids)
    found_product_ids = set(products.values_list('id', flat=True))
    missing = set(product_ids) - found_product_ids
    print(f'missing {len(missing)} product ids')

    # iterate through models, finding which products use that model, then predicting and commiting the topics
    product_models = defaultdict(list) # dict model : [product1, product2, ...]

    for p in products:
        models = p.get_models()
        for m in models:
            product_models[m].append(p)
    
    word2vec = Word2Vec.load(word2vec_model)
    vocab = list(word2vec.wv.key_to_index.keys())
    w2v_embedding = np.zeros((len(products), word2vec.vector_size))
    product_index_embedding = {p.id: i for i, p in enumerate(products)}
        
    status = TopicStatus.objects.get(slug='ml-generated')
    sources = TopicSourceStatus.to_dict()
    product_topics = []
    
    for model, products_choice in product_models.items():
        source = sources['ner'] if model.mode == Modes.NER else sources['classification']

        nlp = model.load()

        # find the model's labels
        if model.mode == Modes.NER:
            entity_recognizer = nlp.get_pipe('ner')
            labels = entity_recognizer.labels
        # TODO: make changes so that the Model table stores a default 'label'
        # elif model.mode == Modes.TEXTCAT or model.mode == Modes.TEXTCAT_MULTILABEL:
            # if meta.get('label') is None:
            #     raise Exception('If the model is of mode TEXTCAT or TEXTCAT_MULTILABEL, it must contain the "label" metadata field.')
            
            # labels = [meta.get('label')]


        for p in products_choice:
            text = p.name + '\n' + p.description
            label_dict = self.PREDICT_FUNCTIONS[model.mode](self, nlp, text, label=None)
            for label, topics in label_dict.items():
                for t in topics:
                    product_topics.append({
                        'product_id': p.id,
                        'topic': t,
                        'label': label,
                        'status': status,
                        'source': source
                    })

    # append product_topics
    product_topics = pd.DataFrame(product_topics)
    if not product_topics.empty:
        product_topics_obj = []
        with transaction.atomic(using='food'):
            topics = product_topics.topic.unique()
            labels = product_topics.label.unique()

            for t in topics:
                topic, _ = Topic.objects.get_or_create(name=t)
                
            for l in labels:
                label, _ = Label.objects.get_or_create(name=l)
        
            for i, row in product_topics.iterrows():
                topic = Topic.objects.get(name=row.topic)
                label = Label.objects.get(name=row.label)
                try:
                    product = Product.objects.get(pk=row.product_id)
                except Product.DoesNotExist:
                    print(f'product with id {row.product_id} is not found') # don't throw error, just log

                product_topic = ProductTopic(
                    topic=topic,
                    label=label,
                    product=product,
                    status=row.status,
                    source=row.source
                )
                product_topics_obj.append(product_topic)

        ProductTopic.objects.bulk_create(product_topics_obj)

        # run word2vec and sbert on the models

        for product_id, pt in product_topics.groupby('product_id'):
            product_vec = np.average(np.array([
                word2vec.wv.get_vector(t)
                for t in pt.topic
                if t in vocab
            ]), axis=0)
            w2v_embedding[product_index_embedding[product_id]] = product_vec

    # sbert = settings.SBERT
    sbert = pickle.load(open(sbert_model, 'rb'))
    names = [p.name for p in products]

    sbert_embedding = []
    num_batches = len(names)//batch_size if len(names)//batch_size != 0 else 1
    for n in np.array_split(names, num_batches):
        encoded = sbert.encode(n, show_progress_bar=True)
        sbert_embedding.extend(encoded)

    sbert_embedding = np.array(sbert_embedding)

    embedding = np.nan_to_num(np.concatenate((w2v_embedding, sbert_embedding), axis=1))

    docs = []
    for p in products:
        outlet_locale = list(p.get_localizations().values_list('code', flat=True))
        delivery_areas = p.get_delivery_cities()
        delivery_area = list()

        for da in delivery_areas:
            delivery_area.append(da.id)

        vec = embedding[product_index_embedding[p.id]]
        if np.any(vec):
            parent_category = p.get_parent_category()
            child_category = p.product_category

            category = [
                parent_category.id if parent_category else 0, 
                child_category.id if child_category else 0
            ] # category lvl 1, category lvl 2
            
            docs.append({
                '_id': p.id,
                'vector': vec,
                "category": category,
                'outlet_id': p.outlet.id,
                'is_active': p.is_active,
                'outlet_locale': outlet_locale,
                'delivery_area': delivery_area,
                '_op_type': 'index',
                '_index': settings.ES_INDEX
            })
    bulk(settings.ES, docs)
    settings.ES.indices.refresh(index=settings.ES_INDEX)

