from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from elasticsearch.exceptions import NotFoundError
import json
import time

from collection.models import Product

from .tasks import update_index

def index_products(request):
    body = json.loads(request.body)
    ids = body.get('ids')

    if not ids:
        return HttpResponseBadRequest('body must include the field "ids"')
    
    if type(ids) != list:
        return HttpResponseBadRequest('"ids" must be a list of product ids')
    
    # task = update_index.delay(ids)
    # task.get(propagate=False) # TODO: timeout

    response = {}
    try:
        task = update_index(ids, 'data/models/w2v.model', 'data/models/sbert.pkl')
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
