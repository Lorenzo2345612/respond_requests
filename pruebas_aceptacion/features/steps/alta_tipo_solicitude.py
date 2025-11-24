from behave import when, then, given
from selenium.webdriver.common.by import By
import time

@given(u'que ingreso al sistema')
def step_impl(context):
    context.driver.get(context.url)


@given(u'seleccion el menú Tipo de solicitudes')
def step_impl(context):
    context.driver.get(f"{context.url}/tipo-solicitud/")
    time.sleep(1)


@given(u'escribo en la caja de texto nombre "{nombre}" y en la descripción "{descripcion}"')
def step_impl(context, nombre, descripcion):
    context.driver.find_element(By.NAME, 'nombre').send_keys(nombre)
    context.driver.find_element(By.NAME, 'descripcion').send_keys(descripcion)
    time.sleep(1)


#===WHEN

@when(u'presiono el botón Agregar')
def step_impl(context):
    boton = context.driver.find_element(By.XPATH, "//button[@type='submit']")
    boton.click()
    time.sleep(2)


#===THEN

@then(u'puedo ver el tipo "{nombre}" en la lista de tipos de solicitudes.')
def step_impl(context, nombre):
    time.sleep(1)
    
    if '/tipo-solicitud/lista/' not in context.driver.current_url:
        context.driver.get(f"{context.url}/tipo-solicitud/lista/")
        time.sleep(1)
    else:
        context.driver.refresh()
        time.sleep(1)
    
    body = context.driver.find_element(By.ID, 'bodyTipoSolicitudes')
    trs = body.find_elements(By.TAG_NAME, 'tr')
    tipo_solicitud = []
    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        if tds and len(tds) > 0:
            tipo_solicitud.append(tds[0].text)
    assert nombre in tipo_solicitud, f"No se encontró '{nombre}' en la lista: {str(tipo_solicitud)}"
    time.sleep(1)


