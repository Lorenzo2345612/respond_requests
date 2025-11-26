from django import forms


class CerrarSolicitudForm(forms.Form):
    ESTADO_CHOICES = (
        ('3', 'Terminada'),
        ('4', 'Cancelada'),
    )

    estatus = forms.ChoiceField(
        choices=ESTADO_CHOICES,
        required=True,
        error_messages={
            'required': 'El estatus es obligatorio.',
            'invalid_choice': 'Estatus inválido. Use 3 (Terminada) o 4 (Cancelada).'
        }
    )
    observaciones = forms.CharField(
        required=True,
        widget=forms.Textarea,
        error_messages={
            'required': 'Las observaciones son obligatorias.'
        }
    )

    def clean_estatus(self):
        value = (self.cleaned_data.get('estatus') or '').strip()
        if value not in ('3', '4'):
            raise forms.ValidationError('Estatus inválido. Use 3 (Terminada) o 4 (Cancelada).')
        return value

    def clean_observaciones(self):
        value = (self.cleaned_data.get('observaciones') or '').strip()
        if not value:
            raise forms.ValidationError('Las observaciones son obligatorias.')
        return value
