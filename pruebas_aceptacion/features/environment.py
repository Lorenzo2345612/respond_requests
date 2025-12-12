from django.test import Client
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.utils import timezone
from datetime import timedelta
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

from django.contrib.auth import get_user_model
from tipo_solicitudes.models import TipoSolicitud, Solicitud

Usuario = get_user_model()


def crear_datos_prueba_graficas():
    '''Crea datos de prueba para las gráficas'''
    # Crear tipos de solicitud si no existen
    tipo1, _ = TipoSolicitud.objects.get_or_create(
        nombre='Constancias',
        defaults={'descripcion': 'Constancias', 'responsable': '1'}
    )
    tipo2, _ = TipoSolicitud.objects.get_or_create(
        nombre='Inscripciones',
        defaults={'descripcion': 'Inscripción', 'responsable': '1'}
    )
    tipo3, _ = TipoSolicitud.objects.get_or_create(
        nombre='Becas',
        defaults={'descripcion': 'Becas', 'responsable': '1'}
    )
    
    # Crear usuario solicitante si no existe
    solicitante, _ = Usuario.objects.get_or_create(
        username='estudiante_test',
        defaults={
            'email': 'estudiante@uaz.edu.mx',
            'first_name': 'Estudiante',
            'last_name': 'Test',
            'rol': 'alumno'
        }
    )
    if not solicitante.has_usable_password():
        solicitante.set_password('test123')
        solicitante.save()
    
    # Crear solicitudes de hoy
    hoy = timezone.now()
    for i in range(3):
        Solicitud.objects.create(
            tipo_solicitud=tipo1,
            usuario=solicitante,
            folio=f'HOY-{i+1:04d}',
            estatus='1'  # 1 = Creada
        )
    
    # Crear solicitudes de esta semana (hace 3 días)
    hace_3_dias = hoy - timedelta(days=3)
    for i in range(2):
        solicitud = Solicitud.objects.create(
            tipo_solicitud=tipo2,
            usuario=solicitante,
            folio=f'SEM-{i+1:04d}',
            estatus='2'  # 2 = En proceso
        )
        # Modificar manualmente la fecha de creación
        Solicitud.objects.filter(pk=solicitud.pk).update(fecha_creacion=hace_3_dias)
    
    # Crear solicitudes de este mes (hace 15 días)
    hace_15_dias = hoy - timedelta(days=15)
    for i in range(4):
        solicitud = Solicitud.objects.create(
            tipo_solicitud=tipo3,
            usuario=solicitante,
            folio=f'MES-{i+1:04d}',
            estatus='1'  # 1 = Creada
        )
        # Modificar manualmente la fecha de creación
        Solicitud.objects.filter(pk=solicitud.pk).update(fecha_creacion=hace_15_dias)


def before_scenario(context, scenario):
    '''Se ejecuta antes de cada escenario'''
    # Limpiar usuarios previos
    Usuario.objects.all().delete()
    
    # Si el escenario es de gráficas, crear datos de prueba
    if 'graficas' in scenario.feature.filename.lower():
        crear_datos_prueba_graficas()

    context.client = Client()

    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')

    context.driver = webdriver.Chrome(options=chrome_options)
    context.driver.implicitly_wait(5)
    context.url = 'http://localhost:8000'


def after_scenario(context, scenario):
    '''Se ejecuta después de cada escenario'''
    if hasattr(context, 'driver'):
        context.driver.quit()
    
    # Limpiar flags de contexto específicos de gestion_preguntas_campos
    if hasattr(context, 'campos_limpiados_en_escenario'):
        delattr(context, 'campos_limpiados_en_escenario')
    if hasattr(context, 'orden_counter'):
        delattr(context, 'orden_counter')
    
    Usuario.objects.all().delete()
