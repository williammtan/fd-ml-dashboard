from django.urls import path

from . import views

app_name = 'models'
urlpatterns = [
    path('models/', views.ModelIndexView.as_view(), name='model_index'),
    path('models/<int:pk>', views.ModelDetailView.as_view(), name='model_detail'),
    path('models/new/', views.CreateModelView.as_view(), name='create_model'),
    path('models/edit/<int:pk>', views.EditModelView.as_view(), name='edit_model'),
    path('models/delete/<int:pk>', views.DeleteModelView.as_view(), name='delete_model'),
    path('train/', views.TrainIndexView.as_view(), name='train_index'),
    path('train/<int:pk>/', views.TrainDetailView.as_view(), name='train_detail'),
    path('train/<int:train_id>/start/', views.start_train, name='start_train'),
    path('train/<int:train_id>/stop/', views.stop_train, name='stop_train'),
    path('train/new/', views.CreateTrainView.as_view(), name='create_train'),
    path('prediction/', views.PredictionIndexView.as_view(), name='predict_index'),
    path('prediction/<int:pk>/', views.PredictionDetailView.as_view(), name='predict_detail'),
    path('prediction/<int:prediction_id>/start/', views.start_prediction, name='start_prediction'),
    path('prediction/<int:prediction_id>/stop/', views.stop_prediction, name='stop_prediction'),
    path('prediction/new/', views.CreatePredictionView.as_view(), name='create_prediction'),
    path('prediction/<int:prediction_id>/results/<int:result_idx>', views.prediction_results, name='prediction_results'),
    path('prediction/<int:prediction_id>/start-commit/', views.start_commit_prediction, name='start_commit_prediction'),
    path('prediction/<int:prediction_id>/stop-commit/', views.stop_commit_prediction, name='stop_commit_prediction'),
]