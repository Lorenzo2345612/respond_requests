from django.contrib.auth import get_user_model
from django.test import Client
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import sys
import django

# Añadir la carpeta 'app/solicitudes' al PYTHONPATH
base = os.path.abspath(os.path.join(os.path.dirname(
    __file__), '..', '..', 'app', 'solicitudes'))
if base not in sys.path:
    sys.path.insert(0, base)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'solicitudes.settings')
django.setup()


Usuario = get_user_model()


def before_scenario(context, scenario):
    '''Se ejecuta antes de cada escenario'''
    # Limpiar usuarios previos
    Usuario.objects.all().delete()

    context.client = Client()

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    context.driver = webdriver.Chrome(options=chrome_options)
    context.driver.implicitly_wait(5)
    context.url = 'http://localhost:8000'


def after_scenario(context, scenario):
    '''Se ejecuta después de cada escenario'''
    if hasattr(context, 'driver'):
        context.driver.quit()
    Usuario.objects.all().delete()
