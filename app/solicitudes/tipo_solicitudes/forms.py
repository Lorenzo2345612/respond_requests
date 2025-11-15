from django import forms
from .models import ArchivoAdjunto, RespuestaCampo, SeguimientoSolicitud, TipoSolicitud, FormularioSolicitud, CampoFormulario, TIPO_CAMPO, Solicitud

class FormTipoSolicitud(forms.ModelForm):
    class Meta:
        model = TipoSolicitud
        fields = '__all__'
        
class FormFormularioSolicitud(forms.ModelForm):
    class Meta:
        model = FormularioSolicitud
        fields = ['tipo_solicitud', 'nombre', 'descripcion']
        labels = {
            'tipo_solicitud': 'Tipo de Solicitud Asociada',
            'nombre': 'Título del Formulario',
            'descripcion': 'Instrucciones o Descripción'
        }
        
class FormCampoFormulario(forms.ModelForm):
    class Meta:
        model = CampoFormulario
        fields = ['nombre', 'etiqueta', 'tipo', 'requerido', 'opciones', 'cantidad_archivos', 'orden']
        labels = {
            'nombre': 'Nombre interno del campo',
            'etiqueta': 'Texto visible para el usuario',
            'tipo': 'Tipo de campo',
            'requerido': '¿Es obligatorio?',
            'opciones': 'Opciones (solo para select)',
            'cantidad_archivos': 'Cantidad de archivos permitidos',
            'orden': 'Posición en el formulario',
        }

    def __init__(self, *args, **kwargs):
        # El formulario necesita saber qué formularioSolicitud está editando
        self.formulario = kwargs.pop("formulario", None)
        super().__init__(*args, **kwargs)

    def clean_orden(self):
        orden = self.cleaned_data.get("orden")

        # Solo validar si el formulario fue pasado
        if self.formulario:
            existe = CampoFormulario.objects.filter(
                formulario=self.formulario,
                orden=orden
            ).exists()

            if existe:
                raise forms.ValidationError("Ese número de orden ya está en uso para este formulario.")

        return orden

    def clean(self):
        cleaned = super().clean()
        tipo = cleaned.get('tipo')
        opciones = cleaned.get('opciones')

        if tipo == 'select' and (not opciones or opciones.strip() == ""):
            raise forms.ValidationError("Debes agregar opciones separadas por comas para un campo select.")

        if tipo == 'file':
            cant = cleaned.get('cantidad_archivos')
            if not cant or cant < 1:
                raise forms.ValidationError("Debe permitir al menos 1 archivo.")

        return cleaned



class FormSolicitud(forms.ModelForm):
    class Meta:
        model = Solicitud
        exclude = ['usuario', 'folio', 'fecha_creacion']
        
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