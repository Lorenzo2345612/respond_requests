from behave import when, then, given
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
import re


@when(u'hago clic en el menú "Graficas"')
def step_impl(context):
    context.driver.find_element(By.ID, 'menu-graficas').click()
    context.wait = WebDriverWait(context.driver, 10)


@when(u'paso el mouse sobre una barra de la grafica con titulo "{titulo_grafica_solicitud}"')
def step_impl(context, titulo_grafica_solicitud):

    chart_map = {
        'Solicitudes de Hoy': 'chart_hoy',
        'Solicitudes de Esta Semana': 'chart_semana',
        'Solicitudes de Este Mes': 'chart_mes'
    }

    chart_id = chart_map.get(titulo_grafica_solicitud)
    if not chart_id:
        raise ValueError(
            f"No se encontró el chart con título: {titulo_grafica_solicitud}")

    context.wait = WebDriverWait(context.driver, 20)
    context.wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"#{chart_id} .highcharts-container")
        )
    )
    time.sleep(2)
    barra = context.wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"#{chart_id} .highcharts-point")
        )
    )
    actions = ActionChains(context.driver)
    actions.move_to_element(barra).perform()
    time.sleep(2)


@then(u'deberia ver el titulo "{titulo_tendencias_solicitudes}"')
def step_impl(context, titulo_tendencias_solicitudes):
    titulo = context.driver.find_element(By.CLASS_NAME, 'titulo-graficas').text
    assert titulo == titulo_tendencias_solicitudes, f"El titulo es {titulo}"


@then(u'debería ver la grafica con titulo "{titulo_grafica_solicitud}"')
def step_impl(context, titulo_grafica_solicitud):
    titulos = context.driver.find_elements(
        By.CSS_SELECTOR, ".highcharts-title")

    if titulo_grafica_solicitud in [titulo.text for titulo in titulos]:
        assert True
    else:
        assert False, f"No se encontró la gráfica con título {titulo_grafica_solicitud}"
    time.sleep(1)


@then(u'la grafica "{titulo_grafica_solicitud}" deberia mostrar datos')
def step_impl(context, titulo_grafica_solicitud):
    chart_map = {
        'Solicitudes de Hoy': 'chart_hoy',
        'Solicitudes de Esta Semana': 'chart_semana',
        'Solicitudes de Este Mes': 'chart_mes'
    }

    chart_id = chart_map.get(titulo_grafica_solicitud)
    if not chart_id:
        raise ValueError(
            f"No se encontró el chart con título: {titulo_grafica_solicitud}")

    print(f"Buscando barras en: {chart_id}")

    context.wait = WebDriverWait(context.driver, 20)

    context.wait.until(
        EC.presence_of_element_located((By.ID, chart_id))
    )
    context.wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"#{chart_id} .highcharts-container")
        )
    )
    time.sleep(2)
    barras = context.driver.find_elements(
        By.CSS_SELECTOR, f"#{chart_id} .highcharts-point")

    print(f"Se encontraron {len(barras)} barras en {chart_id}")

    assert len(
        barras) > 0, f"No hay barras en {titulo_grafica_solicitud} (ID: {chart_id})"


@then(u'deberia aparecer un recuadro con la informacion detallada')
def step_impl(context):
    tooltip = context.wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.highcharts-tooltip')
        )
    )
    assert tooltip.is_displayed(), "El tooltip no está visible"


@then(u'el recuadro deberia mostrar el tipo de solicitud')
def step_impl(context):
    tooltip_text = context.driver.find_element(
        By.CSS_SELECTOR, '.highcharts-tooltip'
    ).text
    assert len(tooltip_text) > 0, "El tooltip está vacío"
    assert tooltip_text.strip() != '', "El tooltip no muestra el tipo de solicitud"


@then(u'el recuadro deberia mostrar la cantidad de los tipos de solicitud')
def step_impl(context):
    tooltip_text = context.driver.find_element(
        By.CSS_SELECTOR, '.highcharts-tooltip'
    ).text
    numeros = re.findall(r'\d+', tooltip_text)
    assert len(
        numeros) > 0, f"El tooltip no muestra cantidades: {tooltip_text}"
