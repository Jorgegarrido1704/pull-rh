from . import views
from django.urls import path

urlpatterns = [
    path('', views.indexAlm, name='index'),
    path('registro_importacion/', views.registroimpo, name='registro_importacion'),
]