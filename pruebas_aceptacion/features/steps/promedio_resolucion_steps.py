from behave import given, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from tipo_solicitudes.models import Solicitud, TipoSolicitud, SeguimientoSolicitud
from django.contrib.auth import get_user_model
from django.test import Client
from datetime import datetime, timedelta

@given('existen solicitudes con tiempos de resolución calculables')
def step_impl(context):
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

    now = datetime.now()
    for i in range(3):
        solicitud = Solicitud.objects.create(
            usuario=context.admin_user,
            tipo_solicitud=tipo,
            folio=f"RES-{i+1}",
            fecha_creacion=now - timedelta(hours=i+1),
            estatus='3'
        )
        SeguimientoSolicitud.objects.create(
            solicitud=solicitud,
            estatus='3',
            fecha_creacion=now - timedelta(minutes=i*10)
        )

@given('no existen solicitudes completadas')
def step_impl(context):
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
def step_impl(context):
    """Verifica que el span 'promedio-resolucion' muestre un valor numérico."""
    try:
        total_span = WebDriverWait(context.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#promedio-resolucion span"))
        )
        text = total_span.text.strip()
        import re
        assert re.match(r"\d+:\d{2}:00", text), f"El valor no es numérico o no tiene el formato hh:mm:00: {text}"
    except TimeoutException:
        raise AssertionError("El elemento 'Promedio Resolución' no apareció a tiempo.")

@then('debe mostrarse "Pendiente" en "Promedio Resolución"')
def step_impl(context):
    """Verifica que el span muestre 'Pendiente' si no hay solicitudes completadas."""
    try:
        total_span = WebDriverWait(context.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#promedio-resolucion span"))
        )
        text = total_span.text.strip()
        assert text == "Pendiente", f"Se esperaba 'Pendiente' pero se encontró '{text}'"
    except TimeoutException:
        raise AssertionError("El elemento 'Promedio Resolución' no apareció a tiempo.")
