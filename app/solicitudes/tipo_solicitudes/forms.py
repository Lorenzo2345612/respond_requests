from django import forms
from django.core.exceptions import ValidationError
from .models import TipoSolicitud, FormularioSolicitud, CampoFormulario, Solicitud
import os


class FormTipoSolicitud(forms.ModelForm):
    class Meta:
        model = TipoSolicitud
        fields = ['nombre', 'descripcion', 'responsable', 'destinatario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'responsable': forms.Select(attrs={'class': 'form-control'}),
            'destinatario': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre del tipo de solicitud',
            'descripcion': 'Descripción',
            'responsable': 'Responsable de atender',
            'destinatario': 'Dirigido a',
        }


class FormFormularioSolicitud(forms.ModelForm):
    class Meta:
        model = FormularioSolicitud
        fields = ['tipo_solicitud', 'nombre', 'descripcion']
        widgets = {
            'tipo_solicitud': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class FormCampoFormulario(forms.ModelForm):
    class Meta:
        model = CampoFormulario
        fields = ['nombre', 'etiqueta', 'tipo', 'requerido',
                  'opciones', 'cantidad_archivos', 'orden']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'etiqueta': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'requerido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'opciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cantidad_archivos': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'orden': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        self.formulario = kwargs.pop('formulario', None)
        super().__init__(*args, **kwargs)


class FormSolicitud(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['tipo_solicitud']


class FormArchivoAdjunto(forms.Form):
    archivo = forms.FileField()


def validar_archivo(archivo):
    """
    Valida que el archivo sea PDF o imagen y no supere 2MB
    """
    extensiones_permitidas = ['.pdf', '.jpg', '.jpeg', '.png', '.gif']

    ext = os.path.splitext(archivo.name)[1].lower()

    if ext not in extensiones_permitidas:
        raise ValidationError(
            f'Tipo de archivo no permitido: {ext}. Solo se aceptan: PDF, JPG, JPEG, PNG, GIF'
        )

    max_size = 2 * 1024 * 1024  # 2 MB en bytes
    if archivo.size > max_size:
        size_mb = archivo.size / (1024 * 1024)
        raise ValidationError(
            f'El archivo "{archivo.name}" es demasiado grande ({size_mb:.2f}MB). Tamaño máximo permitido: 2MB'
        )

    return archivo
