from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
   path('vacaciones/', views.vacaciones, name='vacaciones'),
    path('vacaciones_detalles/<str:id_empleado>/', views.vacaciones_detalles, name='vacaciones_detalles'),
    path('reportes/<str:numero_empleado>/', views.reportes, name='reportes'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
]