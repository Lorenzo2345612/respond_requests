from behave import fixture, use_fixture
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import django
from django.test.utils import setup_test_environment, teardown_test_environment
from django.core.management import call_command

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'solicitudes.settings')
django.setup()

@fixture
def django_test_environment(context):
    """Configura el entorno de prueba de Django"""
    setup_test_environment()
    # Crear base de datos de prueba
    call_command('migrate', '--run-syncdb', verbosity=0)
    yield
    teardown_test_environment()

@fixture
def browser_chrome(context):
    """Configura el navegador Chrome en modo headless"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    context.driver = webdriver.Chrome(options=chrome_options)
    context.driver.implicitly_wait(5)
    context.url = 'http://localhost:8000'
    
    yield context.driver
    context.driver.quit()

def before_all(context):
    """Se ejecuta antes de todas las pruebas"""
    use_fixture(django_test_environment, context)
    use_fixture(browser_chrome, context)