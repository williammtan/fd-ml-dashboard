from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    # path(r'^(?P<url>[0-9]+)/$', views.TestProxyView.as_view(), name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:session_id>/prodigy/', views.prodigy_redirect, name='prodigy'),
    path('new/', views.get_recipe, name='create_recipe'),
    path('delete/<int:pk>', views.SessionDeleteView.as_view(), name='delete'),
    path('edit/<int:pk>', views.SessionEditView.as_view(), name='edit'),
    path('new/<str:recipe>/', views.create_session, name='recipe'),
    path('<int:session_id>/start', views.start_session, name='start'),
    path('<int:session_id>/stop', views.stop_session, name='stop')
]