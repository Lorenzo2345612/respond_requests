from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from tipo_solicitudes.models import (
    TipoSolicitud, 
    FormularioSolicitud, 
    CampoFormulario, 
    Solicitud, 
    RespuestaCampo, 
    ArchivoAdjunto
)

class TestSmokeTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='password')
        
        self.tipo_solicitud = TipoSolicitud.objects.create(
            nombre='Constancia',
            descripcion='Constancia para servicio social'
        )
        
        self.formulario = FormularioSolicitud.objects.create(
            tipo_solicitud=self.tipo_solicitud,
            nombre='Formulario General'
        )
        
        self.solicitud = Solicitud.objects.create(
            usuario=self.user,
            tipo_solicitud=self.tipo_solicitud,
            folio='FOL-2023-001'
        )

    def test_dos_mas_dos(self):
        self.assertEqual(2, 2)

    def test_tres_mas_tres(self):
        self.assertEqual(3, 3)

    def test_insertar_tipo_solicitud_constancia(self):
        self.assertEqual(self.tipo_solicitud.nombre, TipoSolicitud.objects.first().nombre)

    def test_cantidad_maxima_caracteres_tipo_solicitud(self):
        tipo = TipoSolicitud(
            nombre='Constancia alsdjasdhasjdk asdkashdkajshdkasdhaksdjhaksdjh askdjahsdka sdakshdakjsd kashdjasdhajs dhasjdhasjkd haskdjhaskjdhaskdhaskjdhaskjdhha ks djasdjhajskd ha skdhasd',
            descripcion='Constancia para servicio social'
        )
        with self.assertRaises(ValidationError):
            tipo.full_clean()

    def test_nombre_requerido(self):
        tipo = TipoSolicitud(
            nombre='',
            descripcion='Constancia para servicio social'
        )
        with self.assertRaises(ValidationError):
            tipo.full_clean()

    def test_mensaje_error_requerido(self):
        tipo = TipoSolicitud(
            nombre='',
            descripcion='Constancia para servicio social'
        )
        try:
            tipo.full_clean()
        except ValidationError as ex:
            msg = ex.message_dict['nombre'][0]
            self.assertEqual('Este campo no puede estar en blanco.', msg)

    def test_cantidad_maxima_caracteres_mensaje(self):
        tipo = TipoSolicitud(
            nombre='Constancia alsdjasdhasjdk asdkashdkajshdkasdhaksdjhaksdjh askdjahsdka sdakshdakjsd kashdjasdhajs dhasjdhasjkd haskdjhaskjdhaskdhaskjdhaskjdhha ks djasdjhajskd ha skdhasd',
            descripcion='Constancia para servicio social'
        )
        try:
            tipo.full_clean()
        except ValidationError as ex:
            msg = ex.message_dict['nombre'][0]
            self.assertEqual(
                'Asegúrese de que este valor tenga como máximo 150 caracteres (tiene 169).', msg)

    def test_str_tipo_solicitud(self):
        self.assertEqual(str(self.tipo_solicitud), 'Constancia')

    def test_str_formulario_solicitud(self):
        self.assertEqual(str(self.formulario), 'Formulario: Formulario General')

    def test_str_campo_formulario(self):
        campo = CampoFormulario.objects.create(
            formulario=self.formulario,
            nombre='edad',
            etiqueta='Tu Edad',
            tipo='number'
        )
        self.assertEqual(str(campo), 'Tu Edad (number)')

    def test_str_solicitud(self):
        self.assertEqual(str(self.solicitud), 'FOL-2023-001')

    def test_str_respuesta_campo(self):
        campo = CampoFormulario.objects.create(
            formulario=self.formulario,
            nombre='nombre_completo',
            etiqueta='Nombre',
            tipo='text'
        )
        respuesta = RespuestaCampo.objects.create(
            solicitud=self.solicitud,
            campo=campo,
            valor='Juan Perez'
        )
        self.assertEqual(str(respuesta), 'Respuesta nombre_completo -> Juan Perez')

    def test_str_archivo_adjunto(self):
        archivo_dummy = SimpleUploadedFile("test_file.pdf", b"file_content")
        
        adjunto = ArchivoAdjunto.objects.create(
            solicitud=self.solicitud,
            archivo=archivo_dummy,
            nombre='Documento Prueba'
        )
        self.assertTrue(str(adjunto).startswith('Archivo tickets/FOL-2023-001/test_file'))