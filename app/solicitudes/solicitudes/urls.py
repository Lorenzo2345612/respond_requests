from django.contrib import admin
from django.urls import path, include
from tipo_solicitudes.views import bienvenida
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tipo-solicitud/', include('tipo_solicitudes.urls')),
    path('auth/', include('solicitudes_app.urls')),
    path('solicitudes/', include('atender_solicitudes.urls')),
    path('', bienvenida, name='bienvenida'),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
