from django.urls import path
from tipo_solicitudes import views

'tipo-solicitud/'
urlpatterns = [
    path('', views.lista_solicitudes, name='lista_tipo_solicitudes'),  
    path('agregar/', views.agregar, name='agrega_solicitud'),
    path('crear-formulario/', views.crear_formulario, name='crear_formulario'),
]
