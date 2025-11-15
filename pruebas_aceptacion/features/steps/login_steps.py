from behave import given, when, then
from django.test import Client
from django.urls import reverse
from solicitudes_app.models import Usuario


@given('que existe un usuario con username "{username}" y password "{password}" y rol "{rol}"')
def step_crear_usuario(context, username, password, rol):
    context.usuario = Usuario.objects.create_user(
        username=username,
        email=f"{username}@test.com",
        password=password,
        first_name='Test',
        last_name='User',
        rol=rol
    )


@given('que el usuario "{username}" está autenticado')
def step_autenticar_usuario(context, username):
    if not hasattr(context, 'client'):
        context.client = Client()
    context.client.login(username=username, password='testpass123')


@when('el usuario visita la página de login')
def step_visitar_login(context):
    if not hasattr(context, 'client'):
        context.client = Client()
    context.response = context.client.get(reverse('solicitudes_app:login'))


@when('ingresa username "{username}" y password "{password}"')
def step_ingresar_credenciales(context, username, password):
    context.username = username
    context.password = password


@when('hace clic en el botón de iniciar sesión')
def step_click_login(context):
    context.response = context.client.post(
        reverse('solicitudes_app:login'),
        {
            'username': context.username,
            'password': context.password
        },
        follow=True
    )


@then('el usuario es redirigido a la página de bienvenida')
def step_redirigido_bienvenida(context):
    assert context.response.status_code == 200
    assert context.response.redirect_chain[-1][0] == reverse('bienvenida') or \
           'bienvenida' in context.response.redirect_chain[-1][0]


@then('ve el mensaje "{mensaje}"')
def step_ver_mensaje(context, mensaje):
    content = context.response.content.decode('utf-8')
    assert mensaje in content, f"No se encontró '{mensaje}' en la respuesta"


@then('el usuario permanece en la página de login')
def step_permanece_login(context):
    assert context.response.status_code == 200
    content = context.response.content.decode('utf-8')
    assert 'login' in content.lower()


@when('el usuario intenta acceder a la página de perfil sin estar autenticado')
def step_acceder_perfil_sin_auth(context):
    if not hasattr(context, 'client'):
        context.client = Client()
    context.response = context.client.get(reverse('solicitudes_app:perfil'))


@then('el usuario es redirigido a la página de login')
def step_redirigido_login(context):
    assert context.response.status_code == 302
    assert '/auth/login/' in context.response.url


@when('el usuario hace clic en cerrar sesión')
def step_cerrar_sesion(context):
    context.response = context.client.get(reverse('solicitudes_app:logout'), follow=True)
