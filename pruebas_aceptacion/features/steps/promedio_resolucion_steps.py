from behave import given, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from tipo_solicitudes.models import Solicitud, TipoSolicitud, SeguimientoSolicitud
from django.contrib.auth import get_user_model
from datetime import timedelta


@given('existen solicitudes con tiempos de resolución calculables')
def existen_solicitudes_calculables(context):
    """Crea solicitudes completadas con fechas de creación y resolución para calcular promedio."""
    Solicitud.objects.all().delete()
    TipoSolicitud.objects.all().delete()

    User = get_user_model()
    User.objects.filter(email="admin@admin.com").delete()

    admin_password = "test_password_123"
    context.admin_user = User.objects.create_user(
        username="admin", email="admin@admin.com", password=admin_password
    )
    context.admin_password = admin_password

    tipo, _ = TipoSolicitud.objects.get_or_create(nombre="Tipo Test")

    from django.utils import timezone
    now = timezone.now()

    for i in range(3):
        solicitud = Solicitud.objects.create(
            usuario=context.admin_user,
            tipo_solicitud=tipo,
            folio=f"RES-{i+1}"
        )
        # Crear seguimiento inicial (creada)
        SeguimientoSolicitud.objects.create(
            solicitud=solicitud,
            estatus='1',
            observaciones='Creada',
            fecha_creacion=now - timedelta(hours=i+1)
        )
        # Crear seguimiento de terminada con fecha_terminacion
        seguimiento_terminado = SeguimientoSolicitud.objects.create(
            solicitud=solicitud,
            estatus='3',
            observaciones='Terminada',
            fecha_creacion=now - timedelta(minutes=i*10)
        )
        # Establecer fecha_terminacion manualmente
        seguimiento_terminado.fecha_terminacion = now - timedelta(minutes=i*10)
        seguimiento_terminado.save()


@given('no existen solicitudes completadas')
def no_existen_solicitudes_completadas(context):
    """Asegura que no haya solicitudes completadas en la DB."""
    Solicitud.objects.all().delete()
    TipoSolicitud.objects.all().delete()

    User = get_user_model()
    User.objects.filter(email="admin@admin.com").delete()
    admin_password = "test_password_123"
    context.admin_user = User.objects.create_user(
        username="admin", email="admin@admin.com", password=admin_password
    )
    context.admin_password = admin_password


@then('se debe mostrar un valor numérico en "Promedio Resolución"')
def mostrar_valor_numerico_promedio(context):
    """Verifica que el span 'promedio-resolucion' muestre un valor numérico."""
    try:
        total_span = WebDriverWait(context.driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#promedio-resolucion span"))
        )
        text = total_span.text.strip()
        # El formato puede ser: "0s", "1min 30s", "2h 15min", "3d 5h"
        assert text and text != "Sin datos", f"No se encontró valor o está vacío: {text}"
    except TimeoutException:
        raise AssertionError(
            "El elemento 'Promedio Resolución' no apareció a tiempo.")


@then('debe mostrarse "Pendiente" en "Promedio Resolución"')
def mostrar_pendiente_promedio(context):
    """Verifica que el span muestre 'Sin datos' si no hay solicitudes completadas."""
    try:
        total_span = WebDriverWait(context.driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#promedio-resolucion span"))
        )
        text = total_span.text.strip()
        assert text == "Sin datos", f"Se esperaba 'Sin datos' pero se encontró '{text}'"
    except TimeoutException:
        raise AssertionError(
            "El elemento 'Promedio Resolución' no apareció a tiempo.")
