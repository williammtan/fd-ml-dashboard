from django.urls import path

from . import views

app_name = 'models'
urlpatterns = [
    # path('', views.ModelIndexView.as_view(), name='index'),
    path('train/', views.TrainIndexView.as_view(), name='train_index'),
]