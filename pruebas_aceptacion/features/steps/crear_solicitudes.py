from behave import given, when, then
from django.urls import reverse
from django.contrib.auth.models import User
from tipo_solicitudes.models import (
    TipoSolicitud, FormularioSolicitud, CampoFormulario,
    Solicitud, SeguimientoSolicitud, RespuestaCampo
)
from django.test.client import Client


@given("que el usuario inició sesión")
def step_usuario_login(context):
    context.client = Client()
    context.user = User.objects.create_user(username="cris", password="1234")
    context.client.login(username="cris", password="1234")


@given("existe un tipo de solicitud con formulario")
def step_tipo_solicitud_formulario(context):
    context.tipo = TipoSolicitud.objects.create(
        nombre="Constancia",
        descripcion="Constancia de estudios",
        responsable="1"
    )

    context.formulario = FormularioSolicitud.objects.create(
        tipo_solicitud=context.tipo,
        nombre="Formulario Constancia",
        descripcion="Formulario para solicitar constancia"
    )

    context.campo = CampoFormulario.objects.create(
        formulario=context.formulario,
        nombre="motivo",
        etiqueta="Motivo",
        tipo="text",
        requerido=True
    )


# --- CREAR SOLICITUD ---
@when("llena los campos requeridos y envía el formulario")
def step_usuario_envia_formulario(context):
    url = reverse('crear_solicitud', args=[context.tipo.id])

    context.response = context.client.post(url, {
        'motivo': "Necesito constancia"
    })


@then("la solicitud se guarda exitosamente en la base de datos")
def step_verificar_solicitud_guardada(context):
    assert context.response.status_code == 302
    assert Solicitud.objects.filter(usuario=context.user).count() == 1


# --- LISTAR SOLICITUDES ---
@given("que el usuario tiene solicitudes registradas")
def step_usuario_con_solicitudes(context):
    context.solicitud = Solicitud.objects.create(
        usuario=context.user,
        tipo_solicitud=context.tipo,
        folio="SOLI001"
    )


@when("accede a la pantalla de \"Mis solicitudes\"")
def step_acceder_mis_solicitudes(context):
    url = reverse('mis_solicitudes')
    context.response = context.client.get(url)


@then("puede ver la lista de solicitudes realizadas")
def step_verificar_lista(context):
    assert context.response.status_code == 200
    assert "SOLI001" in context.response.content.decode()


# --- DETALLE DE SOLICITUD ---
@given("que el usuario tiene una solicitud creada")
def step_solicitud_creada(context):
    context.solicitud = Solicitud.objects.create(
        usuario=context.user,
        tipo_solicitud=context.tipo,
        folio="DET001"
    )

    RespuestaCampo.objects.create(
        solicitud=context.solicitud,
        campo=context.campo,
        valor="Motivo de prueba"
    )


@given("existen registros de seguimiento")
def step_registros_seguimiento(context):
    SeguimientoSolicitud.objects.create(
        solicitud=context.solicitud,
        descripcion="Revisando documentos",
        estatus="1"
    )


@when("accede al detalle de la solicitud")
def step_acceder_detalle(context):
    url = reverse('detalle_solicitud', args=[context.solicitud.id])
    context.response = context.client.get(url)


@then("puede ver los campos llenados y el historial de seguimiento")
def step_verificar_detalle(context):
    html = context.response.content.decode()

    # Verificar respuesta del campo
    assert "Motivo de prueba" in html

    # Verificar seguimiento
    assert "Revisando documentos" in html or "Revisando" in html

    assert context.response.status_code == 200
