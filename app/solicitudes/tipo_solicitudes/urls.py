from django.urls import path
from tipo_solicitudes import views


urlpatterns = [
    path('', views.agregar, name='agrega_solicitud'),
]
