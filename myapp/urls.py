
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pull/', include('pullTest.urls')),
    path('', include('login.urls')),
    path('rh/', include('rh.urls')),   
    path('herramental/', include('herramental.urls')),
    path('controlAlmacen/', include('ControlAlmacen.urls')),
]
