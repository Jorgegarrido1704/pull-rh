from . import views
from django.urls import path

urlpatterns = [
    path('diarios', views.diarios, name='diarios'),
    path('', views.index, name='index'),
    path('mantenimientos', views.mantenimientos, name='mantenimientos'),
    path('new_manten', views.new_manten, name='new_manten'),
    path('add_mant', views.add_mant, name='add_mant'),
    path('man_real', views.man_real, name='man_real'),

]