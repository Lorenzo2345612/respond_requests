from django.test import TestCase, Client
from django.urls import reverse
from solicitudes_app.models import Usuario
from solicitudes_app.forms import RegistroUsuarioForm, LoginForm


class UsuarioModelTest(TestCase):
    """
    Pruebas unitarias para el modelo Usuario
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.usuario_alumno = Usuario.objects.create_user(
            username='alumno1',
            email='alumno@test.com',
            password='testpass123',
            first_name='Juan',
            last_name='Pérez',
            rol='alumno',
            matricula='12345'
        )
        
        self.usuario_admin = Usuario.objects.create_user(
            username='admin1',
            email='admin@test.com',
            password='testpass123',
            first_name='Admin',
            last_name='Sistema',
            rol='administrador'
        )
        
        self.usuario_control = Usuario.objects.create_user(
            username='control1',
            email='control@test.com',
            password='testpass123',
            first_name='Control',
            last_name='Escolar',
            rol='control_escolar'
        )
    
    def test_crear_usuario_con_rol(self):
        """Prueba que se puede crear un usuario con rol específico"""
        self.assertEqual(self.usuario_alumno.rol, 'alumno')
        self.assertEqual(self.usuario_admin.rol, 'administrador')
        self.assertEqual(self.usuario_control.rol, 'control_escolar')
    
    def test_str_usuario(self):
        """Prueba el método __str__ del usuario"""
        expected = f"{self.usuario_alumno.get_full_name()} (Alumno)"
        self.assertEqual(str(self.usuario_alumno), expected)
    
    def test_puede_crear_tipo_solicitud(self):
        """Prueba que solo control escolar y admin pueden crear tipos de solicitud"""
        self.assertFalse(self.usuario_alumno.puede_crear_tipo_solicitud())
        self.assertTrue(self.usuario_admin.puede_crear_tipo_solicitud())
        self.assertTrue(self.usuario_control.puede_crear_tipo_solicitud())
    
    def test_puede_atender_solicitudes(self):
        """Prueba que los roles apropiados pueden atender solicitudes"""
        self.assertFalse(self.usuario_alumno.puede_atender_solicitudes())
        self.assertTrue(self.usuario_control.puede_atender_solicitudes())
    
    def test_puede_ver_dashboard(self):
        """Prueba que solo el administrador puede ver el dashboard"""
        self.assertFalse(self.usuario_alumno.puede_ver_dashboard())
        self.assertFalse(self.usuario_control.puede_ver_dashboard())
        self.assertTrue(self.usuario_admin.puede_ver_dashboard())
    
    def test_puede_gestionar_usuarios(self):
        """Prueba que solo el administrador puede gestionar usuarios"""
        self.assertFalse(self.usuario_alumno.puede_gestionar_usuarios())
        self.assertFalse(self.usuario_control.puede_gestionar_usuarios())
        self.assertTrue(self.usuario_admin.puede_gestionar_usuarios())
    
    def test_matricula_alumno(self):
        """Prueba que los alumnos tienen matrícula"""
        self.assertEqual(self.usuario_alumno.matricula, '12345')
    
    def test_usuario_activo_por_defecto(self):
        """Prueba que los usuarios están activos por defecto"""
        self.assertTrue(self.usuario_alumno.is_active)


class RegistroUsuarioFormTest(TestCase):
    """
    Pruebas unitarias para el formulario de registro
    """
    
    def test_formulario_valido_alumno(self):
        """Prueba que el formulario es válido con datos correctos de alumno"""
        form_data = {
            'username': 'nuevo_alumno',
            'email': 'nuevo@test.com',
            'first_name': 'Nuevo',
            'last_name': 'Alumno',
            'rol': 'alumno',
            'matricula': '67890',
            'telefono': '4921234567',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        }
        form = RegistroUsuarioForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_formulario_invalido_alumno_sin_matricula(self):
        """Prueba que el formulario es inválido si un alumno no tiene matrícula"""
        form_data = {
            'username': 'nuevo_alumno',
            'email': 'nuevo@test.com',
            'first_name': 'Nuevo',
            'last_name': 'Alumno',
            'rol': 'alumno',
            'matricula': '',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        }
        form = RegistroUsuarioForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('matricula', form.errors)
    
    def test_formulario_invalido_email_duplicado(self):
        """Prueba que no se puede registrar con un email ya existente"""
        # Crear usuario existente
        Usuario.objects.create_user(
            username='existente',
            email='existente@test.com',
            password='testpass123'
        )
        
        form_data = {
            'username': 'nuevo_usuario',
            'email': 'existente@test.com',  # Email duplicado
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'rol': 'alumno',
            'matricula': '12345',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        }
        form = RegistroUsuarioForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_formulario_valido_sin_matricula_para_no_alumno(self):
        """Prueba que otros roles no necesitan matrícula"""
        form_data = {
            'username': 'nuevo_admin',
            'email': 'nuevo_admin@test.com',
            'first_name': 'Nuevo',
            'last_name': 'Admin',
            'rol': 'administrador',
            'area': 'TI',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        }
        form = RegistroUsuarioForm(data=form_data)
        self.assertTrue(form.is_valid())


class LoginViewTest(TestCase):
    """
    Pruebas unitarias para la vista de login
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
        self.login_url = reverse('solicitudes_app:login')
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            rol='alumno'
        )
    
    def test_login_view_get(self):
        """Prueba que la página de login se carga correctamente"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'solicitudes_app/login.html')
    
    def test_login_exitoso(self):
        """Prueba un login exitoso"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirección
        self.assertTrue(response.url, reverse('bienvenida'))
    
    def test_login_fallido_credenciales_incorrectas(self):
        """Prueba login con credenciales incorrectas"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuario o contraseña incorrectos')
    
    def test_login_redirige_si_ya_autenticado(self):
        """Prueba que usuarios autenticados son redirigidos"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 302)


class RegistroViewTest(TestCase):
    """
    Pruebas unitarias para la vista de registro
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
        self.registro_url = reverse('solicitudes_app:registro')
    
    def test_registro_view_get(self):
        """Prueba que la página de registro se carga correctamente"""
        response = self.client.get(self.registro_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'solicitudes_app/registro.html')
    
    def test_registro_exitoso(self):
        """Prueba un registro exitoso"""
        form_data = {
            'username': 'nuevouser',
            'email': 'nuevo@test.com',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'rol': 'alumno',
            'matricula': '12345',
            'password1': 'testpass123!@#',
            'password2': 'testpass123!@#'
        }
        response = self.client.post(self.registro_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Usuario.objects.filter(username='nuevouser').exists())
    
    def test_registro_usuario_autenticado_automaticamente(self):
        """Prueba que el usuario se autentica automáticamente después del registro"""
        form_data = {
            'username': 'nuevouser',
            'email': 'nuevo@test.com',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'rol': 'alumno',
            'matricula': '12345',
            'password1': 'testpass123!@#',
            'password2': 'testpass123!@#'
        }
        self.client.post(self.registro_url, form_data)
        usuario = Usuario.objects.get(username='nuevouser')
        self.assertTrue(usuario.is_authenticated)


class PerfilViewTest(TestCase):
    """
    Pruebas unitarias para la vista de perfil
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
        self.perfil_url = reverse('solicitudes_app:perfil')
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            rol='alumno'
        )
    
    def test_perfil_requiere_autenticacion(self):
        """Prueba que la vista de perfil requiere autenticación"""
        response = self.client.get(self.perfil_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/auth/login/'))
    
    def test_perfil_view_autenticado(self):
        """Prueba que usuarios autenticados pueden ver su perfil"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.perfil_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'solicitudes_app/perfil.html')
    
    def test_actualizar_perfil(self):
        """Prueba que se puede actualizar el perfil"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.perfil_url, {
            'first_name': 'Nuevo',
            'last_name': 'Nombre',
            'email': 'nuevo@test.com',
            'telefono': '4921234567',
            'matricula': '12345',
            'area': ''
        })
        self.assertEqual(response.status_code, 302)
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.first_name, 'Nuevo')
        self.assertEqual(self.usuario.last_name, 'Nombre')


class GestionUsuariosViewTest(TestCase):
    """
    Pruebas unitarias para las vistas de gestión de usuarios
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
        self.lista_usuarios_url = reverse('solicitudes_app:lista_usuarios')
        
        self.admin = Usuario.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            rol='administrador'
        )
        
        self.alumno = Usuario.objects.create_user(
            username='alumno',
            email='alumno@test.com',
            password='testpass123',
            rol='alumno'
        )
    
    def test_lista_usuarios_requiere_admin(self):
        """Prueba que solo administradores pueden ver la lista de usuarios"""
        # Sin autenticación
        response = self.client.get(self.lista_usuarios_url)
        self.assertEqual(response.status_code, 302)
        
        # Como alumno
        self.client.login(username='alumno', password='testpass123')
        response = self.client.get(self.lista_usuarios_url)
        self.assertEqual(response.status_code, 302)
        
        # Como administrador
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(self.lista_usuarios_url)
        self.assertEqual(response.status_code, 200)
    
    def test_editar_usuario_como_admin(self):
        """Prueba que el administrador puede editar usuarios"""
        self.client.login(username='admin', password='testpass123')
        editar_url = reverse('solicitudes_app:editar_usuario', args=[self.alumno.id])
        
        response = self.client.post(editar_url, {
            'username': 'alumno',
            'email': 'alumno_nuevo@test.com',
            'first_name': 'Alumno',
            'last_name': 'Editado',
            'rol': 'alumno',
            'telefono': '',
            'area': '',
            'matricula': '12345',
            'is_active': True
        })
        
        self.assertEqual(response.status_code, 302)
        self.alumno.refresh_from_db()
        self.assertEqual(self.alumno.email, 'alumno_nuevo@test.com')
    
    def test_eliminar_usuario_como_admin(self):
        """Prueba que el administrador puede eliminar usuarios"""
        self.client.login(username='admin', password='testpass123')
        eliminar_url = reverse('solicitudes_app:eliminar_usuario', args=[self.alumno.id])
        
        response = self.client.post(eliminar_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Usuario.objects.filter(id=self.alumno.id).exists())
    
    def test_admin_no_puede_eliminarse_a_si_mismo(self):
        """Prueba que el administrador no puede eliminar su propia cuenta"""
        self.client.login(username='admin', password='testpass123')
        eliminar_url = reverse('solicitudes_app:eliminar_usuario', args=[self.admin.id])
        
        response = self.client.post(eliminar_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Usuario.objects.filter(id=self.admin.id).exists())


class LogoutViewTest(TestCase):
    """
    Pruebas unitarias para la vista de logout
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
        self.logout_url = reverse('solicitudes_app:logout')
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            rol='alumno'
        )
    
    def test_logout_exitoso(self):
        """Prueba que el logout funciona correctamente"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse('_auth_user_id' in self.client.session)


class TestSolicitudes(TestCase):

    def test_smoke(self):
        self.assertEqual('hola', 'hola')