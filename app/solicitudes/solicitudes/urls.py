from django.contrib import admin
from django.urls import path, include
from tipo_solicitudes.views import bienvenida

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tipo-solicitud', include('tipo_solicitudes.urls')),
    path('', bienvenida, name='bienvenida'),
]
