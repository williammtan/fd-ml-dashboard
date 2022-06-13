from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'models'
urlpatterns = [
    path('api/indexer/product', csrf_exempt(views.index_products), name='index_products'),
    path('api/indexer/product_all', csrf_exempt(views.index_all_products), name='index_all_products'),
    path('api/indexer/status/<str:task_id>', csrf_exempt(views.index_status), name='index_status'),
    path('api/indexer/product_reindex', csrf_exempt(views.reindex_products), name='reindex_products'),
    path('api/similar_product/<int:product_id>', csrf_exempt(views.similar), name='similar_product'),
    path('api/similar_product_many', csrf_exempt(views.similar_many), name='similar_product_many'),
    path('api/similar_product_many_category', csrf_exempt(views.similar_many_category), name="similar_product_many_category"),
    path('api/ping', csrf_exempt(views.ping), name="ping")
]

