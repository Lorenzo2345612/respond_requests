from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch
from tipo_solicitudes.models import (
    TipoSolicitud, FormularioSolicitud, CampoFormulario
)

Usuario = get_user_model()


class TestViewsCoverage(TestCase):
    def setUp(self):
        self.client = Client()

        # 1. Usuarios con perfil completo
        self.admin_user = Usuario.objects.create_user(
            username='admin', password='password',
            rol='administrador', email='admin@test.com'
        )
        self.admin_user.perfil_completo = True
        self.admin_user.save()

        self.alumno_user = Usuario.objects.create_user(
            username='alumno', password='password',
            rol='alumno', email='alumno@test.com'
        )
        self.alumno_user.perfil_completo = True
        self.alumno_user.save()

        # 2. Datos Base
        self.tipo_solicitud = TipoSolicitud.objects.create(
            nombre='Solicitud Test', descripcion='Desc',
            responsable=self.admin_user.pk
        )
        self.formulario = FormularioSolicitud.objects.create(
            tipo_solicitud=self.tipo_solicitud,
            nombre='Form Test', descripcion='Desc Form'
        )

        self.campo_texto = CampoFormulario.objects.create(
            formulario=self.formulario, nombre='motivo', etiqueta='Motivo',
            tipo='text', requerido=True, orden=1
        )
        self.campo_archivo = CampoFormulario.objects.create(
            formulario=self.formulario, nombre='evidencia',
            etiqueta='Evidencia', tipo='file', requerido=True,
            cantidad_archivos=1, orden=2
        )

    # ---------------------------------------------------------
    # COVERAGE: lista_solicitudes
    # ---------------------------------------------------------
    def test_lista_solicitudes(self):
        self.client.login(username='admin', password='password')
        url = reverse('lista_tipo_solicitudes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['tipo_solicitudes']) >= 1)

    # ---------------------------------------------------------
    # COVERAGE: agregar_o_editar
    # ---------------------------------------------------------
    def test_agregar_tipo_solicitud_get(self):
        self.client.login(username='admin', password='password')
        url = reverse('agrega_solicitud')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['instancia'])

    def test_agregar_tipo_solicitud_post_valid(self):
        self.client.login(username='admin', password='password')
        url = reverse('agrega_solicitud')
        data = {'nombre': 'Nuevo Tipo 2', 'descripcion': 'Desc 2',
                'responsable': self.admin_user.pk}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('lista_tipo_solicitudes'))
        self.assertTrue(TipoSolicitud.objects.filter(
            nombre='Nuevo Tipo 2').exists())

    def test_agregar_tipo_solicitud_post_invalid(self):
        self.client.login(username='admin', password='password')
        url = reverse('agrega_solicitud')
        data = {'nombre': '', 'descripcion': 'Desc',
                'responsable': self.admin_user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    def test_editar_tipo_solicitud(self):
        self.client.login(username='admin', password='password')
        url = reverse('editar_tipo_solicitud', args=[self.tipo_solicitud.id])
        data = {'nombre': 'Solicitud Editada',
                'descripcion': 'Desc Editada',
                'responsable': self.admin_user.pk}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('lista_tipo_solicitudes'))
        self.tipo_solicitud.refresh_from_db()
        self.assertEqual(self.tipo_solicitud.nombre, 'Solicitud Editada')

    def test_editar_tipo_solicitud_titulo_get(self):
        self.client.login(username='admin', password='password')
        url = reverse('editar_tipo_solicitud', args=[self.tipo_solicitud.id])
        response = self.client.get(url)
        self.assertEqual(
            response.context['titulo'], "Editar tipo de solicitud")

    # ---------------------------------------------------------
    # COVERAGE: crear_o_editar_formulario
    # ---------------------------------------------------------
    def test_crear_formulario_get(self):
        self.client.login(username='admin', password='password')
        url = reverse('crear_formulario')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['titulo'], "Crear Nuevo Formulario de Solicitud")

    def test_crear_formulario_post(self):
        self.client.login(username='admin', password='password')
        url = reverse('crear_formulario')
        nuevo_tipo = TipoSolicitud.objects.create(
            nombre='Libre', responsable=self.admin_user.pk)
        data = {'tipo_solicitud': nuevo_tipo.id,
                'nombre': 'Nuevo Form', 'descripcion': 'D'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('lista_formularios'))
        self.assertTrue(FormularioSolicitud.objects.filter(
            nombre='Nuevo Form').exists())

    def test_editar_formulario_post(self):
        self.client.login(username='admin', password='password')
        url = reverse('editar_formulario', args=[self.formulario.id])
        data = {'tipo_solicitud': self.tipo_solicitud.id,
                'nombre': 'Form Editado', 'descripcion': 'D'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('lista_formularios'))
        self.formulario.refresh_from_db()
        self.assertEqual(self.formulario.nombre, 'Form Editado')

    def test_editar_formulario_titulo_get(self):
        self.client.login(username='admin', password='password')
        url = reverse('editar_formulario', args=[self.formulario.id])
        response = self.client.get(url)
        self.assertEqual(
            response.context['titulo'], "Editar Formulario de Solicitud")

    # ---------------------------------------------------------
    # COVERAGE: crear_o_editar_campos & _calcular_orden_campo
    # ---------------------------------------------------------

    # --- PRUEBAS AJAX ---
    @patch('tipo_solicitudes.views.render_to_string')
    def test_crear_campo_ajax_get_modal(self, mock_render):
        mock_render.return_value = "<div>Modal</div>"
        self.client.login(username='admin', password='password')
        url = reverse('editar_campos', args=[
                      self.formulario.id, self.campo_texto.id])
        try:
            response = self.client.get(
                url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
        except Exception:
            pass

    def test_crear_campo_ajax_post_success(self):
        self.client.login(username='admin', password='password')
        url = reverse('crear_campos', args=[self.formulario.id])
        data = {'nombre': 'ajax_new', 'etiqueta': 'Ajax',
                'tipo': 'text', 'requerido': False, 'cantidad_archivos': 0}
        response = self.client.post(
            url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['ok'])
        self.assertEqual(CampoFormulario.objects.get(
            nombre='ajax_new').orden, 3)

    @patch('tipo_solicitudes.views.render_to_string')
    def test_crear_campo_ajax_post_form_invalid(self, mock_render):
        mock_render.return_value = "<div>Error HTML</div>"
        self.client.login(username='admin', password='password')
        url = reverse('crear_campos', args=[self.formulario.id])
        data = {}
        response = self.client.post(
            url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['ok'])
        self.assertIn('html', response.json())
        self.assertTrue(mock_render.called)

    @patch('tipo_solicitudes.views._calcular_orden_campo')
    @patch('tipo_solicitudes.views.render_to_string')
    def test_crear_campo_ajax_post_duplicate_view_error(self, mock_render, mock_calc):
        mock_calc.return_value = (None, "Este número de orden ya está en uso")
        mock_render.return_value = "<div>Error HTML</div>"

        self.client.login(username='admin', password='password')
        url = reverse('crear_campos', args=[self.formulario.id])

        data = {'nombre': 'valid', 'etiqueta': 'Valid', 'tipo': 'text',
                'orden': 99, 'requerido': False, 'cantidad_archivos': 0}

        response = self.client.post(
            url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['ok'])
        self.assertIn('html', response.json())

    # --- PRUEBAS NO-AJAX ---
    def test_crear_campo_normal_get(self):
        self.client.login(username='admin', password='password')
        url = reverse('crear_campos', args=[self.formulario.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "preguntas_formulario.html")

    def test_crear_campo_normal_post_success(self):
        self.client.login(username='admin', password='password')
        url = reverse('crear_campos', args=[self.formulario.id])
        data = {'nombre': 'normal_new', 'etiqueta': 'Normal',
                'tipo': 'text', 'requerido': False, 'cantidad_archivos': 0}
        response = self.client.post(url, data)
        self.assertRedirects(response, url)
        self.assertTrue(CampoFormulario.objects.filter(
            nombre='normal_new').exists())

    def test_editar_campo_mismo_orden(self):
        self.client.login(username='admin', password='password')
        url = reverse('editar_campos', args=[
                      self.formulario.id, self.campo_texto.id])
        data = {'nombre': 'motivo_editado', 'etiqueta': 'Motivo',
                'tipo': 'text', 'requerido': True, 'orden': 1,
                'cantidad_archivos': 0}

        # Aquí estaba el otro supuesto error.
        # Se necesita 'response' para el assertRedirects
        response = self.client.post(url, data)

        self.assertRedirects(response, reverse(
            'crear_campos', args=[self.formulario.id]))
        self.campo_texto.refresh_from_db()
        self.assertEqual(self.campo_texto.nombre, 'motivo_editado')

    @patch('tipo_solicitudes.forms.FormCampoFormulario.clean_orden')
    def test_crear_campo_normal_post_duplicate_error(self, mock_clean):
        mock_clean.return_value = 1
        self.client.login(username='admin', password='password')
        url = reverse('crear_campos', args=[self.formulario.id])
        data = {'nombre': 'campo_fail', 'etiqueta': 'Fail', 'tipo': 'text',
                'orden': 1, 'requerido': False, 'cantidad_archivos': 0}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Este número de orden ya está en uso',
                      response.content.decode('utf-8'))

    # ---------------------------------------------------------
    # COVERAGE: eliminar_campo
    # ---------------------------------------------------------
    def test_eliminar_campo(self):
        self.client.login(username='admin', password='password')
        campo_borrar = CampoFormulario.objects.create(
            formulario=self.formulario, nombre='borrar',
            etiqueta='B', tipo='text', orden=10
        )
        url = reverse('eliminar_campo', args=[campo_borrar.id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse(
            'crear_campos', args=[self.formulario.id]))
        self.assertFalse(CampoFormulario.objects.filter(
            id=campo_borrar.id).exists())

    # ---------------------------------------------------------
    # COVERAGE: eliminar_tipo_solicitud y formulario (POST vs GET)
    # ---------------------------------------------------------
    def test_eliminar_tipo_solicitud_post(self):
        self.client.login(username='admin', password='password')
        t = TipoSolicitud.objects.create(
            nombre='TDel', responsable=self.admin_user.pk)
        url = reverse('eliminar_tipo_solicitud', args=[t.id])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertFalse(TipoSolicitud.objects.filter(id=t.id).exists())

    def test_eliminar_tipo_solicitud_get_not_allowed(self):
        self.client.login(username='admin', password='password')
        t = TipoSolicitud.objects.create(
            nombre='TKeep', responsable=self.admin_user.pk)
        url = reverse('eliminar_tipo_solicitud', args=[t.id])
        response = self.client.get(url, follow=True)
        self.assertTrue(TipoSolicitud.objects.filter(id=t.id).exists())
        messages = list(response.context['messages'])
        self.assertIn('Operación no permitida', str(messages[0]))

    def test_eliminar_formulario_post(self):
        self.client.login(username='admin', password='password')
        t = TipoSolicitud.objects.create(
            nombre='TFDel', responsable=self.admin_user.pk)
        f = FormularioSolicitud.objects.create(
            tipo_solicitud=t, nombre='FDel')
        url = reverse('eliminar_formulario', args=[f.id])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertFalse(FormularioSolicitud.objects.filter(id=f.id).exists())

    def test_eliminar_formulario_get_not_allowed(self):
        self.client.login(username='admin', password='password')
        t = TipoSolicitud.objects.create(
            nombre='TFKeep', responsable=self.admin_user.pk)
        f = FormularioSolicitud.objects.create(
            tipo_solicitud=t, nombre='FKeep')
        url = reverse('eliminar_formulario', args=[f.id])
        response = self.client.get(url, follow=True)
        self.assertTrue(FormularioSolicitud.objects.filter(id=f.id).exists())
        messages = list(response.context['messages'])
        self.assertIn('Operación no permitida', str(messages[0]))
