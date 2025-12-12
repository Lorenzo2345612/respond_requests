from behave import when, then, given
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys
import django

# Configurar Django
base = os.path.abspath(os.path.join(os.path.dirname(
    __file__), '..', '..', '..', '..', 'app', 'solicitudes'))
if base not in sys.path:
    sys.path.insert(0, base)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'solicitudes.settings')
django.setup()

from django.contrib.auth import get_user_model

@given(u'que ingreso al sistema')
def step_impl(context):
    # Crear usuario admin si no existe
    Usuario = get_user_model()
    if not Usuario.objects.filter(username='admin').exists():
        admin_user = Usuario.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='admin',
            first_name='Admin',
            last_name='Test',
            rol='administrador'
        )
        admin_user.save()
    
    context.admin_username = 'admin'
    context.admin_password = 'admin'
    
    # Ir a la página de login
    context.driver.get(f"{context.url}/auth/login/")
    time.sleep(3)
    
    # Imprimir URL actual para debug
    print(f"\nURL actual: {context.driver.current_url}")
    print(f"Título: {context.driver.title}")
    
    # Esperar a que aparezcan los campos de login
    wait = WebDriverWait(context.driver, 15)
    try:
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        password_field = context.driver.find_element(By.NAME, 'password')
        
        # Rellenar formulario de login
        username_field.send_keys('admin')
        password_field.send_keys(context.admin_password)
        time.sleep(0.5)
        
        # Hacer clic en el botón de login
        login_btn = context.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_btn.click()
        time.sleep(3)
        
        # Buscar y hacer clic en el botón "Guardar Cambios" si existe
        try:
            print("\nBuscando botón 'Guardar Cambios'...")
            guardar_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Guardar Cambios') or contains(text(), 'Guardar')]")
            ))
            print("Botón encontrado, haciendo clic...")
            guardar_btn.click()
            time.sleep(2)
            
            # Esperar a ver el mensaje de bienvenida
            print("Esperando mensaje de bienvenida...")
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Bienvenid') or contains(text(), 'bienvenid')]")
            ))
            print("¡Mensaje de bienvenida encontrado!")
            time.sleep(1)
        except Exception as e:
            print(f"\nNota: No se encontró botón 'Guardar Cambios' o ya está en página principal: {e}")
            
    except Exception as e:
        print(f"\nError al intentar login: {e}")
        print(f"Contenido de la página: {context.driver.page_source[:500]}")
        raise


@given(u'seleccion el menú Tipo de solicitudes')
def step_impl(context):
    context.driver.get(f"{context.url}/tipo-solicitud/agregar/")
    time.sleep(1)


@given(u'escribo en la caja de texto nombre "{nombre}" y en la descripción "{descripcion}"')
def step_impl(context, nombre, descripcion):
    context.driver.find_element(By.NAME, 'nombre').send_keys(nombre)
    context.driver.find_element(By.NAME, 'descripcion').send_keys(descripcion)
    time.sleep(1)


# ===WHEN

@when(u'presiono el botón Agregar')
def step_impl(context):
    boton = context.driver.find_element(By.XPATH, "//button[@type='submit']")
    boton.click()
    time.sleep(2)


# ===THEN

@then(u'puedo ver el tipo "{nombre}" en la lista de tipos de solicitudes.')
def step_impl(context, nombre):
    time.sleep(1)

    if not context.driver.current_url.endswith('/tipo-solicitud/'):
        context.driver.get(f"{context.url}/tipo-solicitud/")
        time.sleep(1)
    else:
        context.driver.refresh()
        time.sleep(1)

    wait = WebDriverWait(context.driver, 10)
    body = wait.until(EC.presence_of_element_located(
        (By.ID, 'bodyTipoSolicitudes')))
    trs = body.find_elements(By.TAG_NAME, 'tr')
    tipo_solicitud = []
    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        if tds and len(tds) > 0:
            tipo_solicitud.append(tds[0].text)
    assert nombre in tipo_solicitud, f"No se encontró '{nombre}' en la lista: {str(tipo_solicitud)}"
    time.sleep(1)
