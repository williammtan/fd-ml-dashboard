from django.urls import path

from . import views

app_name = 'collection'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('new/', views.CollectionCreateView.as_view(), name='create'),
    path('edit/<int:pk>', views.CollectionEditView.as_view(), name='edit'),
    path('delete/<int:pk>', views.CollectionDeleteView.as_view(), name='delete')
]