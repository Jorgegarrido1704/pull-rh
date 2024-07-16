from . import views
from django.urls import path

urlpatterns = [
    path('diarios', views.diarios, name='diarios'),
    path('', views.index, name='index'),
    path('mantenimientos', views.mantenimientos, name='mantenimientos'),
]