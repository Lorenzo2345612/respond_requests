from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tipo_solicitudes.models import (
    Solicitud, TipoSolicitud, SeguimientoSolicitud
)
from django.contrib.auth import get_user_model
from django.test import Client


@given(u'existen varios tipos de solicitud con datos registrados')
def existen_tipos_solicitud_registrados(context):
    SeguimientoSolicitud.objects.all().delete()
    Solicitud.objects.all().delete()
    TipoSolicitud.objects.all().delete()
    User = get_user_model()
    User.objects.filter(email="admin@admin.com").delete()

    admin_password = "test_password_123"
    context.admin_user = User.objects.create_user(
        username="admin", email="admin@admin.com", password=admin_password
    )
    context.admin_password = admin_password

    tipos = ["Soporte", "Mantenimiento", "Consulta", "Incidencia"]
    tipos_objs = []
    for t in tipos:
        tipo_obj, _ = TipoSolicitud.objects.get_or_create(nombre=t)
        tipos_objs.append(tipo_obj)

    for i, tipo_obj in enumerate(tipos_objs):
        for j in range(i + 1):
            solicitud = Solicitud.objects.create(
                usuario=context.admin_user,
                tipo_solicitud=tipo_obj,
                folio=f"FOLIO-{tipo_obj.nombre}-{j+1}"
            )
            SeguimientoSolicitud.objects.create(
                solicitud=solicitud,
                estatus='1',
                observaciones='Seguimiento inicial'
            )


@when(u'ingreso a la página de métricas')
def ingreso_pagina_metricas(context):
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

    context.driver.get("http://127.0.0.1:8000/tipo-solicitud/metricas/")


@then(u'la tabla "Solicitudes por Tipo" debe listar cada tipo con su conteo')
def tabla_solicitudes_por_tipo_lista_conteo(context):
    locator_xpath = (
        "//h5[contains(text(), 'Solicitudes por Tipo')]"
        "/ancestor::div[contains(@class, 'card')]//table"
    )

    table = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, locator_xpath))
    )

    rows = table.find_elements(By.XPATH, ".//tbody/tr")
    resultados = {}

    for row in rows:
        tipo = row.find_element(By.XPATH, ".//td[1]").text.strip()
        # La cantidad esta dentro de un <span> en la segunda celda
        cantidad = row.find_element(By.XPATH, ".//td[2]//span").text.strip()
        cantidad_num = int(''.join(filter(str.isdigit, cantidad)))
        resultados[tipo] = cantidad_num

    esperados = {
        "Soporte": 1,
        "Mantenimiento": 2,
        "Consulta": 3,
        "Incidencia": 4
    }

    assert len(resultados) == len(esperados), (
        f"Se encontraron {len(resultados)} filas pero se esperaban "
        f"{len(esperados)}"
    )

    for tipo, cantidad_esperada in esperados.items():
        assert tipo in resultados, (
            f"No se encontró el tipo '{tipo}' en la tabla"
        )
        assert resultados[tipo] == cantidad_esperada, (
            f"Para el tipo '{tipo}': se esperaba {cantidad_esperada} pero "
            f"se encontró {resultados[tipo]}"
        )
