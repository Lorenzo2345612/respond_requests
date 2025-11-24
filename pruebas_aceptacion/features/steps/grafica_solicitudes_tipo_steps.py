from behave import then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, JavascriptException

# Los pasos @given y @when son reutilizados de `solicitudes_por_tipo_steps.py`
# Por eso no se ven aquí

@then('la gráfica de tipo "{chart_type}" debe renderizarse')
def step_impl(context, chart_type):
    """Verifica que el gráfico de Chart.js se haya renderizado con el tipo correcto."""
    try:
        canvas = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, "trendChart"))
        )

        script = "return Chart.getChart(arguments[0]).config.type;"

        actual_type = WebDriverWait(context.driver, 10).until(
            lambda driver: driver.execute_script(script, canvas)
        )

        assert actual_type == chart_type, f"El tipo de gráfico esperado era '{chart_type}' pero se encontró '{actual_type}'"

    except TimeoutException:
        raise AssertionError("El canvas del gráfico 'trendChart' no se encontró o la instancia de Chart.js no se pudo obtener a tiempo.")
    except JavascriptException as e:
        raise AssertionError(f"Error de JavaScript al inspeccionar el gráfico: {e}")

@then('las etiquetas deben coincidir con los nombres de los tipos de solicitud')
def step_impl(context):
    """Verifica que las etiquetas del gráfico coincidan con los datos de prueba."""
    expected_labels = sorted(["Soporte", "Mantenimiento", "Consulta", "Incidencia"])
    
    try:
        canvas = context.driver.find_element(By.ID, "trendChart")
        script = "return Chart.getChart(arguments[0]).data.labels;"
        actual_labels = sorted(context.driver.execute_script(script, canvas))
        
        assert actual_labels == expected_labels, f"Las etiquetas no coinciden. Esperado: {expected_labels}, Encontrado: {actual_labels}"

    except (TimeoutException, JavascriptException) as e:
        raise AssertionError(f"No se pudieron obtener las etiquetas del gráfico: {e}")

@then('los valores deben coincidir con los conteos reales')
def step_impl(context):
    """Verifica que los datos del gráfico coincidan con los conteos de los datos de prueba."""
    # Los datos de prueba se crearon en `solicitudes_por_tipo_steps.py`
    expected_data_map = {
        "Soporte": 1,
        "Mantenimiento": 2,
        "Consulta": 3,
        "Incidencia": 4
    }
    
    try:
        canvas = context.driver.find_element(By.ID, "trendChart")
        # Obtener tanto etiquetas como datos para asegurar la correspondencia
        script = "const chart = Chart.getChart(arguments[0]); return { labels: chart.data.labels, data: chart.data.datasets[0].data };"
        chart_data = context.driver.execute_script(script, canvas)
        
        actual_data_map = dict(zip(chart_data['labels'], chart_data['data']))

        assert len(actual_data_map) == len(expected_data_map), f"El número de series de datos no coincide. Esperado: {len(expected_data_map)}, Encontrado: {len(actual_data_map)}"
        
        for label, expected_value in expected_data_map.items():
            assert label in actual_data_map, f"La etiqueta '{label}' no se encontró en el gráfico."
            assert actual_data_map[label] == expected_value, f"Para '{label}', se esperaba el valor {expected_value} pero se encontró {actual_data_map[label]}"
            
    except (TimeoutException, JavascriptException) as e:
        raise AssertionError(f"No se pudieron obtener los datos del gráfico: {e}")
