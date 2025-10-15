from behave import when, then, given
from selenium.webdriver.common.by import By
import time

@given(u'que ingreso al sistema')
def step_impl(context):
    context.driver.get(context.url)


@given(u'seleccion el menú Tipo de solicitudes')
def step_impl(context):
    context.driver.find_element(By.LINK_TEXT, 'Tipo solicitudes').click()
    time.sleep(10)


@given(u'escribo en la caja de texto nombre "Constancia" y en la descripción "Constancia para servicio de social"')
def step_impl(context):
    pass


@when(u'presiono el botón Agregar')
def step_impl(context):
    pass


@then(u'puedo ver el tipo "Constancia" en la lista de tipos de solicitudes.')
def step_impl(context):
    pass

