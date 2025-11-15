from django.urls import path
from tipo_solicitudes import views

'tipo-solicitud/'
urlpatterns = [
<<<<<<< HEAD
    path('', views.lista_solicitudes, name='lista_tipo_solicitudes'),  
    path('agregar/', views.agregar, name='agrega_solicitud'),
    path('crear-formulario/', views.crear_formulario, name='crear_formulario'),
=======
    path('', views.agregar, name='agrega_solicitud'),
    path('lista', views.lista_solicitudes, name='lista_tipo_solicitudes'),
    path('crear-formulario', views.crear_formulario, name='crear_formulario'),
    path('formulario/<int:formulario_id>/campos/', views.crear_campos, name='crear_campos'),
    path('formulario/campo/<int:campo_id>/eliminar/', views.eliminar_campo, name='eliminar_campo'),
>>>>>>> 2e0532116dbc708af21493ab5a4cf81df3849071
]
