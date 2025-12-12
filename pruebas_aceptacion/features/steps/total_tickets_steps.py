from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tipo_solicitudes.models import (
    Solicitud, TipoSolicitud, SeguimientoSolicitud
)
from django.contrib.auth import get_user_model
from django.test import Client


@given("existen 10 solicitudes registradas")
def existen_10_solicitudes_registradas(context):
    User = get_user_model()
    # Limpiar para asegurar un estado limpio
    Solicitud.objects.all().delete()
    TipoSolicitud.objects.all().delete()
    User.objects.filter(email="admin@admin.com").delete()

    admin_password = "test_password_123"
    context.admin_user = User.objects.create_user(
        username="admin", email="admin@admin.com", password=admin_password
    )
    context.admin_password = admin_password

    tipo, _ = TipoSolicitud.objects.get_or_create(nombre="Tipo Test")

    for i in range(10):
        solicitud = Solicitud.objects.create(
            usuario=context.admin_user,
            tipo_solicitud=tipo,
            folio=f"FOLIO-{i+1}"
        )
        SeguimientoSolicitud.objects.create(
            solicitud=solicitud,
            estatus='1',  # Creada
            observaciones='Seguimiento inicial'
        )


@when("ingreso a la página de listar solicitudes")
def ingreso_pagina_listar_solicitudes(context):
    client = Client()
    login_successful = client.login(
        username="admin", password=context.admin_password
    )
    assert login_successful, (
        "El inicio de sesión en el backend de Django falló."
    )

    session_cookie = client.cookies['sessionid']

    context.driver.get("http://127.0.0.1:8000/solicitudes/")
    context.driver.add_cookie({
        'name': 'sessionid',
        'value': session_cookie.value,
        'path': '/',
        'domain': '127.0.0.1'
    })

    context.driver.get("http://127.0.0.1:8000/solicitudes/listar/")


@then('debe mostrarse el número "{expected_number}" en el filtro '
      '"{filter_name}"')
def mostrar_numero_en_filtro(context, expected_number, filter_name):
    filter_id = f"btn-{filter_name.lower()}"
    locator_css = f"#{filter_id} span.badge"

    total_element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, locator_css))
    )
    assert total_element.text == expected_number, (
        f"El número esperado era {expected_number} pero se encontró "
        f"{total_element.text}"
    )
