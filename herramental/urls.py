from . import views
from django.urls import path

urlpatterns = [
    path('diarios/', views.diarios, name='diarios'),
]