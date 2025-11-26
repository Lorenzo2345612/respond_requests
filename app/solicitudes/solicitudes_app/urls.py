from django.urls import path
from . import views

app_name = 'solicitudes_app'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('usuarios/', views.lista_usuarios_view, name='lista_usuarios'),
    path('usuarios/<int:usuario_id>/editar/', views.editar_usuario_view, name='editar_usuario'),
    path('usuarios/<int:usuario_id>/eliminar/', views.eliminar_usuario_view, name='eliminar_usuario'),
]
