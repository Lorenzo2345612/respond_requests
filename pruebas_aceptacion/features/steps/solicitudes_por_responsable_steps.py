from behave import given, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Modelos Django
from tipo_solicitudes.models import (
    Solicitud, TipoSolicitud, SeguimientoSolicitud
)
from django.contrib.auth import get_user_model


@given("existen solicitudes asignadas a varios responsables")
def existen_solicitudes_por_responsables(context):
    """Crea varias solicitudes con diferentes responsables para pruebas."""
    # Limpiar datos previos
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

    # Crear tipos de solicitud con distintos responsables
    responsables = ["Ana", "Luis", "Pedro"]
    for idx, resp in enumerate(responsables):
        tipo, _ = TipoSolicitud.objects.get_or_create(
            nombre=f"Tipo {idx+1}", responsable=resp
        )
        # Crear 3 solicitudes por responsable
        for i in range(3):
            solicitud = Solicitud.objects.create(
                usuario=context.admin_user,
                tipo_solicitud=tipo,
                folio=f"FOLIO-{resp}-{i+1}"
            )
            SeguimientoSolicitud.objects.create(
                solicitud=solicitud,
                estatus='1',
                observaciones='Seguimiento inicial'
            )


@then("debo ver una tabla que muestre el responsable y el total asignado")
def ver_tabla_responsables(context):
    """Verifica que la tabla muestre cada responsable con su total."""
    locator_xpath = (
        "//h5[contains(text(), 'Solicitudes por Responsable')]"
        "/ancestor::div[contains(@class, 'card')]//table"
    )

    try:
        table = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, locator_xpath))
        )

        rows = table.find_elements(By.XPATH, ".//tbody/tr")
        assert len(rows) > 0, (
            "No se encontraron filas en la tabla de responsables"
        )

        responsables_vistos = {}
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) == 2:
                responsable = cols[0].text.strip()
                # La cantidad esta dentro de un <span> en la segunda celda
                cantidad_raw = cols[1].find_element(
                    By.TAG_NAME, "span"
                ).text.strip()
                total = int(''.join(filter(str.isdigit, cantidad_raw)))
                responsables_vistos[responsable] = total

        expected_responsables = ["Ana", "Luis", "Pedro"]
        assert len(responsables_vistos) == len(expected_responsables), (
            f"Se esperaban {len(expected_responsables)} responsables pero "
            f"se encontraron {len(responsables_vistos)}"
        )

        for resp in expected_responsables:
            assert resp in responsables_vistos, (
                f"Responsable '{resp}' no aparece en la tabla"
            )
            assert responsables_vistos[resp] == 3, (
                f"Responsable '{resp}' debería tener 3 solicitudes, pero "
                f"tiene {responsables_vistos[resp]}"
            )

    except TimeoutException:
        print(
            f"DEBUG: No se pudo encontrar la tabla con el XPath: "
            f"{locator_xpath}"
        )
        raise AssertionError(
            "La tabla de responsables no cargó a tiempo o el selector es "
            "incorrecto."
        )
