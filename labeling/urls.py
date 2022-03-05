from django.urls import path

from . import views

app_name = 'labeling'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('new/', views.DatasetCreateView.as_view(), name='create'),
    path('<int:dataset_id>/results/<int:result_idx>', views.dataset_results, name='results')
]