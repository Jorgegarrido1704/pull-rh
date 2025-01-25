from . import views
from django.urls import path

urlpatterns = [
    path('', views.indexAlm, name='indexAlm'),
    path('registro_importacion/', views.registroimpo, name='registro_importacion'),
    path('registroMovimiento/',views.registrosRecords,name='registroMovimiento'),
    path('cambios/',views.cambios,name='cambios'),
]