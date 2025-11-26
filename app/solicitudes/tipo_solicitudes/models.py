from django.db import models
from django.conf import settings

RESPOSABLES = [
    ('1', 'Control escolar'),
    ('2', 'Responsable de programa'),
    ('3', 'Responsable de tutorías'),
    ('4', 'Director'),
]
class TipoSolicitud(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=350)
    responsable = models.CharField(max_length=1, choices=RESPOSABLES, default='1')

    def __str__(self):
        return self.nombre

class FormularioSolicitud(models.Model):
    tipo_solicitud = models.OneToOneField(TipoSolicitud, on_delete=models.CASCADE, related_name='formulario')
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"Formulario: {self.nombre}"

TIPO_CAMPO = [
    ('text', 'Texto corto'),
    ('textarea', 'Texto largo'),
    ('number', 'Número'),
    ('date', 'Fecha'),
    ('select', 'Selección'),
    ('file', 'Archivo'),
]
class CampoFormulario(models.Model):
    formulario = models.ForeignKey(FormularioSolicitud, on_delete=models.CASCADE, related_name='campos')
    nombre = models.CharField(max_length=100)
    etiqueta = models.CharField(max_length=150)
    tipo = models.CharField(max_length=20, choices=TIPO_CAMPO)
    requerido = models.BooleanField(default=True)
    opciones = models.TextField(blank=True, help_text="Usar comas para separar opciones (solo para tipo 'select')")
    cantidad_archivos = models.PositiveIntegerField(default=1, help_text="Aplica si el campo es tipo archivo")
    orden = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.etiqueta} ({self.tipo})"

ESTATUS = [
    ('1', 'Creada'),
    ('2', 'En proceso'),
    ('3', 'Terminada'),
    ('4', 'Cancelada'),
]

class Solicitud(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo_solicitud = models.ForeignKey(TipoSolicitud, on_delete=models.CASCADE)
    folio = models.CharField(max_length=20, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.folio}"

class RespuestaCampo(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='respuestas')
    campo = models.ForeignKey(CampoFormulario, on_delete=models.CASCADE)
    valor = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Respuesta {self.campo.nombre} -> {self.valor}"

def upload_path(instance, filename):
    return f"tickets/{instance.solicitud.folio}/{filename}"

class ArchivoAdjunto(models.Model):
    respuesta = models.ForeignKey(RespuestaCampo, on_delete=models.CASCADE, related_name='archivos', null=True, blank=True)
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='archivos')
    archivo = models.FileField(upload_to=upload_path)
    nombre = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Archivo {self.archivo.name}"

class SeguimientoSolicitud(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='seguimientos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_terminacion = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    estatus = models.CharField(max_length=1, choices=ESTATUS)
