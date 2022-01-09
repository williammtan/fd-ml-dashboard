from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'models'
urlpatterns = [
    path('api/indexer/product', csrf_exempt(views.index_products), name='index_products'),
]

