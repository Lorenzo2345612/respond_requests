from django.contrib import admin
from .models import (TipoSolicitud, FormularioSolicitud, CampoFormulario,
Solicitud, RespuestaCampo, ArchivoAdjunto, SeguimientoSolicitud)

# Register your models here.
admin.site.register(TipoSolicitud)
admin.site.register(FormularioSolicitud)
admin.site.register(CampoFormulario)

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ['folio', 'usuario', 'tipo_solicitud', 'fecha_creacion']
    
    def save_model(self, request, obj, form, change):
        """
        Sobrescribe el método save_model para crear automáticamente
        el seguimiento inicial cuando se crea una nueva solicitud
        """
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        
        # Si es una nueva solicitud, crear el seguimiento inicial
        if is_new:
            SeguimientoSolicitud.objects.create(
                solicitud=obj,
                estatus='1',
                observaciones='Solicitud creada desde el admin'
            )

admin.site.register(RespuestaCampo)
admin.site.register(ArchivoAdjunto)

@admin.register(SeguimientoSolicitud)
class SeguimientoSolicitudAdmin(admin.ModelAdmin):
    list_display = ['solicitud', 'estatus', 'fecha_creacion', 'fecha_terminacion']
    readonly_fields = ['fecha_terminacion']
    
    def save_model(self, request, obj, form, change):
        """
        Establece automáticamente fecha_terminacion cuando el estatus es '3' (Terminada)
        """
        # Si el estatus es '3' (Terminada) y no tiene fecha_terminacion, establecerla
        if obj.estatus == '3' and not obj.fecha_terminacion:
            from django.utils import timezone
            obj.fecha_terminacion = timezone.now()
        # Si el estatus no es '3', limpiar fecha_terminacion
        elif obj.estatus != '3':
            obj.fecha_terminacion = None
        
        super().save_model(request, obj, form, change)
