from django.test import TestCase
from django.contrib.auth.models import User
from tipo_solicitudes.models import (
    TipoSolicitud, FormularioSolicitud, CampoFormulario,
    Solicitud, RespuestaCampo, ArchivoAdjunto
)
from django.core.files.uploadedfile import SimpleUploadedFile


class ModelosSolicitudesTest(TestCase):

    def setUp(self):
        # Usuario
        self.user = User.objects.create_user(username='cris', password='1234')

        # Tipo de solicitud
        self.tipo = TipoSolicitud.objects.create(
            nombre="Constancia",
            descripcion="Constancia de estudios",
            responsable="1"
        )

        # Formulario
        self.formulario = FormularioSolicitud.objects.create(
            tipo_solicitud=self.tipo,
            nombre="Formulario Constancia",
            descripcion="Formulario para solicitar constancia"
        )

        # Campo
        self.campo_texto = CampoFormulario.objects.create(
            formulario=self.formulario,
            nombre="motivo",
            etiqueta="Motivo",
            tipo="text",
            requerido=True
        )

        self.campo_file = CampoFormulario.objects.create(
            formulario=self.formulario,
            nombre="documento",
            etiqueta="Documento",
            tipo="file",
            requerido=False,
            cantidad_archivos=2
        )

    def test_tipo_solicitud_str(self):
        self.assertEqual(str(self.tipo), "Constancia")

    def test_formulario_str(self):
        self.assertEqual(str(self.formulario), "Formulario: Formulario Constancia")

    def test_campo_formulario_str(self):
        self.assertEqual(str(self.campo_texto), "Motivo (text)")

    def test_crear_solicitud(self):
        solicitud = Solicitud.objects.create(
            usuario=self.user,
            tipo_solicitud=self.tipo,
            folio="ABC123"
        )

        self.assertEqual(solicitud.usuario.username, "cris")
        self.assertEqual(solicitud.folio, "ABC123")
        self.assertEqual(solicitud.tipo_solicitud, self.tipo)

    def test_respuesta_campo(self):
        solicitud = Solicitud.objects.create(
            usuario=self.user,
            tipo_solicitud=self.tipo,
            folio="XYZ999"
        )

        respuesta = RespuestaCampo.objects.create(
            solicitud=solicitud,
            campo=self.campo_texto,
            valor="Necesito constancia"
        )

        self.assertEqual(str(respuesta),
                         "Respuesta motivo -> Necesito constancia")

    def test_archivo_adjunto(self):
        solicitud = Solicitud.objects.create(
            usuario=self.user,
            tipo_solicitud=self.tipo,
            folio="FILE001"
        )

        respuesta = RespuestaCampo.objects.create(
            solicitud=solicitud,
            campo=self.campo_file
        )

        archivo = SimpleUploadedFile("prueba.pdf", b"contenido")

        adjunto = ArchivoAdjunto.objects.create(
            solicitud=solicitud,
            respuesta=respuesta,
            archivo=archivo,
            nombre="prueba.pdf"
        )

        self.assertIn("prueba", adjunto.archivo.name)
        self.assertIn(".pdf", adjunto.archivo.name)
        self.assertIn(f"tickets/{solicitud.folio}/", str(adjunto))