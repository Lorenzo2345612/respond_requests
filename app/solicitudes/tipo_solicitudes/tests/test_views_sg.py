from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from tipo_solicitudes.models import TipoSolicitud, FormularioSolicitud, CampoFormulario, Solicitud


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='cris', password='1234')

        self.tipo = TipoSolicitud.objects.create(
            nombre="Constancia",
            descripcion="Prueba",
            responsable="1"
        )

        self.formulario = FormularioSolicitud.objects.create(
            tipo_solicitud=self.tipo,
            nombre="Form Const",
            descripcion="desc"
        )

        CampoFormulario.objects.create(
            formulario=self.formulario,
            nombre="motivo",
            etiqueta="Motivo",
            tipo="text"
        )

    def test_lista_solicitudes_view(self):
        response = self.client.get(reverse('lista_tipo_solicitudes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lista_tipo_solicitudes.html')

    def test_agregar_tipo_solicitud(self):
        response = self.client.post(reverse('agrega_solicitud'), {
            'nombre': "Nuevo",
            'descripcion': "desc",
            'responsable': "2"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TipoSolicitud.objects.filter(nombre="Nuevo").exists())

    def test_crear_solicitud(self):
        self.client.login(username='cris', password='1234')

        url = reverse('crear_solicitud', args=[self.tipo.id])

        resp = self.client.post(url, {
            'motivo': "Necesito constancia"
        })

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Solicitud.objects.filter(usuario=self.user).exists())

    def test_mis_solicitudes_view(self):
        self.client.login(username='cris', password='1234')

        Solicitud.objects.create(
            usuario=self.user,
            tipo_solicitud=self.tipo,
            folio="ABC123"
        )

        response = self.client.get(reverse('mis_solicitudes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABC123")