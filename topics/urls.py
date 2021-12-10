from django.urls import path

from . import views

app_name = 'topics'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('update/<int:pk>/', views.UpdateView.as_view(), name='update')
]