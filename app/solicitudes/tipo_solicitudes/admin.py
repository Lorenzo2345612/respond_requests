from django.contrib import admin
from .models import (TipoSolicitud, FormularioSolicitud, CampoFormulario,
Solicitud, RespuestaCampo, ArchivoAdjunto, SeguimientoSolicitud)

# Register your models here.
admin.site.register(TipoSolicitud)
admin.site.register(FormularioSolicitud)
admin.site.register(CampoFormulario)
admin.site.register(Solicitud)
admin.site.register(RespuestaCampo)
admin.site.register(ArchivoAdjunto)
admin.site.register(SeguimientoSolicitud)
