from django import forms
from .models import (
    ArchivoAdjunto, RespuestaCampo, SeguimientoSolicitud,
    TipoSolicitud, FormularioSolicitud, CampoFormulario,
    Solicitud
)


class FormTipoSolicitud(forms.ModelForm):
    class Meta:
        model = TipoSolicitud
        fields = '__all__'

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'style': 'resize: none;'
            }),
            'responsable': forms.Select(attrs={'class': 'form-control'}),
        }


class FormFormularioSolicitud(forms.ModelForm):
    class Meta:
        model = FormularioSolicitud
        fields = ['tipo_solicitud', 'nombre', 'descripcion']
        labels = {
            'tipo_solicitud': 'Tipo de Solicitud Asociada',
            'nombre': 'Título del Formulario',
            'descripcion': 'Instrucciones o Descripción'
        }
        widgets = {
            'tipo_solicitud': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'style': 'resize: none;'
            }),
        }


class FormCampoFormulario(forms.ModelForm):
    class Meta:
        model = CampoFormulario
        fields = ['formulario', 'nombre', 'etiqueta', 'tipo',
                  'requerido', 'opciones', 'cantidad_archivos', 'orden']
        labels = {
            'nombre': 'Nombre interno del campo',
            'etiqueta': 'Texto visible para el usuario',
            'tipo': 'Tipo de campo',
            'requerido': '¿Es obligatorio?',
            'opciones': 'Opciones (solo para select)',
            'cantidad_archivos': 'Cantidad de archivos permitidos',
            'orden': 'Posición en el formulario',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'etiqueta': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'requerido': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'opciones': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 6}
            ),
            'cantidad_archivos': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'orden': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # El formulario necesita saber qué formularioSolicitud está editando
        self.formulario = kwargs.pop("formulario", None)
        super().__init__(*args, **kwargs)
        self.fields['formulario'].required = False
        self.fields['formulario'].widget = forms.HiddenInput()
        self.fields['orden'].required = False

    def clean_orden(self):
        orden = self.cleaned_data.get("orden")

        if not orden:
            return orden

        if self.formulario:
            qs = CampoFormulario.objects.filter(
                formulario=self.formulario,
                orden=orden
            )

            # Si estamos editando un campo → excluirlo de la validación
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    "Ese número de orden ya está en uso para este formulario."
                )

        return orden

    def clean(self):
        cleaned = super().clean()
        tipo = cleaned.get('tipo')
        opciones = cleaned.get('opciones')

        if tipo == 'select' and (not opciones or opciones.strip() == ""):
            raise forms.ValidationError(
                "Debes agregar opciones separadas por comas para un campo select."
            )

        if tipo == 'file':
            cant = cleaned.get('cantidad_archivos')
            if not cant or cant < 1:
                raise forms.ValidationError(
                    "Debe permitir al menos 1 archivo.")

        return cleaned


class FormSolicitud(forms.ModelForm):
    class Meta:
        model = Solicitud
        exclude = ['usuario', 'folio', 'fecha_creacion', 'estatus']


class FormRespuestaCampo(forms.ModelForm):
    class Meta:
        model = RespuestaCampo
        fields = ['valor']


class FormSeguimientoSolicitud(forms.ModelForm):
    class Meta:
        model = SeguimientoSolicitud
        fields = ['observaciones', 'estatus']


class FormArchivoAdjunto(forms.ModelForm):
    class Meta:
        model = ArchivoAdjunto
        exclude = ['respuesta', 'solicitud']
        fields = ['archivo', 'nombre']
