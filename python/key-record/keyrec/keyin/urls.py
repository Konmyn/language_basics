from django.urls import path

from . import views

urlpatterns = [
    path('', views.keyin, name='index'),
    path('info/', views.info, name='info'),
    path('cloud/', views.cloud, name='cloud'),
]