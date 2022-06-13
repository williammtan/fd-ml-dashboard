from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from elasticsearch.exceptions import NotFoundError
from pydantic import Json
from ml_dashboard.celery import app
import numpy as np
import json
import time

from collection.models import Product
from recommendation.helper import get_offset

from .tasks import update_index, reindex, update_all

def reindex_products(request):
    task = reindex.delay(word2vec_save='data/models/w2v.model', sbert_model='data/models/sbert.pkl')

    response = {
        'task_id': task.id
    }

    return JsonResponse(response, status=200)

def index_status(request, task_id):
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

    response = {
        'task_id': task.id,
    }

    return JsonResponse(response, status=200)

def index_all_products(request):
    if request.method == 'GET':
        batch_size = int(request.GET.get('size') or 1000)
        task = update_all.delay(batch_size)

        response = {
            'task_id': task.id
        }

        return JsonResponse(response, status=200)
    else:
        return HttpResponseBadRequest('Must be a GET request')

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

        try:
            page = int(request.GET.get('page') or settings.DEFAULT_SIZE)
        except ValueError:
            return HttpResponseBadRequest("Page must be an integer")

        try:
            city_id = int(request.GET.get('city_id'))
        except ValueError:
            return HttpResponseBadRequest("City ID must be an integer")

        locale = request.GET.get('locale', 'id')

        product = product_res['_source']
        product_vec = product['vector']
        
        script_query = {
            "script_score": {
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"outlet_locale": locale}},
                            {"match": {"delivery_area": city_id}},
                            {"match": {"is_active": 1}}
                        ],
                        "must_not": [
                            {"match": {"_id": product_id }}
                        ]
                    }
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                    "params": {"query_vector": product_vec}
                }
            }
        }

        res = settings.ES.search(index=settings.ES_INDEX, body={"size": size, "from": get_offset(page, size), "_source": ["_id"], "query": script_query})
        count = settings.ES.count(index=settings.ES_INDEX, body={"query": script_query})["count"]

        return JsonResponse({
            'data' : [
                {
                    "id": int(hit.get('_id')),
                    "similarity": hit.get('_score')
                }
                for hit in res['hits']['hits']
            ],
            'size': size,
            'page': page,
            'total': count,
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

        try:
            page = int(request.GET.get('page') or settings.DEFAULT_SIZE)
        except ValueError:
            return HttpResponseBadRequest("Page must be an integer")

        try:
            city_id = int(request.GET.get('city_id'))
        except ValueError:
            return HttpResponseBadRequest("City ID must be an integer")

        locale = request.GET.get('locale', 'id')

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
                        "must":[
                            {'match': {"outlet_locale": locale}},
                            {'match': {"delivery_area": city_id}},
                            {"match": {"is_active": 1}}
                        ],
                        "must_not": [
                            {"match": {"_id": product_id }}
                            for product_id in set(product_ids)
                        ]
                    }
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                    "params": {"query_vector": avg_product_vec}
                }
            }
        }
        
        res = settings.ES.search(index=settings.ES_INDEX, body={"size": size, "from": get_offset(page, size), "_source": ["_id"], "query": script_query})
        count = settings.ES.count(index=settings.ES_INDEX, body={"query": script_query})["count"]

        return JsonResponse({
            'data' : [
                {
                    "id": int(hit.get('_id')),
                    "similarity": hit.get('_score')
                }
                for hit in res['hits']['hits']
            ][:size],
            'size': size,
            'page': page,
            'total': count,
            'took': time.time()-now
        }, status=200)
    else:
        return HttpResponseBadRequest('Must be a GET request')

def similar_many_category(request):
    # The function is pretty *similar* to the similar_many function, except in this function we also
    # have to filter the result by the category (whether the level 1 category, or level 2 category).

    # Might be useful if we use an array of integers which has the level 1 category ID and level 2
    # category ID in the category column instead of only the level 1 category ID.

    # The product IDs filtering is done by the FD-API's side and it will send the Product IDs from the
    # same Category IDs, with their following families.

    body = json.loads(request.body.decode('utf-8'))
    now = time.time()

    if request.method == "GET":
        product_ids = body.get("product_ids")

        if not product_ids:
            return HttpResponseBadRequest('body must include the field "product_ids"')

        try:
            size = int(request.GET.get('size') or settings.DEFAULT_SIZE)
        except ValueError:
            return HttpResponseBadRequest('Size must be an integer')

        try:
            page = int(request.GET.get('page') or settings.DEFAULT_SIZE)
        except ValueError:
            return HttpResponseBadRequest("Page must be an integer")

        try:
            city_id = int(request.GET.get('city_id'))
        except ValueError:
            return HttpResponseBadRequest("City ID must be an integer")

        try:
            category_id = int(request.GET.get('category_id'))
        except ValueError:
            return HttpResponseBadRequest("Category ID must be an integer")

        locale = request.GET.get('locale', 'id')

        product_vecs = []

        for id in product_ids:
            try:
                product_res = settings.ES.get(index=settings.ES_INDEX, id=id)
            except NotFoundError:
                return HttpResponseNotFound(f"Product ID ({id}) not in settings.ES index")
            

            product = product_res['_source']
            product_vec = product['vector']

            product_vecs.append(product_vec)

        avg_product_vec = np.mean(product_vecs, axis=0)

        script_query = {
            "script_score": {
                "query": {
                    "bool": {
                        "must":[
                            {'match': {"category": category_id}},
                            {'match': {"outlet_locale": locale}},
                            {'match': {"delivery_area": city_id}},
                            {"match": {"is_active": 1}}
                        ],
                        "must_not": [
                            {"match": {"_id": product_id }}
                            for product_id in set(product_ids)
                        ]
                    }
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                    "params": {"query_vector": avg_product_vec}
                }
            }
        }

        res = settings.ES.search(index=settings.ES_INDEX, body={"size": size, "from": get_offset(page, size), "_source": ["_id"], "query": script_query})
        count = settings.ES.count(index=settings.ES_INDEX, body={"query": script_query})["count"]

        return JsonResponse({
            'data' : [
                {
                    "id": int(hit.get('_id')),
                    "similarity": hit.get('_score')
                }
                for hit in res['hits']['hits']
            ][:size],
            'size': size,
            'page': page,
            'total': count,
            'took': time.time() - now
        }, status=200)
    else:
        return HttpResponseNotFound("Request does not exist.")

def ping(request):
    # This function's sole purpose is to check whether the application deployed successfully.
    if request.method == "GET":
        return JsonResponse({
            "value": "pong"
        }, status=200)
    else:
        return HttpResponseNotFound("Request does not exist.")