from django.shortcuts import render
from django.core.exceptions import BadRequest
from django.http import JsonResponse
import json

from .tasks import update_index

def index_products(request):
    body = json.loads(request.body)
    ids = body.get('ids')

    if not ids:
        return BadRequest('body must include the field "ids"')
    
    if type(ids) != list:
        return BadRequest('"ids" must be a list of product ids')
    
    # task = update_index.delay(ids)
    # task.get(propagate=False) # TODO: timeout

    response = {}
    try:
        task = update_index(ids, 'data/models/w2v.model', 'data/models/sbert.pkl')
    except Exception as err:
        response['error'] = str(err)
        return JsonResponse(response, status=500)

    return JsonResponse({}, status=200)
