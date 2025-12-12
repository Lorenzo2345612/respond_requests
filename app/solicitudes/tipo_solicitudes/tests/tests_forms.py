from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from tipo_solicitudes.models import CampoFormulario, RespuestaCampo, Solicitud, TipoSolicitud, FormularioSolicitud
from tipo_solicitudes.forms import FormArchivoAdjunto, FormSolicitud, FormTipoSolicitud, FormFormularioSolicitud, FormCampoFormulario, validar_archivo
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class TestFromTipoSolicitud(TestCase):
    def test_informacion_valida(self):
        Usuario.objects.create_user(
            username='responsable1', email='resp1@test.com', password='password')
        data = {
            'nombre': 'Constancia',
            'descripcion': 'Constancia para servicio social',
            'responsable': Usuario.objects.first().pk
        }
        form = FormTipoSolicitud(data)
        self.assertTrue(form.is_valid())

    def test_nombre_es_requerido(self):
        data = {
            'nombre': '',
            'descripcion': 'Constancia para servicio social',
            'responsable': '2'
        }
        form = FormTipoSolicitud(data)
        self.assertFalse(form.is_valid())

    def test_descripcion_es_requerido(self):
        data = {
            'nombre': 'Constancia',
            'descripcion': '',
            'responsable': '2'
        }
        form = FormTipoSolicitud(data)
        self.assertFalse(form.is_valid())

    def test_nombre_es_requerido_mensaje(self):
        data = {
            'nombre': '',
            'descripcion': 'Constancia para servicio social',
            'responsable': '2'
        }
        form = FormTipoSolicitud(data)
        self.assertEqual(form.errors['nombre'][0],
                         'Este campo es obligatorio.')

    def test_responsable_es_requerido_mensaje(self):
        data = {
            'nombre': 'Constancia',
            'descripcion': 'Constancia para servicio social',
            'responsable': ''
        }
        form = FormTipoSolicitud(data)
        self.assertEqual(form.errors['responsable']
                         [0], 'Este campo es obligatorio.')

    def test_guarda_constancia(self):
        Usuario.objects.create_user(
            username='responsable2', email='resp2@test.com', password='password')
        data = {
            'nombre': 'Constancia',
            'descripcion': 'Constancia para servicio social',
            'responsable': Usuario.objects.first().pk
        }
        form = FormTipoSolicitud(data)
        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(form.data.get('nombre'),
                         TipoSolicitud.objects.first().nombre)


class TestFormFormularioSolicitud(TestCase):
    def setUp(self):
        self.tipo_solicitud = TipoSolicitud.objects.create(
            nombre='Servicio Social',
            descripcion='Solicitud para iniciar servicio social'
        )

    def test_formulario_valido(self):
        data = {
            'tipo_solicitud': self.tipo_solicitud.pk,
            'nombre': 'Formulario Oficial de SS',
            'descripcion': 'Llenar todos los campos con letra legible.'
        }

        form = FormFormularioSolicitud(data=data)
        self.assertTrue(
            form.is_valid(), "El formulario debería ser válido con datos completos.")
        self.assertEqual(form.errors, {})

    def test_formulario_invalido_por_falta_de_nombre(self):
        data = {
            'tipo_solicitud': self.tipo_solicitud.pk,
            'descripcion': 'Instrucciones...'
        }

        form = FormFormularioSolicitud(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_formulario_invalido_por_tipo_solicitud_inexistente(self):
        data = {
            'tipo_solicitud': 9999,
            'nombre': 'Test',
            'descripcion': 'Test'
        }

        form = FormFormularioSolicitud(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('tipo_solicitud', form.errors)


class TestFormCampoFormulario(TestCase):
    def setUp(self):
        self.tipo_solicitud = TipoSolicitud.objects.create(
            nombre='Servicio Social',
            descripcion='Tipo de Solicitud base'
        )

        self.formulario_solicitud = FormularioSolicitud.objects.create(
            tipo_solicitud=self.tipo_solicitud,
            nombre='Formulario para el alumno',
            descripcion='Instrucciones'
        )

        self.valid_data_text = {
            'formulario': self.formulario_solicitud.pk,
            'nombre': 'nombre_alumno',
            'etiqueta': 'Nombre Completo',
            'tipo': 'text',
            'requerido': True,
            'opciones': '',
            'cantidad_archivos': 1,
            'orden': 1
        }

    def test_campo_formulario_valido(self):
        form = FormCampoFormulario(data=self.valid_data_text)
        self.assertTrue(
            form.is_valid(), f"El formulario debería ser válido. Errores: {form.errors}")

    def test_campo_formulario_invalido_por_falta_de_etiqueta(self):
        data = self.valid_data_text.copy()
        del data['etiqueta']

        form = FormCampoFormulario(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('etiqueta', form.errors)

    def test_campo_formulario_valido_con_opciones_para_select(self):
        data = {
            'formulario': self.formulario_solicitud.pk,
            'nombre': 'semestre_select',
            'etiqueta': 'Selecciona tu semestre',
            'tipo': 'select',
            'requerido': True,
            'opciones': 'Primero, Segundo, Tercero, Cuarto',
            'cantidad_archivos': 1,
            'orden': 2
        }

        form = FormCampoFormulario(data=data)
        self.assertTrue(form.is_valid(
        ), f"El formulario 'select' debería ser válido. Errores: {form.errors}")

    def test_campo_formulario_invalido_por_formulario_inexistente(self):
        data = self.valid_data_text.copy()
        data['formulario'] = 9999

        form = FormCampoFormulario(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('formulario', form.errors)

    def test_form_campo_formulario_init_con_formulario(self):
        """Prueba que el __init__ acepta y guarda el parámetro formulario"""
        form = FormCampoFormulario(formulario=self.formulario_solicitud)
        self.assertEqual(form.formulario, self.formulario_solicitud)

    def test_form_campo_formulario_init_sin_formulario(self):
        """Prueba que el __init__ funciona sin el parámetro formulario"""
        form = FormCampoFormulario()
        self.assertIsNone(form.formulario)


class TestFormSolicitud(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            username='testuser', password='password')
        self.tipo_solicitud = TipoSolicitud.objects.create(
            nombre='Viaje',
            descripcion='Solicitud de permiso de viaje',
            responsable=self.user.pk
        )

        self.valid_data = {
            'tipo_solicitud': self.tipo_solicitud.pk,
        }

    def test_solicitud_valida(self):
        form = FormSolicitud(data=self.valid_data)
        self.assertTrue(form.is_valid(),
                        f"Debería ser válido. Errores: {form.errors}")

    def test_solicitud_invalida_por_tipo_solicitud_faltante(self):
        data = {}
        form = FormSolicitud(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('tipo_solicitud', form.errors)

    def test_solicitud_invalida_por_tipo_solicitud_inexistente(self):
        data = {'tipo_solicitud': 9999}
        form = FormSolicitud(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('tipo_solicitud', form.errors)
        self.assertIn('Seleccione una opción válida. La opción seleccionada no es una de las disponibles.',
                      form.errors['tipo_solicitud'][0])

    def test_guardar_solicitud(self):
        form = FormSolicitud(data=self.valid_data)
        self.assertTrue(form.is_valid())

        solicitud = form.save(commit=False)
        solicitud.usuario = self.user
        solicitud.folio = 'TEST-001'
        solicitud.save()

        self.assertEqual(Solicitud.objects.count(), 1)
        self.assertEqual(Solicitud.objects.first(
        ).tipo_solicitud, self.tipo_solicitud)


class TestFormRespuestaCampo(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(username='testuser2')
        self.tipo_solicitud = TipoSolicitud.objects.create(nombre='Test')
        self.solicitud = Solicitud.objects.create(
            usuario=self.user,
            tipo_solicitud=self.tipo_solicitud,
            folio='RESP-001'
        )
        self.formulario = FormularioSolicitud.objects.create(
            tipo_solicitud=self.tipo_solicitud,
            nombre='Formulario Test'
        )
        self.campo = CampoFormulario.objects.create(
            formulario=self.formulario,
            nombre='matricula',
            etiqueta='Matrícula',
            tipo='text'
        )

    def test_respuesta_campo_valida(self):
        data = {'valor': 'S12345'}
        form = FormRespuestaCampo(data=data)
        self.assertTrue(form.is_valid())

    def test_respuesta_campo_valida_con_valor_vacio(self):
        data = {'valor': ''}
        form = FormRespuestaCampo(data=data)
        self.assertTrue(form.is_valid())

    def test_guardar_respuesta_campo(self):
        data = {'valor': 'Respuesta de prueba'}
        form = FormRespuestaCampo(data=data)
        self.assertTrue(form.is_valid())

        respuesta = form.save(commit=False)
        respuesta.solicitud = self.solicitud
        respuesta.campo = self.campo
        respuesta.save()

        self.assertEqual(RespuestaCampo.objects.count(), 1)
        self.assertEqual(RespuestaCampo.objects.first().valor,
                         'Respuesta de prueba')


class TestFormSeguimientoSolicitud(TestCase):
    def test_seguimiento_valido(self):
        data = {
            'observaciones': 'Documentos recibidos y revisados.',
            'estatus': '2'
        }
        form = FormSeguimientoSolicitud(data=data)
        self.assertTrue(form.is_valid())

    def test_seguimiento_valido_con_observaciones_vacias(self):
        data = {
            'observaciones': '',
            'estatus': '3'
        }
        form = FormSeguimientoSolicitud(data=data)
        self.assertTrue(form.is_valid())

    def test_seguimiento_invalido_por_estatus_faltante(self):
        data = {'observaciones': 'Test'}
        form = FormSeguimientoSolicitud(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('estatus', form.errors)

    def test_seguimiento_invalido_por_estatus_invalido(self):
        data = {
            'observaciones': 'Test',
            'estatus': '5'
        }
        form = FormSeguimientoSolicitud(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('estatus', form.errors)
        self.assertIn(
            'Seleccione una opción válida. 5 no es una de las opciones disponibles.', form.errors['estatus'][0])


class TestFormArchivoAdjunto(TestCase):
    def setUp(self):
        self.file_content = b'Contenido de prueba'
        self.test_file = SimpleUploadedFile(
            "test_doc.pdf",
            self.file_content,
            content_type="application/pdf"
        )

        self.valid_data = {
            'nombre': 'Constancia de Bachiller'
        }
        self.valid_files = {
            'archivo': self.test_file
        }

    def test_archivo_adjunto_valido(self):
        form = FormArchivoAdjunto(data=self.valid_data, files=self.valid_files)
        self.assertTrue(form.is_valid(),
                        f"Debería ser válido. Errores: {form.errors}")

    def test_archivo_adjunto_invalido_sin_archivo(self):
        form = FormArchivoAdjunto(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('archivo', form.errors)

    def test_archivo_adjunto_valido_sin_nombre(self):
        data = {}
        form = FormArchivoAdjunto(data=data, files=self.valid_files)
        self.assertTrue(
            form.is_valid(), f"Debería ser válido sin nombre. Errores: {form.errors}")

    def test_guardar_archivo_adjunto(self):
        form = FormArchivoAdjunto(data=self.valid_data, files=self.valid_files)
        self.assertTrue(form.is_valid())

        archivo_adjunto = form.save(commit=False)
        user = Usuario.objects.create_user(username='archiver')
        tipo = TipoSolicitud.objects.create(nombre='Archiv')
        solicitud = Solicitud.objects.create(
            usuario=user, tipo_solicitud=tipo, folio='FILE-001')

        archivo_adjunto.solicitud = solicitud
        archivo_adjunto.save()

        self.assertEqual(archivo_adjunto.nombre, 'Constancia de Bachiller')
        self.assertIsNotNone(archivo_adjunto.archivo)


class TestValidarArchivo(TestCase):
    """Pruebas para la función validar_archivo() de forms.py"""

    def setUp(self):
        # Archivo válido PDF pequeño (1MB)
        self.pdf_valido = SimpleUploadedFile(
            "documento.pdf",
            b'x' * (1024 * 1024),  # 1MB
            content_type="application/pdf"
        )

        # Archivo válido JPG pequeño
        self.jpg_valido = SimpleUploadedFile(
            "imagen.jpg",
            b'x' * (500 * 1024),  # 500KB
            content_type="image/jpeg"
        )

        # Archivo válido PNG pequeño
        self.png_valido = SimpleUploadedFile(
            "imagen.png",
            b'x' * (300 * 1024),  # 300KB
            content_type="image/png"
        )

        # Archivo válido GIF pequeño
        self.gif_valido = SimpleUploadedFile(
            "imagen.gif",
            b'x' * (200 * 1024),  # 200KB
            content_type="image/gif"
        )

        # Archivo válido JPEG (variante de jpg)
        self.jpeg_valido = SimpleUploadedFile(
            "imagen.jpeg",
            b'x' * (400 * 1024),  # 400KB
            content_type="image/jpeg"
        )

        # Archivo exactamente en el límite de 2MB
        self.archivo_limite_2mb = SimpleUploadedFile(
            "limite.pdf",
            b'x' * (2 * 1024 * 1024),  # Exactamente 2MB
            content_type="application/pdf"
        )

        # Archivo que excede 2MB
        self.archivo_muy_grande = SimpleUploadedFile(
            "grande.pdf",
            b'x' * (3 * 1024 * 1024),  # 3MB
            content_type="application/pdf"
        )

        # Archivo con extensión inválida
        self.archivo_invalido_ext = SimpleUploadedFile(
            "documento.doc",
            b'x' * (500 * 1024),  # 500KB
            content_type="application/msword"
        )

        # Archivo con extensión inválida (txt)
        self.archivo_txt = SimpleUploadedFile(
            "documento.txt",
            b'x' * (100 * 1024),  # 100KB
            content_type="text/plain"
        )

    def test_validar_archivo_pdf_valido(self):
        """Prueba que un archivo PDF válido pasa la validación"""
        resultado = validar_archivo(self.pdf_valido)
        self.assertEqual(resultado, self.pdf_valido)

    def test_validar_archivo_jpg_valido(self):
        """Prueba que un archivo JPG válido pasa la validación"""
        resultado = validar_archivo(self.jpg_valido)
        self.assertEqual(resultado, self.jpg_valido)

    def test_validar_archivo_jpeg_valido(self):
        """Prueba que un archivo JPEG válido pasa la validación"""
        resultado = validar_archivo(self.jpeg_valido)
        self.assertEqual(resultado, self.jpeg_valido)

    def test_validar_archivo_png_valido(self):
        """Prueba que un archivo PNG válido pasa la validación"""
        resultado = validar_archivo(self.png_valido)
        self.assertEqual(resultado, self.png_valido)

    def test_validar_archivo_gif_valido(self):
        """Prueba que un archivo GIF válido pasa la validación"""
        resultado = validar_archivo(self.gif_valido)
        self.assertEqual(resultado, self.gif_valido)

    def test_validar_archivo_limite_2mb(self):
        """Prueba que un archivo exactamente en el límite de 2MB pasa la validación"""
        resultado = validar_archivo(self.archivo_limite_2mb)
        self.assertEqual(resultado, self.archivo_limite_2mb)

    def test_validar_archivo_excede_2mb(self):
        """Prueba que un archivo que excede 2MB lanza ValidationError"""
        with self.assertRaises(ValidationError) as context:
            validar_archivo(self.archivo_muy_grande)

        error_message = str(context.exception)
        self.assertIn('demasiado grande', error_message)
        self.assertIn('2MB', error_message)

    def test_validar_archivo_extension_invalida_doc(self):
        """Prueba que un archivo con extensión .doc lanza ValidationError"""
        with self.assertRaises(ValidationError) as context:
            validar_archivo(self.archivo_invalido_ext)

        error_message = str(context.exception)
        self.assertIn('Tipo de archivo no permitido', error_message)
        self.assertIn('.doc', error_message)
        self.assertIn('PDF, JPG, JPEG, PNG, GIF', error_message)

    def test_validar_archivo_extension_invalida_txt(self):
        """Prueba que un archivo con extensión .txt lanza ValidationError"""
        with self.assertRaises(ValidationError) as context:
            validar_archivo(self.archivo_txt)

        error_message = str(context.exception)
        self.assertIn('Tipo de archivo no permitido', error_message)
        self.assertIn('.txt', error_message)

    def test_validar_archivo_extension_case_insensitive(self):
        """Prueba que la validación de extensión es case-insensitive"""
        # Archivo con extensión en mayúsculas
        archivo_pdf_mayusculas = SimpleUploadedFile(
            "DOCUMENTO.PDF",
            b'x' * (500 * 1024),
            content_type="application/pdf"
        )
        resultado = validar_archivo(archivo_pdf_mayusculas)
        self.assertEqual(resultado, archivo_pdf_mayusculas)

        # Archivo con extensión mixta
        archivo_jpg_mixto = SimpleUploadedFile(
            "IMAGEN.JpG",
            b'x' * (300 * 1024),
            content_type="image/jpeg"
        )
        resultado = validar_archivo(archivo_jpg_mixto)
        self.assertEqual(resultado, archivo_jpg_mixto)

    def test_validar_archivo_mensaje_error_tamaño_incluye_nombre(self):
        """Prueba que el mensaje de error de tamaño incluye el nombre del archivo"""
        with self.assertRaises(ValidationError) as context:
            validar_archivo(self.archivo_muy_grande)

        error_message = str(context.exception)
        self.assertIn('grande.pdf', error_message)

    def test_validar_archivo_mensaje_error_tamaño_muestra_mb(self):
        """Prueba que el mensaje de error muestra el tamaño en MB"""
        with self.assertRaises(ValidationError) as context:
            validar_archivo(self.archivo_muy_grande)

        error_message = str(context.exception)
        # Debería mostrar algo como "3.00MB" o similar
        self.assertIn('MB', error_message)
