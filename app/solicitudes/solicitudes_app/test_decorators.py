"""
Tests unitarios para decoradores de solicitudes_app (DSM5)
"""
from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from solicitudes_app.models import Usuario
from solicitudes_app.decorators import (
    rol_requerido,
    administrador_requerido,
    puede_crear_tipos,
    puede_atender_solicitudes,
    puede_ver_dashboard
)


class DecoradorRolRequeridoTest(TestCase):
    """Tests para el decorador rol_requerido"""

    def setUp(self):
        self.factory = RequestFactory()
        self.alumno = Usuario.objects.create_user(
            username='alumno1',
            email='alumno@test.com',
            password='testpass123',
            rol='alumno'
        )
        self.admin = Usuario.objects.create_user(
            username='admin1',
            email='admin@test.com',
            password='testpass123',
            rol='administrador'
        )

    def _add_messages_to_request(self, request):
        """Helper para agregar sistema de mensajes al request"""
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

    def test_usuario_no_autenticado_redirige_a_login(self):
        """Usuario no autenticado debe redirigir a login"""
        @rol_requerido('administrador')
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = AnonymousUser()
        self._add_messages_to_request(request)

        response = vista_test(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('login' in response.url)

    def test_usuario_con_rol_correcto_accede(self):
        """Usuario con rol correcto debe acceder a la vista"""
        @rol_requerido('administrador')
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = self.admin
        self._add_messages_to_request(request)

        response = vista_test(request)
        self.assertEqual(response, "success")

    def test_usuario_sin_rol_correcto_redirige(self):
        """Usuario sin el rol correcto debe redirigir a bienvenida"""
        @rol_requerido('administrador')
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = self.alumno
        self._add_messages_to_request(request)

        response = vista_test(request)
        self.assertEqual(response.status_code, 302)
        # Bienvenida is at root '/' or may include the name 'bienvenida'
        self.assertTrue('bienvenida' in response.url or response.url == '/')

    def test_multiples_roles_permitidos(self):
        """Decorador con múltiples roles debe permitir cualquiera"""
        @rol_requerido('alumno', 'administrador')
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = self.alumno
        self._add_messages_to_request(request)

        response = vista_test(request)
        self.assertEqual(response, "success")


class DecoradorAdministradorRequeridoTest(TestCase):
    """Tests para el decorador administrador_requerido"""

    def setUp(self):
        self.factory = RequestFactory()
        self.alumno = Usuario.objects.create_user(
            username='alumno1',
            email='alumno@test.com',
            password='testpass123',
            rol='alumno'
        )
        self.admin = Usuario.objects.create_user(
            username='admin1',
            email='admin@test.com',
            password='testpass123',
            rol='administrador'
        )

    def _add_messages_to_request(self, request):
        """Helper para agregar sistema de mensajes al request"""
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

    def test_admin_puede_acceder(self):
        """Administrador puede acceder a vista protegida"""
        @administrador_requerido
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = self.admin
        self._add_messages_to_request(request)

        response = vista_test(request)
        self.assertEqual(response, "success")

    def test_no_admin_no_puede_acceder(self):
        """No administrador no puede acceder"""
        @administrador_requerido
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = self.alumno
        self._add_messages_to_request(request)

        response = vista_test(request)
        self.assertEqual(response.status_code, 302)

    def test_usuario_no_autenticado_redirige(self):
        """Usuario no autenticado redirige a login"""
        @administrador_requerido
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = AnonymousUser()
        self._add_messages_to_request(request)

        response = vista_test(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('login' in response.url)


class DecoradorPuedeCrearTiposTest(TestCase):
    """Tests para el decorador puede_crear_tipos"""

    def setUp(self):
        self.factory = RequestFactory()
        self.alumno = Usuario.objects.create_user(
            username='alumno1',
            email='alumno@test.com',
            password='testpass123',
            rol='alumno'
        )
        self.control = Usuario.objects.create_user(
            username='control1',
            email='control@test.com',
            password='testpass123',
            rol='control_escolar'
        )
        self.admin = Usuario.objects.create_user(
            username='admin1',
            email='admin@test.com',
            password='testpass123',
            rol='administrador'
        )

    def _add_messages_to_request(self, request):
        """Helper para agregar sistema de mensajes al request"""
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

    def test_control_escolar_puede_crear_tipos(self):
        """Control escolar puede crear tipos de solicitud"""
        @puede_crear_tipos
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = self.control
        self._add_messages_to_request(request)

        response = vista_test(request)
        self.assertEqual(response, "success")

    def test_administrador_puede_crear_tipos(self):
        """Administrador puede crear tipos de solicitud"""
        @puede_crear_tipos
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = self.admin
        self._add_messages_to_request(request)

        response = vista_test(request)
        self.assertEqual(response, "success")

    def test_alumno_no_puede_crear_tipos(self):
        """Alumno no puede crear tipos de solicitud"""
        @puede_crear_tipos
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = self.alumno
        self._add_messages_to_request(request)

        response = vista_test(request)
        self.assertEqual(response.status_code, 302)

    def test_alumno_sin_permiso_mensaje_error(self):
        """Alumno sin permiso recibe mensaje de error específico"""
        @puede_crear_tipos
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = self.alumno
        self._add_messages_to_request(request)

        response = vista_test(request)
        
        # Verificar que hay mensajes
        storage = messages.get_messages(request)
        message_list = list(storage)
        self.assertTrue(len(message_list) > 0)
        
        # Verificar contenido del mensaje
        message_text = str(message_list[0])
        self.assertIn('permiso', message_text.lower())
        self.assertIn('crear tipos', message_text.lower())


class DecoradorPuedeAtenderSolicitudesTest(TestCase):
    """Tests para el decorador puede_atender_solicitudes_decorator"""

    def setUp(self):
        self.factory = RequestFactory()
        self.alumno = Usuario.objects.create_user(
            username='alumno1',
            email='alumno@test.com',
            password='testpass123',
            rol='alumno'
        )
        self.control = Usuario.objects.create_user(
            username='control1',
            email='control@test.com',
            password='testpass123',
            rol='control_escolar'
        )
        self.responsable_prog = Usuario.objects.create_user(
            username='resp_prog1',
            email='resp_prog@test.com',
            password='testpass123',
            rol='responsable_programa'
        )
        self.responsable_tut = Usuario.objects.create_user(
            username='resp_tut1',
            email='resp_tut@test.com',
            password='testpass123',
            rol='responsable_tutorias'
        )
        self.director = Usuario.objects.create_user(
            username='director1',
            email='director@test.com',
            password='testpass123',
            rol='director'
        )

    def _add_messages_to_request(self, request):
        """Helper para agregar sistema de mensajes al request"""
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

    def test_control_escolar_puede_atender(self):
        """Control escolar puede atender solicitudes"""
        @puede_atender_solicitudes
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = self.control
        self._add_messages_to_request(request)

        response = vista_test(request)
        self.assertEqual(response, "success")

    def test_responsable_programa_puede_atender(self):
        """Responsable de programa puede atender solicitudes"""
        @puede_atender_solicitudes
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = self.responsable_prog
        self._add_messages_to_request(request)

        response = vista_test(request)
        self.assertEqual(response, "success")

    def test_responsable_tutorias_puede_atender(self):
        """Responsable de tutorías puede atender solicitudes"""
        @puede_atender_solicitudes
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = self.responsable_tut
        self._add_messages_to_request(request)

        response = vista_test(request)
        self.assertEqual(response, "success")

    def test_director_puede_atender(self):
        """Director puede atender solicitudes"""
        @puede_atender_solicitudes
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = self.director
        self._add_messages_to_request(request)

        response = vista_test(request)
        self.assertEqual(response, "success")

    def test_alumno_no_puede_atender(self):
        """Alumno no puede atender solicitudes"""
        @puede_atender_solicitudes
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = self.alumno
        self._add_messages_to_request(request)

        response = vista_test(request)
        self.assertEqual(response.status_code, 302)

    def test_alumno_sin_permiso_atender_mensaje_error(self):
        """Alumno sin permiso para atender recibe mensaje de error"""
        @puede_atender_solicitudes
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = self.alumno
        self._add_messages_to_request(request)

        response = vista_test(request)
        
        # Verificar que hay mensajes
        storage = messages.get_messages(request)
        message_list = list(storage)
        self.assertTrue(len(message_list) > 0)
        
        # Verificar contenido del mensaje
        message_text = str(message_list[0])
        self.assertIn('permiso', message_text.lower())
        self.assertIn('atender solicitudes', message_text.lower())




class DecoradorPuedeVerDashboardTest(TestCase):
    """Tests para el decorador puede_ver_dashboard"""

    def setUp(self):
        self.factory = RequestFactory()
        self.admin = Usuario.objects.create_user(
            username='admin1',
            email='admin@test.com',
            password='testpass123',
            rol='administrador',
            perfil_completo=True
        )
        self.alumno = Usuario.objects.create_user(
            username='alumno1',
            email='alumno@test.com',
            password='testpass123',
            rol='alumno',
            perfil_completo=True
        )

    def _add_messages_to_request(self, request):
        """Helper para agregar sistema de mensajes al request"""
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

    def test_admin_puede_ver_dashboard(self):
        """Administrador puede ver dashboard"""
        @puede_ver_dashboard
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = self.admin
        self._add_messages_to_request(request)

        response = vista_test(request)
        self.assertEqual(response, "success")

    def test_no_admin_no_puede_ver_dashboard(self):
        """No administrador no puede ver dashboard"""
        @puede_ver_dashboard
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = self.alumno
        self._add_messages_to_request(request)

        response = vista_test(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('bienvenida' in response.url or response.url == '/')

    def test_usuario_no_autenticado_redirige(self):
        """Usuario no autenticado redirige a login"""
        @puede_ver_dashboard
        def vista_test(request):
            return "success"

        request = self.factory.get('/test/')
        request.user = AnonymousUser()
        self._add_messages_to_request(request)

        response = vista_test(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('login' in response.url)
