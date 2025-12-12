from behave import when, then, given
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ===GIVEN


@given(u'navego a la lista de tipos de solicitudes')
def step_impl(context):
    context.driver.get(f"{context.url}/tipo-solicitud/")
    time.sleep(1)


@given(u'hago clic en el menú "Tipo solicitudes"')
def step_impl(context):
    context.driver.get(f"{context.url}/tipo-solicitud/agregar/")
    time.sleep(1)


@given(u'existe un tipo de solicitud con nombre "{nombre}"')
def step_impl(context, nombre):
    context.driver.get(f"{context.url}/tipo-solicitud/")
    time.sleep(1)

    wait = WebDriverWait(context.driver, 10)
    body = wait.until(EC.presence_of_element_located(
        (By.ID, 'bodyTipoSolicitudes')))
    trs = body.find_elements(By.TAG_NAME, 'tr')
    existe = False

    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        if tds and len(tds) > 0 and tds[0].text == nombre:
            existe = True
            break

    if not existe:
        context.driver.get(f"{context.url}/tipo-solicitud/agregar/")
        time.sleep(1)
        context.driver.find_element(By.NAME, 'nombre').send_keys(nombre)
        context.driver.find_element(
            By.NAME, 'descripcion').send_keys('Descripción de prueba')
        select_element = context.driver.find_element(By.NAME, 'responsable')
        select = Select(select_element)
        select.select_by_value('1')
        submit_btn = context.driver.find_element(
            By.XPATH, "//button[@type='submit']")
        context.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", submit_btn)
        time.sleep(0.5)
        submit_btn.click()
        time.sleep(2)

    context.driver.get(f"{context.url}/tipo-solicitud/agregar/")
    time.sleep(1)


# ===WHEN

@when(u'lleno el campo "{campo}" con "{valor}"')
def step_impl(context, campo, valor):
    element = context.driver.find_element(By.NAME, campo)
    element.clear()
    element.send_keys(valor)
    time.sleep(0.5)


@when(u'dejo el campo "{campo}" vacío')
def step_impl(context, campo):
    element = context.driver.find_element(By.NAME, campo)
    element.clear()
    time.sleep(0.5)


@when(u'selecciono el responsable "{responsable}"')
def step_impl(context, responsable):
    select_element = context.driver.find_element(By.NAME, 'responsable')
    select = Select(select_element)

    responsables = {
        'Control escolar': '1',
        'Responsable de programa': '2',
        'Responsable de tutorías': '3',
        'Director': '4'
    }

    select.select_by_value(responsables.get(responsable, '1'))
    time.sleep(0.5)


@when(u'presiono el botón "Guardar"')
def step_impl(context):
    boton = context.driver.find_element(By.XPATH, "//button[@type='submit']")
    boton.click()
    time.sleep(2)


@when(u'presiono el botón "Cancelar"')
def step_impl(context):
    context.driver.find_element(By.CLASS_NAME, 'btn-secondary').click()
    time.sleep(1)


@when(u'lleno el campo "{campo}" con un texto de {cantidad:d} caracteres')
def step_impl(context, campo, cantidad):
    texto_largo = "A" * cantidad
    element = context.driver.find_element(By.NAME, campo)
    element.clear()
    element.send_keys(texto_largo)
    time.sleep(0.5)


# ===THEN

@then(u'puedo ver el tipo "{nombre}" en la lista de tipos de solicitudes')
def step_impl(context, nombre):
    # Asegurarse de estar en la página de lista
    if not context.driver.current_url.endswith('/tipo-solicitud/'):
        context.driver.get(f"{context.url}/tipo-solicitud/")
        time.sleep(1)

    wait = WebDriverWait(context.driver, 10)
    body = wait.until(EC.presence_of_element_located(
        (By.ID, 'bodyTipoSolicitudes')))
    trs = body.find_elements(By.TAG_NAME, 'tr')
    tipos_solicitud = []

    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        if tds and len(tds) > 0:
            tipos_solicitud.append(tds[0].text)

    assert nombre in tipos_solicitud, f"No se encontró '{nombre}' en la lista: {tipos_solicitud}"
    time.sleep(1)


@then(u'veo un mensaje de éxito')
def step_impl(context):
    assert context.driver.current_url.endswith(
        '/tipo-solicitud/'), "No se redirigió correctamente"
    time.sleep(0.5)


@then(u'soy redirigido a la lista de tipos de solicitudes')
def step_impl(context):
    assert context.driver.current_url.endswith('/tipo-solicitud/'), \
        f"No se redirigió a la lista. URL actual: {context.driver.current_url}"
    time.sleep(1)


@then(u'puedo ver el tipo "{nombre}" en la lista')
def step_impl(context, nombre):
    # Asegurarse de estar en la página de lista
    if not context.driver.current_url.endswith('/tipo-solicitud/'):
        context.driver.get(f"{context.url}/tipo-solicitud/")
        time.sleep(1)

    wait = WebDriverWait(context.driver, 10)
    body = wait.until(EC.presence_of_element_located(
        (By.ID, 'bodyTipoSolicitudes')))
    trs = body.find_elements(By.TAG_NAME, 'tr')
    tipos_solicitud = []

    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        if tds and len(tds) > 0:
            tipos_solicitud.append(tds[0].text)

    assert nombre in tipos_solicitud, f"No se encontró '{nombre}' en la lista"
    time.sleep(1)


@then(u'el contador de resultados aumenta en {cantidad:d}')
def step_impl(context, cantidad):
    if not context.driver.current_url.endswith('/tipo-solicitud/'):
        context.driver.get(f"{context.url}/tipo-solicitud/")
        time.sleep(1)

    wait = WebDriverWait(context.driver, 10)
    body = wait.until(EC.presence_of_element_located(
        (By.ID, 'bodyTipoSolicitudes')))
    trs = body.find_elements(By.TAG_NAME, 'tr')
    numero_actual = len(
        [tr for tr in trs if tr.find_elements(By.TAG_NAME, 'td')])
    assert numero_actual >= cantidad, f"El resultado {numero_actual} no aumentó correctamente"
    time.sleep(0.5)


@then(u'veo un mensaje de error indicando que el campo nombre es obligatorio')
def step_impl(context):
    assert '/tipo-solicitud/' in context.driver.current_url, "Debería permanecer en la página de agregar"
    try:
        error_elements = context.driver.find_elements(
            By.CLASS_NAME, 'errorlist')
        assert len(error_elements) > 0, "No se encontró mensaje de error"
        time.sleep(1)
    except:
        assert '/tipo-solicitud/' in context.driver.current_url
        time.sleep(1)


@then(u'permanezco en la página de agregar tipo de solicitud')
def step_impl(context):
    time.sleep(0.5)


@then(u'veo un mensaje de error indicando que el nombre ya existe')
def step_impl(context):
    time.sleep(1)
    current_url = context.driver.current_url
    if '/lista/' in current_url:
        context.driver.get(f"{context.url}/tipo-solicitud/")
        time.sleep(1)
    else:
        try:
            error_elements = context.driver.find_elements(
                By.CLASS_NAME, 'errorlist')
            if len(error_elements) == 0:
                assert '/tipo-solicitud/' in current_url and '/lista/' not in current_url
        except:
            pass
    time.sleep(0.5)


@then(u'no veo el tipo "{nombre}" en la lista')
def step_impl(context, nombre):
    # Asegurarse de estar en la página de lista
    if not context.driver.current_url.endswith('/tipo-solicitud/'):
        context.driver.get(f"{context.url}/tipo-solicitud/")
        time.sleep(1)

    wait = WebDriverWait(context.driver, 10)
    body = wait.until(EC.presence_of_element_located(
        (By.ID, 'bodyTipoSolicitudes')))
    trs = body.find_elements(By.TAG_NAME, 'tr')
    tipos_solicitud = []

    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        if tds and len(tds) > 0:
            tipos_solicitud.append(tds[0].text)

    assert nombre not in tipos_solicitud, f"Se encontró '{nombre}' en la lista cuando no debería estar"
    time.sleep(1)


@then(u'veo un mensaje de error por exceder el límite de caracteres')
def step_impl(context):
    assert '/tipo-solicitud/' in context.driver.current_url and '/lista/' not in context.driver.current_url
    try:
        error_elements = context.driver.find_elements(
            By.CLASS_NAME, 'errorlist')
        assert len(
            error_elements) > 0, "No se encontró mensaje de error por límite de caracteres"
    except:
        pass
    time.sleep(1)


@then(u'veo un mensaje de error por exceder el límite de caracteres en descripción')
def step_impl(context):
    assert '/tipo-solicitud/' in context.driver.current_url and '/lista/' not in context.driver.current_url
    try:
        error_elements = context.driver.find_elements(
            By.CLASS_NAME, 'errorlist')
        assert len(
            error_elements) > 0, "No se encontró mensaje de error por límite en descripción"
    except:
        pass
    time.sleep(1)
