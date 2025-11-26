from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado con roles para el sistema de solicitudes
    """
    ROLES = [
        ('alumno', 'Alumno'),
        ('control_escolar', 'Control Escolar'),
        ('responsable_programa', 'Responsable de Programa'),
        ('responsable_tutorias', 'Responsable de Tutorías'),
        ('director', 'Director'),
        ('administrador', 'Administrador'),
    ]
    
    rol = models.CharField(max_length=30, choices=ROLES, default='alumno')
    telefono = models.CharField(max_length=15, blank=True)
    matricula = models.CharField(max_length=20, blank=True, help_text="Solo para alumnos")
    area = models.CharField(max_length=100, blank=True, help_text="Área de trabajo para personal administrativo")
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_rol_display()})"
    
    def puede_crear_tipo_solicitud(self):
        """Control escolar y administrador pueden crear tipos de solicitud"""
        return self.rol in ['control_escolar', 'administrador']
    
    def puede_atender_solicitudes(self):
        """Roles que pueden atender solicitudes"""
        return self.rol in ['control_escolar', 'responsable_programa', 
                           'responsable_tutorias', 'director']
    
    def puede_ver_dashboard(self):
        """Solo administrador ve dashboard completo"""
        return self.rol == 'administrador'
    
    def puede_gestionar_usuarios(self):
        """Solo administrador puede gestionar usuarios"""
        return self.rol == 'administrador'
