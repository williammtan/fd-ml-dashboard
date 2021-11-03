from django.urls import path

from . import views

app_name = 'models'
urlpatterns = [
    # path('', views.ModelIndexView.as_view(), name='index'),
    path('train/', views.TrainIndexView.as_view(), name='train_index'),
    path('train/<int:pk>/', views.TrainDetailView.as_view(), name='train_detail'),
    path('train/<int:train_id>/start/', views.start_train, name='start_train'),
    path('train/<int:train_id>/stop/', views.stop_train, name='stop_train'),
    path('train/new/', views.CreateTrainView.as_view(), name='create_train')
]