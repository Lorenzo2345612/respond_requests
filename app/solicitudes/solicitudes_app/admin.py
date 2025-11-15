from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuración del panel de administración para el modelo Usuario
    """
    list_display = ['username', 'email', 'first_name', 'last_name', 'rol', 'is_active', 'date_joined']
    list_filter = ['rol', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'matricula']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('rol', 'telefono', 'matricula', 'area')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': ('rol', 'telefono', 'matricula', 'area')
        }),
    )
