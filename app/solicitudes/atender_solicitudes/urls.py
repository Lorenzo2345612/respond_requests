from django.urls import path
from .views import atender_solicitud, marcar_solicitud_en_proceso, cerrar_solicitud, listar_solicitudes

urlpatterns = [
    path('atender_solicitud/<int:solicitud_id>/', atender_solicitud, name='atender_solicitud'),
    path('marcar-en-proceso/<int:solicitud_id>/', marcar_solicitud_en_proceso, name='marcar_solicitud_en_proceso'),
    path('cerrar/<int:solicitud_id>/', cerrar_solicitud, name='cerrar_solicitud'),
    path('listar/', listar_solicitudes, name='listar_solicitudes'),
]
