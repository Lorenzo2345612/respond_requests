from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from tipo_solicitudes.models import (
    Solicitud, TipoSolicitud, SeguimientoSolicitud
)
from django.contrib.auth import get_user_model
from django.test import Client


@given(u'existen solicitudes en estatus Creada, En proceso y Terminada')
def existen_solicitudes_con_estatus(context):
    Solicitud.objects.all().delete()
    TipoSolicitud.objects.all().delete()
    SeguimientoSolicitud.objects.all().delete()
    User = get_user_model()
    User.objects.filter(email="admin@admin.com").delete()

    admin_password = "test_password_123"
    context.admin_user = User.objects.create_user(
        username="admin", email="admin@admin.com", password=admin_password
    )
    context.admin_password = admin_password

    tipo, _ = TipoSolicitud.objects.get_or_create(nombre="Tipo General")

    estatus_a_crear = {
        '1': 5,  # 5 Creadas
        '2': 3,  # 3 En Proceso
        '3': 2,  # 2 Terminadas
    }

    for estatus, cantidad in estatus_a_crear.items():
        for i in range(cantidad):
            solicitud = Solicitud.objects.create(
                usuario=context.admin_user,
                tipo_solicitud=tipo,
                folio=f"FOLIO-{estatus}-{i}"
            )
            SeguimientoSolicitud.objects.create(
                solicitud=solicitud,
                estatus=estatus,
                observaciones=f"Seguimiento con estatus {estatus}"
            )


@when(u'ingreso al dashboard de métricas')
def ingreso_dashboard_metricas(context):
    """Se loguea y navega a la página de métricas."""
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


@then(u'debo ver una tabla con el conteo agrupado por estatus')
def ver_tabla_conteo_estatus(context):
    """Verifica que la tabla de estatus se muestre correctamente."""
    locator_xpath = (
        "//h5[contains(text(), 'Estatus de Solicitudes')]"
        "/ancestor::div[contains(@class, 'card-header')]"
        "/following-sibling::div//table"
    )

    try:
        table = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, locator_xpath))
        )

        rows = table.find_elements(By.XPATH, ".//tbody/tr")
        assert len(rows) > 0, (
            "No se encontraron filas en la tabla de estatus."
        )

        estatus_vistos = {}
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) == 2:
                estatus = cols[0].find_element(
                    By.TAG_NAME, "span"
                ).text.strip()
                cantidad = int(cols[1].text.strip())
                estatus_vistos[estatus] = cantidad

        expected_counts = {
            "Creada": 5,
            "En proceso": 3,
            "Terminada": 2,
            "Cancelada": 0
        }

        assert len(estatus_vistos) == len(expected_counts), (
            f"Se esperaban {len(expected_counts)} estatus pero se "
            f"encontraron {len(estatus_vistos)}"
        )

        for estatus, count in expected_counts.items():
            assert estatus in estatus_vistos, (
                f"El estatus '{estatus}' no fue encontrado en la tabla."
            )
            assert estatus_vistos[estatus] == count, (
                f"Para '{estatus}', se esperaba {count} pero se encontró "
                f"{estatus_vistos[estatus]}"
            )

    except TimeoutException:
        raise AssertionError(
            "La tabla de estatus no cargó a tiempo o el selector es "
            "incorrecto."
        )
