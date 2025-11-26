from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

BASE_URL = "http://localhost:8000/solicitudes/listar"

@given("que estoy en la página de listado de solicitudes")
def step_impl(context):
    context.driver.get(BASE_URL)
    time.sleep(1) 

@given("estoy en la página de listado de solicitudes")
def step_impl(context):
    context.driver.get("http://localhost:8000/solicitudes/listar/")
    time.sleep(1)


@then("debo ver una tabla con al menos una solicitud")
def step_impl(context):
    filas = context.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    
    assert len(filas) >= 1, \
        " No se encontró ninguna solicitud en la tabla."

    print(f"Se encontraron {len(filas)} solicitudes.")

@then(u'solo veo las solicitudes en estado "Cancelada"')
def step_impl(context):
    filas = context.driver.find_elements(By.CSS_SELECTOR, "#solicitudesTable tbody tr")
    assert filas, "No se encontraron filas en la tabla de solicitudes."

    for fila in filas:
        celdas = fila.find_elements(By.TAG_NAME, "td")
        assert len(celdas) >= 4, "La fila no tiene suficientes columnas."
        texto_estado = celdas[3].text.strip()
        assert "Cancelada" in texto_estado, (
            f"Se encontró una solicitud con estado diferente: {texto_estado}"
        )

@when('hago clic en el botón "Atender" de la primera solicitud')
def step_impl(context):
    try:
        boton = context.driver.find_element(
            By.CSS_SELECTOR, "a.btn, a[href*='atender']"
        )
        boton.click()
        time.sleep(1)
    except NoSuchElementException:
        assert False, " No se encontró el botón 'Atender' en la tabla."

@when('aplico filtro por estado "Cancelada"')
def step_impl(context):
    boton = context.driver.find_element(By.ID, "btn-cancelada")
    boton.click()
    time.sleep(1)

@when('escribo "{folio}" en el buscador de folios')
def step_impl(context, folio):
    search_input = context.driver.find_element(By.ID, "search")
    search_input.clear()
    search_input.send_keys(folio)
    search_button = context.driver.find_element(By.ID, "search-button")
    search_button.click()

    time.sleep(1)


@then("debo ver el detalle de la solicitud")
def step_impl(context):
    body = context.driver.find_element(By.TAG_NAME, "body").text
    
    assert "Detalles de la Solicitud" in body, \
        " No se cargó la página de detalle de la solicitud."

    print("Se abrió la página de detalle correctamente.")


@then("debo ver un historial de seguimiento con al menos un registro")
def step_impl(context):
    filas = context.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    assert len(filas) >= 1, \
        " No existen filas en el historial de seguimiento."

    print(f"El historial contiene {len(filas)} registros.")

@then('debo ver en la tabla una fila con el folio "{folio}"')
def step_impl(context, folio):
    filas = context.driver.find_elements(By.CSS_SELECTOR, "#solicitudesTable tbody tr")
    assert len(filas) > 0, "No se encontraron filas en la tabla después de buscar."

    encontrado = False
    for fila in filas:
        celdas = fila.find_elements(By.TAG_NAME, "td")
        if not celdas:
            continue
        folio_en_tabla = celdas[0].text.strip() 
        if folio_en_tabla == folio:
            encontrado = True
            break

    assert encontrado, f'No se encontró una fila con el folio "{folio}" en los resultados de búsqueda.'
