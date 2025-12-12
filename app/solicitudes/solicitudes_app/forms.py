from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError
import re
from .models import Usuario


class RegistroUsuarioForm(UserCreationForm):
    """
    Formulario para registro público - SOLO para alumnos
    El personal administrativo se crea desde el panel de administración
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
    # Campo oculto - siempre será 'alumno' en registro público
    rol = forms.ChoiceField(
        choices=[('alumno', 'Alumno')],
        initial='alumno',
        widget=forms.HiddenInput()
    )
    matricula = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-user',
        'placeholder': 'Matrícula'
    }))
    telefono = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-user',
        'placeholder': 'Teléfono (opcional)'
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
                  'matricula', 'telefono', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control form-control-user',
                'placeholder': 'Nombre de usuario'
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError(
                "El correo electrónico es obligatorio.")

        # Validar formato de email más estricto
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise forms.ValidationError(
                "Ingresa un correo electrónico válido.")

        # Validar que el email no esté duplicado
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este correo electrónico ya está registrado.")

        return email.lower()  # Normalizar a minúsculas

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError("El nombre de usuario es obligatorio.")

        # Validar longitud mínima
        if len(username) < 4:
            raise forms.ValidationError(
                "El nombre de usuario debe tener al menos 4 caracteres.")

        # Validar que solo contenga letras, números y guiones bajos
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError(
                "El nombre de usuario solo puede contener letras, números y guiones bajos.")

        # Validar que no esté duplicado
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Este nombre de usuario ya está en uso.")

        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError("El nombre es obligatorio.")

        # Validar que solo contenga letras y espacios
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', first_name):
            raise forms.ValidationError(
                "El nombre solo puede contener letras.")

        # Validar longitud mínima
        if len(first_name.strip()) < 2:
            raise forms.ValidationError(
                "El nombre debe tener al menos 2 caracteres.")

        return first_name.strip()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError("Los apellidos son obligatorios.")

        # Validar que solo contenga letras y espacios
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', last_name):
            raise forms.ValidationError(
                "Los apellidos solo pueden contener letras.")

        # Validar longitud mínima
        if len(last_name.strip()) < 2:
            raise forms.ValidationError(
                "Los apellidos deben tener al menos 2 caracteres.")

        return last_name.strip()

    def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula')
        if not matricula:
            return matricula

        # Validar formato de matrícula (ajusta según tu formato real)
        # Formato ejemplo: 5-8 dígitos numéricos
        if not re.match(r'^\d{5,8}$', matricula):
            raise forms.ValidationError(
                "La matrícula debe contener entre 5 y 8 dígitos.")

        # Validar que no esté duplicada
        if Usuario.objects.filter(matricula=matricula).exists():
            raise forms.ValidationError("Esta matrícula ya está registrada.")

        return matricula

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono:
            return telefono

        # Validar formato de teléfono (10 dígitos)
        telefono_limpio = re.sub(r'[^0-9]', '', telefono)
        if len(telefono_limpio) != 10:
            raise forms.ValidationError(
                "El teléfono debe contener exactamente 10 dígitos.")

        return telefono_limpio

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not password1:
            raise forms.ValidationError("La contraseña es obligatoria.")

        # Validar longitud mínima
        if len(password1) < 8:
            raise forms.ValidationError(
                "La contraseña debe tener al menos 8 caracteres.")

        # Validar que contenga al menos una letra mayúscula
        if not re.search(r'[A-Z]', password1):
            raise forms.ValidationError(
                "La contraseña debe contener al menos una letra mayúscula.")

        # Validar que contenga al menos una letra minúscula
        if not re.search(r'[a-z]', password1):
            raise forms.ValidationError(
                "La contraseña debe contener al menos una letra minúscula.")

        # Validar que contenga al menos un número
        if not re.search(r'\d', password1):
            raise forms.ValidationError(
                "La contraseña debe contener al menos un número.")

        # Validar que contenga al menos un carácter especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise forms.ValidationError(
                "La contraseña debe contener al menos un carácter especial (!@#$%^&*...).")

        return password1

    def clean(self):
        cleaned_data = super().clean()
        matricula = cleaned_data.get('matricula')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Forzar rol a 'alumno' en registro público
        cleaned_data['rol'] = 'alumno'

        # Validar que la matrícula sea obligatoria (siempre es alumno)
        if not matricula:
            self.add_error('matricula', 'La matrícula es obligatoria.')

        # Validar que las contraseñas coincidan
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')

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
        fields = ['first_name', 'last_name',
                  'email', 'telefono', 'area', 'matricula']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre(s)'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Área'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matrícula'}),
        }

    def clean_first_name(self):
        """Validar que el nombre solo contenga letras y espacios"""
        first_name = self.cleaned_data.get('first_name')
        if first_name and not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', first_name):
            raise ValidationError(
                'El nombre solo debe contener letras y espacios.')
        return first_name

    def clean_last_name(self):
        """Validar que los apellidos solo contengan letras y espacios"""
        last_name = self.cleaned_data.get('last_name')
        if last_name and not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', last_name):
            raise ValidationError(
                'Los apellidos solo deben contener letras y espacios.')
        return last_name

    def clean_email(self):
        """Validar que el email sea único (excepto el del usuario actual)"""
        email = self.cleaned_data.get('email')
        if email:
            # Verificar si otro usuario ya tiene este email
            usuarios_con_email = Usuario.objects.filter(
                email=email).exclude(id=self.instance.id)
            if usuarios_con_email.exists():
                raise ValidationError(
                    'Este correo electrónico ya está registrado.')
        return email

    def clean_telefono(self):
        """Validar formato de teléfono (10 dígitos)"""
        telefono = self.cleaned_data.get('telefono')
        if telefono and not re.match(r'^\d{10}$', telefono):
            raise ValidationError(
                'El teléfono debe contener exactamente 10 dígitos.')
        return telefono

    def clean_matricula(self):
        """Validar formato de matrícula (solo para alumnos)"""
        matricula = self.cleaned_data.get('matricula')
        if matricula:
            # Validar formato: 5-8 dígitos
            if not re.match(r'^\d{5,8}$', matricula):
                raise ValidationError(
                    'La matrícula debe contener entre 5 y 8 dígitos.')

            # Verificar que sea única (excepto el usuario actual)
            usuarios_con_matricula = Usuario.objects.filter(
                matricula=matricula).exclude(id=self.instance.id)
            if usuarios_con_matricula.exists():
                raise ValidationError('Esta matrícula ya está registrada.')

        return matricula


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

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Validar que solo contenga letras, números y guiones bajos
            if not re.match(r'^[a-zA-Z0-9_]+$', username):
                raise ValidationError(
                    'El nombre de usuario solo puede contener letras, números y guiones bajos.')
            # Verificar que no exista otro usuario con el mismo username (excluyendo el usuario actual)
            if Usuario.objects.filter(username=username).exclude(id=self.instance.id).exists():
                raise ValidationError('Este nombre de usuario ya está en uso.')
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            # Validar que solo contenga letras y espacios
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', first_name):
                raise ValidationError(
                    'El nombre solo puede contener letras y espacios.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            # Validar que solo contenga letras y espacios
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', last_name):
                raise ValidationError(
                    'El apellido solo puede contener letras y espacios.')
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Verificar que no exista otro usuario con el mismo email (excluyendo el usuario actual)
            if Usuario.objects.filter(email=email).exclude(id=self.instance.id).exists():
                raise ValidationError(
                    'Este correo electrónico ya está registrado.')
        return email

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            # Validar que tenga exactamente 10 dígitos
            if not re.match(r'^\d{10}$', telefono):
                raise ValidationError(
                    'El teléfono debe tener exactamente 10 dígitos.')
        return telefono

    def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula')
        if matricula:
            # Validar que tenga entre 5 y 8 dígitos
            if not re.match(r'^\d{5,8}$', matricula):
                raise ValidationError(
                    'La matrícula debe tener entre 5 y 8 dígitos.')
            # Verificar que no exista otro usuario con la misma matrícula (excluyendo el usuario actual)
            if Usuario.objects.filter(matricula=matricula).exclude(id=self.instance.id).exists():
                raise ValidationError('Esta matrícula ya está registrada.')
        return matricula
