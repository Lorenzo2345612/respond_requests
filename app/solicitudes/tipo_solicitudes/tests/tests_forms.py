from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django import forms  # Necesario para ValidationError y HiddenInput

# Ajusta la ruta de importación si tus modelos y forms están en una app diferente
from tipo_solicitudes.models import (
    CampoFormulario, RespuestaCampo, Solicitud,
    TipoSolicitud, FormularioSolicitud)
from tipo_solicitudes.forms import (
    FormArchivoAdjunto, FormRespuestaCampo, FormSeguimientoSolicitud,
    FormSolicitud, FormTipoSolicitud, FormFormularioSolicitud,
    FormCampoFormulario)

Usuario = get_user_model()


class TestFromTipoSolicitud(TestCase):
    def test_informacion_valida(self):
        Usuario.objects.create_user(
            username='responsable1',
            email='resp1@test.com',
            password='password'
        )
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
        self.assertEqual(
            form.errors['nombre'][0],
            'Este campo es obligatorio.'
        )

    def test_responsable_es_requerido_mensaje(self):
        data = {
            'nombre': 'Constancia',
            'descripcion': 'Constancia para servicio social',
            'responsable': ''
        }
        form = FormTipoSolicitud(data)
        self.assertEqual(
            form.errors['responsable'][0],
            'Este campo es obligatorio.'
        )

    def test_guarda_constancia(self):
        Usuario.objects.create_user(
            username='responsable2',
            email='resp2@test.com',
            password='password'
        )
        data = {
            'nombre': 'Constancia',
            'descripcion': 'Constancia para servicio social',
            'responsable': Usuario.objects.first().pk
        }
        form = FormTipoSolicitud(data)
        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(
            form.data.get('nombre'),
            TipoSolicitud.objects.first().nombre
        )


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
            form.is_valid(),
            "El formulario debería ser válido con datos completos."
        )
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

    # --- Cobertura del método __init__ ---
    def test_init_con_argumento_formulario(self):
        form = FormCampoFormulario(formulario=self.formulario_solicitud)

        self.assertEqual(form.formulario, self.formulario_solicitud)
        self.assertFalse(form.fields['formulario'].required)
        self.assertIsInstance(
            form.fields['formulario'].widget, forms.HiddenInput
        )

    def test_campo_formulario_valido(self):
        form = FormCampoFormulario(data=self.valid_data_text)
        self.assertTrue(
            form.is_valid(),
            f"El formulario debería ser válido. Errores: {form.errors}"
        )

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
        self.assertTrue(
            form.is_valid(),
            f"El formulario 'select' debe ser válido. Errores: {form.errors}"
        )

    def test_campo_formulario_invalido_por_formulario_inexistente(self):
        data = self.valid_data_text.copy()
        data['formulario'] = 9999

        form = FormCampoFormulario(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('formulario', form.errors)

    # --- Cobertura del método clean_orden ---
    def test_clean_orden_duplicado_en_creacion_falla(self):
        CampoFormulario.objects.create(
            formulario=self.formulario_solicitud,
            nombre='otro_campo',
            etiqueta='Otro',
            tipo='text',
            orden=1
        )
        data = self.valid_data_text.copy()  # Ya tiene orden=1

        form = FormCampoFormulario(
            data=data, formulario=self.formulario_solicitud
        )

        self.assertFalse(form.is_valid())
        self.assertIn('orden', form.errors)
        self.assertIn(
            "Ese número de orden ya está en uso",
            form.errors['orden'][0]
        )

    def test_clean_orden_permitido_en_edicion(self):
        campo_existente = CampoFormulario.objects.create(
            formulario=self.formulario_solicitud,
            nombre='campo_a_editar',
            etiqueta='Editar',
            tipo='text',
            orden=1,
            requerido=True,
            cantidad_archivos=1
        )

        data = {
            'formulario': self.formulario_solicitud.pk,
            'nombre': 'campo_editado',
            'etiqueta': 'Etiqueta Editada',
            'tipo': 'text',
            'requerido': True,
            'opciones': '',
            'cantidad_archivos': 1,
            'orden': 1
        }

        form = FormCampoFormulario(
            data=data,
            instance=campo_existente,
            formulario=self.formulario_solicitud
        )

        if not form.is_valid():
            print(f"Errores de validación: {form.errors}")

        self.assertTrue(
            form.is_valid(),
            f"Debe ser válido al editarse a sí mismo. Errores: {form.errors}"
        )

    def test_clean_orden_vacio_pasa(self):
        data = self.valid_data_text.copy()
        data['orden'] = None  # Permite que pase la primera línea clean_orden

        form = FormCampoFormulario(data=data)
        self.assertTrue(form.is_valid())

    # --- Cobertura del método clean ---
    def test_clean_select_sin_opciones_falla(self):
        data = self.valid_data_text.copy()
        data['tipo'] = 'select'
        data['opciones'] = ''

        form = FormCampoFormulario(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn(
            "Debes agregar opciones separadas por comas para un campo select.",
            form.errors['__all__'][0]
        )

    def test_clean_file_con_cantidad_cero_falla(self):
        data = self.valid_data_text.copy()
        data['tipo'] = 'file'
        data['cantidad_archivos'] = 0

        form = FormCampoFormulario(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn(
            "Debe permitir al menos 1 archivo.",
            form.errors['__all__'][0]
        )

    def test_clean_file_sin_cantidad_falla(self):
        data = self.valid_data_text.copy()
        data['tipo'] = 'file'
        # Quitar el campo para simular que no viene en POST
        del data['cantidad_archivos']

        form = FormCampoFormulario(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn(
            "Debe permitir al menos 1 archivo.",
            form.errors['__all__'][0]
        )


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
        self.assertTrue(
            form.is_valid(),
            f"Debería ser válido. Errores: {form.errors}"
        )

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
        self.assertIn(
            'Seleccione una opción válida. La opción seleccionada no es una '
            'de las disponibles.',
            form.errors['tipo_solicitud'][0]
        )

    def test_guardar_solicitud(self):
        form = FormSolicitud(data=self.valid_data)
        self.assertTrue(form.is_valid())

        solicitud = form.save(commit=False)
        solicitud.usuario = self.user
        solicitud.folio = 'TEST-001'
        solicitud.save()

        self.assertEqual(Solicitud.objects.count(), 1)
        self.assertEqual(
            Solicitud.objects.first().tipo_solicitud,
            self.tipo_solicitud
        )


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
        self.assertEqual(
            RespuestaCampo.objects.first().valor,
            'Respuesta de prueba'
        )


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
            'Seleccione una opción válida. 5 no es una de las opciones '
            'disponibles.',
            form.errors['estatus'][0]
        )


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
        self.assertTrue(
            form.is_valid(),
            f"Debería ser válido. Errores: {form.errors}"
        )

    def test_archivo_adjunto_invalido_sin_archivo(self):
        form = FormArchivoAdjunto(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('archivo', form.errors)

    def test_archivo_adjunto_valido_sin_nombre(self):
        data = {}
        form = FormArchivoAdjunto(data=data, files=self.valid_files)
        self.assertTrue(
            form.is_valid(),
            f"Debería ser válido sin nombre. Errores: {form.errors}"
        )

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
