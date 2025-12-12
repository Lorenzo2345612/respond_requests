from behave import when, then, given
from selenium.webdriver.common.by import By
import time


@given(u'que ingreso al url del sistema')
def step_impl(context):
    context.driver.get(context.url)
    time.sleep(1)


# ===WHEN

@when(u'me dirijo a raíz /')
def step_impl(context):
    pass


# ===THEN

@then(u'puedo ver en la página de bienvenida el mensaje "{mensaje}"')
def step_impl(context, mensaje):
    esperado = context.driver.find_element(By.ID, 'titulo').text
    assert esperado == mensaje, \
        f"El mensaje esperado es {esperado} y el que se obtiene es {mensaje}"
