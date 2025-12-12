from behave import then
from selenium.webdriver.common.by import By
import re

from .utils import parse_time_hms_to_minutes


@then(u'debería ver el título "{title}"')
def ver_titulo(context, title):
    # busca un h1 con el texto esperado
    try:
        h1 = context.driver.find_element(By.TAG_NAME, 'h1').text
    except Exception:
        h1 = context.driver.find_element(
            By.TAG_NAME, 'body').text.split('\n')[0]
    assert title in h1, f"Título esperado '{title}' no encontrado en '{h1}'"


@then(u'debería ver la línea que muestra "Total de tickets"')
def ver_total_tickets(context):
    body = context.driver.find_element(By.TAG_NAME, 'body').text
    assert 'Total de tickets' in body, (
        f"No se encontró 'Total de tickets' en la página: {body[:200]}"
    )


@then(u'debería ver la sección "{section}"')
def ver_seccion(context, section):
    # buscamos h3 con ese texto
    elems = context.driver.find_elements(By.TAG_NAME, 'h3')
    texts = [e.text for e in elems]
    assert section in texts, (
        f"Sección '{section}' no encontrada. Secciones: {texts}"
    )


@then(u'debería existir un elemento con id "{elem_id}"')
def elemento_existe(context, elem_id):
    el = context.driver.find_element(By.ID, elem_id)
    assert el is not None, f"Elemento con id '{elem_id}' no encontrado"


@then(u'debería ser redirigido a la página de login o ver un mensaje '
      u'de acceso denegado')
def redirigido_a_login(context):
    # Comprobar URL o texto que indique acceso denegado
    current = context.driver.current_url
    body = context.driver.find_element(By.TAG_NAME, 'body').text.lower()
    if '/accounts/login' in current or 'login' in current:
        return
    denied_keywords = [
        'denegado', 'acceso denegado', 'no tienes permiso',
        'not authorized', 'forbidden', '403'
    ]
    assert any(k in body for k in denied_keywords), (
        f"No redirigido a login ni encontrado mensaje de denegación. "
        f"URL: {current} Texto: {body[:200]}"
    )


@then(u'el texto junto a "Total de tickets" debería contener un número')
def total_tickets_contiene_numero(context):
    body = context.driver.find_element(By.TAG_NAME, 'body').text
    m = re.search(r'Total de tickets\s*[:]?\s*(\d+)', body)
    assert m is not None, (
        f"No se encontró un número después de 'Total de tickets' "
        f"en: {body[:200]}"
    )


@then(u'la tabla de "Solicitudes por tipo" debería contener al menos '
      u'una fila o el texto "No hay solicitudes"')
def tabla_solicitudes_por_tipo(context):
    # Intentamos seleccionar la tabla que sigue al h3 'Solicitudes por tipo'
    try:
        xpath = (
            "//h3[normalize-space()='Solicitudes por tipo']"
            "/following-sibling::table[1]"
        )
        table = context.driver.find_element(By.XPATH, xpath)
        rows = table.find_elements(By.TAG_NAME, 'tr')
        # descontar la fila de encabezado
        if len(rows) - 1 >= 1:
            return
    except Exception:
        pass
    body = context.driver.find_element(By.TAG_NAME, 'body').text
    assert 'No hay solicitudes' in body, (
        f"La tabla no contiene filas y no se encontró 'No hay solicitudes'. "
        f"Texto de la página: {body[:200]}"
    )


@then(u'el campo "Total de tickets" debería ser "{expected}"')
def total_tickets_exacto(context, expected):
    body = context.driver.find_element(By.TAG_NAME, 'body').text
    m = re.search(r'Total de tickets\s*[:]?[\s]*(\d+)', body)
    assert m is not None, (
        f"No se encontró 'Total de tickets' en la página: {body[:200]}"
    )
    actual = m.group(1)
    assert str(actual) == str(expected), (
        f"Total de tickets esperado {expected} pero se encontró {actual}"
    )


@then(u'el campo "En proceso" debería ser "{expected}"')
def en_proceso_exacto(context, expected):
    # Buscamos la frase 'En proceso' seguida de número
    body = context.driver.find_element(By.TAG_NAME, 'body').text
    m = re.search(r'[Ee]n proceso\s*[:]?[\s]*(\d+)', body)
    if m:
        actual = m.group(1)
        assert str(actual) == str(expected), (
            f"En proceso esperado {expected} pero se encontró {actual}"
        )
        return
    # Si no se encuentra, falla con pista para preparar la plantilla
    raise AssertionError(
        "No se encontró el elemento 'En proceso' en la página. "
        "Asegúrate de que la plantilla muestra 'En proceso: <n>' o "
        "ajusta el selector"
    )


@then(u'el campo "Promedio de tiempo de resolución" debería ser '
      u'"{expected}"')
def promedio_resolucion_exacto(context, expected):
    body = context.driver.find_element(By.TAG_NAME, 'body').text
    # buscamos la línea que contiene 'Promedio de tiempo de resolución:'
    m = re.search(
        r'Promedio de tiempo de resolución\s*[:]?[\s]*([\d:\sapmAPM]+)',
        body
    )
    assert m is not None, (
        f"No se encontró 'Promedio de tiempo de resolución' en la página. "
        f"Texto: {body[:200]}"
    )
    actual_raw = m.group(1).strip()
    # Si el esperado es un formato H:M:S o H:M, compararemos en minutos
    parsed_expected = parse_time_hms_to_minutes(expected)
    parsed_actual = parse_time_hms_to_minutes(actual_raw)
    if parsed_expected is not None and parsed_actual is not None:
        # tolerancia de 5 minutos
        diff = abs(parsed_actual - parsed_expected)
        assert diff <= 5, (
            f"Promedio esperado ~{parsed_expected} min, "
            f"actual {parsed_actual} min (diferencia {diff} min)"
        )
    else:
        # fallback a comparación de strings
        assert actual_raw == expected, (
            f"Promedio esperado '{expected}' pero se encontró "
            f"'{actual_raw}'"
        )


@then(u'la fila para el responsable "{name}" debería mostrar "{count}"')
def responsable_count(context, name, count):
    # Buscar tabla de 'Solicitudes por responsable' y filas
    try:
        xpath = (
            "//h3[normalize-space()='Solicitudes por responsable']"
            "/following-sibling::table[1]"
        )
        table = context.driver.find_element(By.XPATH, xpath)
    except Exception:
        # alternativamente buscar cualquier tabla que contenga el responsable
        table = None
    rows = []
    if table:
        rows = table.find_elements(By.TAG_NAME, 'tr')
    else:
        # scan body for lines like 'Nombre <whitespace> número'
        body = context.driver.find_element(
            By.TAG_NAME, 'body').text.split('\n')
        for line in body:
            if name in line:
                # extraer dígitos en la línea
                m = re.search(r"(\d+)", line)
                if m:
                    actual = m.group(1)
                    assert str(actual) == str(count), (
                        f"Para responsable {name} se esperaba {count} "
                        f"pero se encontró {actual} en la línea: {line}"
                    )
                    return
        raise AssertionError(
            f"No se encontró tabla ni línea con responsable '{name}'"
        )
    # iterar filas buscando el nombre
    for tr in rows[1:]:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        if not tds:
            continue
        first = tds[0].text.strip()
        if first == name:
            actual = tds[1].text.strip()
            assert str(actual) == str(count), (
                f"Para responsable {name} se esperaba {count} "
                f"pero se encontró {actual}"
            )
            return
    raise AssertionError(
        f"No se encontró fila para el responsable '{name}' en la tabla"
    )
