from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'models'
urlpatterns = [
    path('api/indexer/product/', csrf_exempt(views.index_products), name='index_products'),
    path('api/indexer/product_reindex/<str:task_id>/', csrf_exempt(views.reindex_products_status), name='reindex_products_status'),
    path('api/indexer/product_reindex/', csrf_exempt(views.reindex_products), name='reindex_products'),
    path('api/similar_product/<int:product_id>/', csrf_exempt(views.similar), name='similar_product'),
    path('api/similar_product_many/', csrf_exempt(views.similar_many), name='similar_product_many'),
]

