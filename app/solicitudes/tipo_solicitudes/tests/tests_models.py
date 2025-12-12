from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from tipo_solicitudes.models import (
    TipoSolicitud, FormularioSolicitud, CampoFormulario,
    Solicitud, RespuestaCampo, ArchivoAdjunto, SeguimientoSolicitud
)

# Obtener el modelo de usuario
User = get_user_model()


class TestSmokeTest(TestCase):

    def test_dos_mas_dos(self):
        self.assertEqual(2, 2)

    def test_tres_mas_tres(self):
        self.assertEqual(3, 3)

    def test_insertar_tipo_solicitud_constancia(self):
        tipo = TipoSolicitud.objects.create(
            nombre='Constancia',
            descripcion='Constancia para servicio social'
        )
        self.assertEqual(tipo.nombre, TipoSolicitud.objects.first().nombre)
        # self.assertEqual(1, TipoSolicitud.objects.count())

    def test_cantidad_maxima_caracteres_tipo_solicitud(self):
        tipo = TipoSolicitud(
            nombre='Constancia alsdjasdhasjdk asdkashdkajshdkasdhaksdjhaksdjh askdjahsdka sdakshdakjsd kashdjasdhajs dhasjdhasjkd haskdjhaskjdhaskdhaskjdhaskjdhha ks djasdjhajskd ha skdhasd',
            descripcion='Constancia para servicio social'
        )
        with self.assertRaises(ValidationError):
            tipo.full_clean()

    def test_nombre_requerdio(self):
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

    def test_str_archivo_adjunto(self):
        # Crear usuario
        usuario = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Crear tipo de solicitud
        tipo_solicitud = TipoSolicitud.objects.create(
            nombre='Constancia',
            descripcion='Constancia para servicio social'
        )

        # Crear solicitud con folio
        solicitud = Solicitud.objects.create(
            usuario=usuario,
            tipo_solicitud=tipo_solicitud,
            folio='TEST001'
        )

        # Crear archivo adjunto (usando SimpleUploadedFile para simular archivo)
        from django.core.files.uploadedfile import SimpleUploadedFile
        archivo = SimpleUploadedFile(
            "test.txt",
            b"contenido del archivo"
        )

        archivo_adjunto = ArchivoAdjunto.objects.create(
            solicitud=solicitud,
            archivo=archivo,
            nombre="archivo_test.txt"
        )

        # Verificar que el __str__ funciona
        self.assertEqual(
            str(archivo_adjunto),
            f"Archivo tickets/{solicitud.folio}/{archivo.name}"
        )

    def test_str_seguimiento_solicitud(self):
        # Crear usuario
        usuario = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Crear tipo de solicitud
        tipo_solicitud = TipoSolicitud.objects.create(
            nombre='Constancia',
            descripcion='Constancia para servicio social'
        )

        # Crear solicitud con folio
        solicitud = Solicitud.objects.create(
            usuario=usuario,
            tipo_solicitud=tipo_solicitud,
            folio='TEST002'
        )

        # Crear seguimiento
        seguimiento = SeguimientoSolicitud.objects.create(
            solicitud=solicitud,
            estatus='1',  # Creada
            observaciones='Primer seguimiento'
        )

        # Verificar que el __str__ funciona
        self.assertEqual(
            str(seguimiento),
            f"Seguimiento {solicitud.folio} - Creada"
        )

    def test_seguimiento_con_diferentes_estatus(self):
        """Test para verificar que __str__ funciona con diferentes estatus"""
        # Crear usuario
        usuario = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )

        # Crear tipo de solicitud
        tipo_solicitud = TipoSolicitud.objects.create(
            nombre='Certificado',
            descripcion='Certificado de estudios'
        )

        # Crear solicitud con folio
        solicitud = Solicitud.objects.create(
            usuario=usuario,
            tipo_solicitud=tipo_solicitud,
            folio='TEST003'
        )

        # Probar con diferentes estatus
        estatus_test_cases = [
            ('1', 'Creada'),
            ('2', 'En proceso'),
            ('3', 'Terminada'),
            ('4', 'Cancelada')
        ]

        for estatus_codigo, estatus_display in estatus_test_cases:
            seguimiento = SeguimientoSolicitud.objects.create(
                solicitud=solicitud,
                estatus=estatus_codigo,
                observaciones=f'Seguimiento con estatus {estatus_codigo}'
            )

            self.assertEqual(
                str(seguimiento),
                f"Seguimiento {solicitud.folio} - {estatus_display}"
            )
