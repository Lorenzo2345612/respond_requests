from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class RegistroUsuarioForm(UserCreationForm):
    """
    Formulario para registro de nuevos usuarios con roles
    """
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-user',
        'placeholder': 'Correo electrónico'
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-user',
        'placeholder': 'Nombre(s)'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-user',
        'placeholder': 'Apellidos'
    }))
    rol = forms.ChoiceField(choices=Usuario.ROLES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    matricula = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-user',
        'placeholder': 'Matrícula (solo para alumnos)'
    }))
    telefono = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-user',
        'placeholder': 'Teléfono'
    }))
    area = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-user',
        'placeholder': 'Área de trabajo'
    }))
    
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Contraseña'
        })
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Repetir contraseña'
        })
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'rol', 
                  'matricula', 'telefono', 'area', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control form-control-user',
                'placeholder': 'Nombre de usuario'
            })
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        rol = cleaned_data.get('rol')
        matricula = cleaned_data.get('matricula')
        
        # Validar que los alumnos tengan matrícula
        if rol == 'alumno' and not matricula:
            self.add_error('matricula', 'La matrícula es obligatoria para alumnos.')
        
        return cleaned_data


class LoginForm(AuthenticationForm):
    """
    Formulario personalizado para login
    """
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-user',
        'placeholder': 'Nombre de usuario o correo'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-user',
        'placeholder': 'Contraseña'
    }))
    remember_me = forms.BooleanField(required=False, initial=False)


class ActualizarPerfilForm(forms.ModelForm):
    """
    Formulario para actualizar el perfil del usuario
    """
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono', 'area', 'matricula']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre(s)'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Área'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matrícula'}),
        }


class GestionarUsuarioForm(forms.ModelForm):
    """
    Formulario para que administrador gestione usuarios
    """
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'rol', 
                  'telefono', 'area', 'matricula', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
