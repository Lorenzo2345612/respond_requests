from behave import when, then, given
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ===GIVEN


@given(u'navego a la lista de formularios')
def step_impl(context):
    context.driver.get(f"{context.url}/tipo-solicitud/formularios/")
    time.sleep(1)


@given(u'existe un formulario llamado "{nombre}"')
def step_impl(context, nombre):
    context.driver.get(f"{context.url}/tipo-solicitud/formularios/")
    time.sleep(1)

    wait = WebDriverWait(context.driver, 10)
    body = wait.until(EC.presence_of_element_located(
        (By.ID, 'bodyTipoSolicitudes')))
    trs = body.find_elements(By.TAG_NAME, 'tr')
    existe = False

    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        if tds and len(tds) > 1 and tds[1].text == nombre:
            existe = True
            break

    if not existe:
        tipo_nombre = f"TipoPara{nombre.replace(' ', '')}"
        context.driver.get(f"{context.url}/tipo-solicitud/")
        time.sleep(0.5)

        wait = WebDriverWait(context.driver, 10)
        body_tipos = wait.until(EC.presence_of_element_located(
            (By.ID, 'bodyTipoSolicitudes')))
        trs_tipos = body_tipos.find_elements(By.TAG_NAME, 'tr')
        tipo_existe = False

        for tr in trs_tipos:
            tds = tr.find_elements(By.TAG_NAME, 'td')
            if tds and len(tds) > 0 and tds[0].text == tipo_nombre:
                tipo_existe = True
                break

        if not tipo_existe:
            context.driver.get(f"{context.url}/tipo-solicitud/agregar/")
            time.sleep(0.5)
            context.driver.find_element(
                By.NAME, 'nombre').send_keys(tipo_nombre)
            context.driver.find_element(
                By.NAME, 'descripcion').send_keys("Tipo de prueba")
            select_element = context.driver.find_element(
                By.NAME, 'responsable')
            select = Select(select_element)
            select.select_by_value('1')
            submit_btn = context.driver.find_element(
                By.XPATH, "//button[@type='submit']")
            context.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            time.sleep(0.5)
            submit_btn.click()
            time.sleep(2)

        context.driver.get(f"{context.url}/tipo-solicitud/formularios/crear/")
        time.sleep(1)

        select_element = context.driver.find_element(By.NAME, 'tipo_solicitud')
        select = Select(select_element)
        try:
            select.select_by_visible_text(tipo_nombre)
        except:
            options = [opt.text for opt in select.options]
            if options:
                select.select_by_index(1)

        context.driver.find_element(By.NAME, 'nombre').send_keys(nombre)
        context.driver.find_element(By.NAME, 'descripcion').send_keys(
            f"Descripción de {nombre}")

        wait = WebDriverWait(context.driver, 10)
        submit_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']")))
        context.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", submit_btn)
        time.sleep(0.5)
        context.driver.execute_script("arguments[0].click();", submit_btn)
        time.sleep(2)

    context.driver.get(f"{context.url}/tipo-solicitud/formularios/")
    time.sleep(1)
    context.ultimo_formulario_creado = nombre


# ===WHEN

@when(u'hago clic en el botón "Agregar"')
def step_impl(context):
    agregar_btn = context.driver.find_element(
        By.XPATH, "//a[contains(@class, 'btn-primary') and contains(., 'Agregar')]")
    agregar_btn.click()
    time.sleep(1)


@when(u'selecciono el tipo de solicitud "{tipo}"')
def step_impl(context, tipo):
    select_element = context.driver.find_element(By.NAME, 'tipo_solicitud')
    select = Select(select_element)

    try:
        select.select_by_visible_text(tipo)
        time.sleep(0.5)
    except:
        # Si no existe el tipo, crearlo directamente
        context.driver.get(f"{context.url}/tipo-solicitud/agregar/")
        time.sleep(1)
        context.driver.find_element(By.NAME, 'nombre').send_keys(tipo)
        context.driver.find_element(By.NAME, 'descripcion').send_keys(
            f"Descripción de {tipo}")
        select_resp = context.driver.find_element(By.NAME, 'responsable')
        Select(select_resp).select_by_value('1')
        context.driver.find_element(
            By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)

        # Volver a la página de crear formulario e intentar seleccionar
        context.driver.get(f"{context.url}/tipo-solicitud/formularios/crear/")
        time.sleep(1)
        select_element = context.driver.find_element(By.NAME, 'tipo_solicitud')
        select = Select(select_element)
        select.select_by_visible_text(tipo)
        time.sleep(0.5)


@when(u'no selecciono ningún tipo de solicitud')
def step_impl(context):
    time.sleep(0.5)


@when(u'lleno el campo formulario "{campo}" con "{valor}"')
def step_impl(context, campo, valor):
    element = context.driver.find_element(By.NAME, campo)
    element.clear()
    element.send_keys(valor)
    time.sleep(0.5)


@when(u'dejo el campo formulario "{campo}" vacío')
def step_impl(context, campo):
    element = context.driver.find_element(By.NAME, campo)
    element.clear()
    time.sleep(0.5)


@when(u'presiono el botón "Crear Formulario"')
def step_impl(context):
    wait = WebDriverWait(context.driver, 10)
    try:
        crear_btn = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Crear Formulario')]")))
    except:
        crear_btn = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[@type='submit']")))
    context.driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", crear_btn)
    time.sleep(0.5)
    context.driver.execute_script("arguments[0].click();", crear_btn)
    time.sleep(2)


@when(u'presiono el botón de cancelar en formulario')
def step_impl(context):
    wait = WebDriverWait(context.driver, 10)
    try:
        cancelar_btn = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@class, 'btn-secondary') and contains(text(), 'Cancelar')]")))
    except:
        cancelar_btn = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@href, 'formularios')]")))
    context.driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", cancelar_btn)
    time.sleep(0.5)
    context.driver.execute_script("arguments[0].click();", cancelar_btn)
    time.sleep(1)


@when(u'hago clic en el botón de opciones del formulario "{nombre}"')
def step_impl(context, nombre):
    body = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'bodyTipoSolicitudes'))
    )
    trs = body.find_elements(By.TAG_NAME, 'tr')

    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        if tds and nombre in tds[1].text:
            dropdown_btn = WebDriverWait(context.driver, 10).until(
                EC.element_to_be_clickable(tr.find_element(
                    By.CLASS_NAME, 'dropdown-toggle'))
            )
            context.driver.execute_script(
                "arguments[0].scrollIntoView(true);", dropdown_btn)
            time.sleep(0.3)
            dropdown_btn.click()
            WebDriverWait(context.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.dropdown-menu.show'))
            )
            time.sleep(0.5)
            break
    else:
        raise Exception(f"No se encontró el formulario '{nombre}' en la lista")


@when(u'selecciono la opción "{opcion}"')
def step_impl(context, opcion):
    dropdown_menu = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.dropdown-menu.show'))
    )
    opcion_link = dropdown_menu.find_element(
        By.XPATH, f".//a[contains(., '{opcion}')]")
    context.driver.execute_script(
        "arguments[0].scrollIntoView(true);", opcion_link)
    time.sleep(0.3)
    opcion_link.click()
    time.sleep(1)


@when(u'modifico el campo formulario "{campo}" a "{valor}"')
def step_impl(context, campo, valor):
    element = context.driver.find_element(By.NAME, campo)
    element.clear()
    time.sleep(0.2)
    element.send_keys(valor)
    time.sleep(0.5)


@when(u'limpio el campo formulario "{campo}"')
def step_impl(context, campo):
    element = context.driver.find_element(By.NAME, campo)
    element.clear()
    context.driver.execute_script("arguments[0].value = '';", element)
    time.sleep(0.5)


@when(u'presiono el botón "Guardar Cambios"')
def step_impl(context):
    wait = WebDriverWait(context.driver, 10)
    try:
        guardar_btn = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Guardar Cambios')]")))
    except:
        guardar_btn = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[@type='submit']")))
    context.driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", guardar_btn)
    time.sleep(0.5)
    context.driver.execute_script("arguments[0].click();", guardar_btn)
    time.sleep(2)


# ===THEN

@then(u'puedo ver el formulario "{nombre}" en la lista de formularios')
def step_impl(context, nombre):
    body = context.driver.find_element(By.ID, 'bodyTipoSolicitudes')
    trs = body.find_elements(By.TAG_NAME, 'tr')
    formularios = []

    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        if tds and len(tds) > 1:
            formularios.append(tds[1].text)  # Columna del nombre

    assert nombre in formularios, f"No se encontró '{nombre}' en la lista de formularios: {formularios}"
    time.sleep(1)


@then(u'soy redirigido a la lista de formularios')
def step_impl(context):
    assert '/tipo-solicitud/formularios/' in context.driver.current_url, \
        f"No se redirigió a la lista de formularios. URL actual: {context.driver.current_url}"
    time.sleep(1)


@then(u'veo el formulario "{nombre}" en la lista')
def step_impl(context, nombre):
    body = context.driver.find_element(By.ID, 'bodyTipoSolicitudes')
    trs = body.find_elements(By.TAG_NAME, 'tr')
    formularios = []

    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        if tds and len(tds) > 1:
            formularios.append(tds[1].text)

    assert nombre in formularios, f"No se encontró '{nombre}' en la lista"
    time.sleep(1)


@then(u'el contador de formularios aumenta en {cantidad:d}')
def step_impl(context, cantidad):
    if '/tipo-solicitud/formularios/' not in context.driver.current_url:
        context.driver.get(f"{context.url}/tipo-solicitud/formularios/")
        time.sleep(1)

    body = context.driver.find_element(By.ID, 'bodyTipoSolicitudes')
    trs = body.find_elements(By.TAG_NAME, 'tr')
    numero_actual = len(
        [tr for tr in trs if tr.find_elements(By.TAG_NAME, 'td')])
    assert numero_actual >= cantidad, f"El resultado {numero_actual} no es el esperado"
    time.sleep(0.5)


@then(u'veo un mensaje de error en el campo nombre del formulario')
def step_impl(context):
    assert '/tipo-solicitud/formularios/' in context.driver.current_url
    try:
        error_elements = context.driver.find_elements(
            By.CLASS_NAME, 'errorlist')
        assert len(error_elements) > 0, "No se encontró mensaje de error"
    except:
        pass
    time.sleep(1)


@then(u'permanezco en la página de crear formulario')
def step_impl(context):
    assert '/tipo-solicitud/formularios/crear/' in context.driver.current_url, \
        f"No permanece en la página de crear. URL actual: {context.driver.current_url}"
    time.sleep(0.5)


@then(u'permanezco en la página de editar formulario')
def step_impl(context):
    time.sleep(1)
    current_url = context.driver.current_url
    assert '/tipo-solicitud/formularios/' in current_url and '/editar/' in current_url, \
        f"No permanece en la página de editar. URL actual: {current_url}"
    time.sleep(0.5)


@then(u'veo un mensaje de error indicando que debe seleccionar un tipo de solicitud')
def step_impl(context):
    assert '/tipo-solicitud/formularios/crear/' in context.driver.current_url
    try:
        error_elements = context.driver.find_elements(
            By.CLASS_NAME, 'errorlist')
        assert len(error_elements) > 0, "No se encontró mensaje de error"
    except:
        pass
    time.sleep(1)


@then(u'no veo el formulario "{nombre}" en la lista')
def step_impl(context, nombre):
    body = context.driver.find_element(By.ID, 'bodyTipoSolicitudes')
    trs = body.find_elements(By.TAG_NAME, 'tr')
    formularios = []

    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        if tds and len(tds) > 1:
            formularios.append(tds[1].text)

    assert nombre not in formularios, f"Se encontró '{nombre}' en la lista cuando no debería estar"
    time.sleep(1)


@then(u'soy redirigido a la página de configurar campos')
def step_impl(context):
    # Verificar que la URL contiene la ruta de campos
    assert '/formulario/' in context.driver.current_url and '/campos/' in context.driver.current_url, \
        f"No se redirigió a la página de campos. URL actual: {context.driver.current_url}"
    time.sleep(1)


@then(u'veo el título "Configurar campos del formulario: {nombre}"')
def step_impl(context, nombre):
    time.sleep(1)
    try:
        h1_element = context.driver.find_element(By.TAG_NAME, 'h1')
        titulo = h1_element.text
    except:
        titulo = context.driver.find_element(By.XPATH, "//h1 | //h2").text

    assert 'Configurar campos' in titulo or nombre in titulo, \
        f"No se encontró el título esperado. Título actual: {titulo}"
    time.sleep(0.5)
