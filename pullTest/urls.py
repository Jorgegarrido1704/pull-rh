from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('malas', views.malas, name='malas'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('graficas', views.graficas, name='graficas'),
]