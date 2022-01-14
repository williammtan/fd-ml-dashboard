from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from elasticsearch.exceptions import NotFoundError
from ml_dashboard.celery import app
import numpy as np
import json
import time

from collection.models import Product

from .tasks import update_index, reindex

def reindex_products(request):
    task = reindex.delay(word2vec_save='data/models/w2v.model', sbert_model='data/models/sbert.pkl')

    response = {
        'task_id': task.id
    }

    return JsonResponse(response, status=200)

def reindex_products_status(request, task_id):
    task = app.AsyncResult(task_id)
    if request.method == 'GET':
        # just get reindex status
        state = task.state

        if state == 'FAILURE' or state == 'REVOKED':
            # then state MUST be an Exception
            return JsonResponse({
                'state': state,
                'error': str(task.info)
            }, status=500)
        else:
            response = {
                'state': state,
                'meta': task.info
            }
            return JsonResponse(response, status=200)

    elif request.method == 'DELETE':
        # terminate reindex
        app.control.revoke(task_id, terminate=True)
        return JsonResponse({}, status=204)
    else:
        return HttpResponseBadRequest('Not valid method in this endpoint')

def index_products(request):
    body = json.loads(request.body.decode('utf-8'))
    ids = body.get('ids')

    if not ids:
        return HttpResponseBadRequest('body must include the field "ids"')
    
    if type(ids) != list:
        return HttpResponseBadRequest('"ids" must be a list of product ids')
    
    task = update_index.delay(ids, 'data/models/w2v.model', 'data/models/sbert.pkl')

    response = {}
    try:
        task.get() # TODO: timeout
    except Exception as err:
        response['error'] = str(err)
        return JsonResponse(response, status=500)

    return JsonResponse({}, status=200)

def similar(request, product_id):

    now = time.time()
    if request.method == 'GET':
        try:
            size = int(request.GET.get('size') or settings.DEFAULT_SIZE)
        except ValueError:
            return HttpResponseBadRequest('Size must be an integer')
        try:
            product_res = settings.ES.get(index=settings.ES_INDEX, id=product_id)
        except NotFoundError:
            return HttpResponseNotFound(f"Product ID ({product_id}) not in ES index")

        product = product_res['_source']
        product_vec = product['vector']
        
        script_query = {
            "script_score": {
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"category": product['category']}} # category must match
                        ]
                    }
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                    "params": {"query_vector": product_vec}
                }
            }
        }
        res = settings.ES.search(index=settings.ES_INDEX, body={"size": size+1, "_source": ["_id"], "query": script_query})
        return JsonResponse({
            'data' : [
                {
                    "id": int(hit.get('_id')),
                    "similarity": hit.get('_score')
                }
                for hit in res['hits']['hits']
                if int(hit.get('_id')) != product_id
            ],
            'took': time.time()-now
        }, status=200)
    else:
        return HttpResponseBadRequest('Must be a GET request')

def similar_many(request):
    body = json.loads(request.body.decode('utf-8'))
    now = time.time()

    if request.method == 'GET':
        product_ids = body.get('product_ids')

        if not product_ids:
            return HttpResponseBadRequest('body must include the field "product_ids"')

        try:
            size = int(request.GET.get('size') or settings.DEFAULT_SIZE)
        except ValueError:
            return HttpResponseBadRequest('Size must be an integer')

        categories = []
        product_vecs = []

        for id in product_ids:
            try:
                product_res = settings.ES.get(index=settings.ES_INDEX, id=id)
            except NotFoundError:
                return HttpResponseNotFound(f"Product ID ({id}) not in settings.ES index")
            

            product = product_res['_source']
            product_vec = product['vector']

            categories.append(product['category'])
            product_vecs.append(product_vec)
        
        avg_product_vec = np.mean(product_vecs, axis=0)

        script_query = {
            "script_score": {
                "query": {
                    "bool": {
                        "should": [
                            {'match': {"category": c}}
                            for c in set(categories)
                        ],
                        "minimum_should_match" : 1
                    }
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                    "params": {"query_vector": avg_product_vec}
                }
            }
        }
        res = settings.ES.search(index=settings.ES_INDEX, body={"size": size+len(product_ids), "_source": ["_id"], "query": script_query})
        return JsonResponse({
            'data' : [
                {
                    "id": int(hit.get('_id')),
                    "similarity": hit.get('_score')
                }
                for hit in res['hits']['hits']
                if int(hit.get('_id')) not in product_ids
            ][:size],
            'took': time.time()-now
        }, status=200)
    else:
        return HttpResponseBadRequest('Must be a GET request')
