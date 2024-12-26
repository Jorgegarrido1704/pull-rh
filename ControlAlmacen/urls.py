from . import views
from django.urls import path

urlpatterns = [
    path('', views.indexAlm, name='index'),
]