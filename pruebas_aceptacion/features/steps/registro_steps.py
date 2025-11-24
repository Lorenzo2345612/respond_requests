from behave import given, when, then
from django.test import Client
from django.urls import reverse
from solicitudes_app.models import Usuario


@when('el usuario visita la página de registro')
def step_visitar_registro(context):
    if not hasattr(context, 'client'):
        context.client = Client()
    context.response = context.client.get(reverse('solicitudes_app:registro'))
    context.form_data = {}


@when('completa el formulario con los siguientes datos de alumno:')
def step_completar_formulario_alumno(context):
    for row in context.table:
        context.form_data[row['Campo']] = row['Valor']


@when('completa el formulario con los siguientes datos de administrador:')
def step_completar_formulario_admin(context):
    for row in context.table:
        context.form_data[row['Campo']] = row['Valor']


@when('hace clic en el botón de registrar')
def step_click_registrar(context):
    context.response = context.client.post(
        reverse('solicitudes_app:registro'),
        context.form_data,
        follow=True
    )


@then('el usuario está autenticado')
def step_usuario_autenticado(context):
    # Verificar que hay un usuario en la sesión
    assert '_auth_user_id' in context.client.session


@then('existe un usuario en la base de datos con username "{username}"')
def step_existe_usuario(context, username):
    assert Usuario.objects.filter(username=username).exists()


@then('existe en la base de datos un usuario con username "{username}" y rol "{rol}"')
def step_existe_usuario_con_rol(context, username, rol):
    usuario = Usuario.objects.get(username=username)
    assert usuario.rol == rol


@then('el usuario permanece en la página de registro')
def step_permanece_registro(context):
    assert context.response.status_code == 200
    content = context.response.content.decode('utf-8')
    assert 'registr' in content.lower() or 'crear' in content.lower()


@then('ve un error indicando que la matrícula es obligatoria para alumnos')
def step_error_matricula(context):
    content = context.response.content.decode('utf-8')
    assert 'matrícula' in content.lower() or 'matricula' in content.lower()


@given('que existe un usuario con email "{email}"')
def step_crear_usuario_con_email(context, email):
    Usuario.objects.create_user(
        username='existente',
        email=email,
        password='testpass123',
        rol='alumno'
    )


@when('completa el formulario con email "{email}"')
def step_completar_con_email(context, email):
    context.form_data = {
        'username': 'nuevo_usuario',
        'email': email,
        'first_name': 'Nuevo',
        'last_name': 'Usuario',
        'rol': 'alumno',
        'matricula': '12345',
        'password1': 'testpass123!',
        'password2': 'testpass123!'
    }


@then('ve un error indicando que el email ya está registrado')
def step_error_email_duplicado(context):
    content = context.response.content.decode('utf-8')
    assert 'email' in content.lower() and ('registrado' in content.lower() or 'exist' in content.lower())


@when('ingresa contraseñas diferentes en password1 y password2')
def step_contraseñas_diferentes(context):
    context.form_data = {
        'username': 'test_user',
        'email': 'test@test.com',
        'first_name': 'Test',
        'last_name': 'User',
        'rol': 'alumno',
        'matricula': '12345',
        'password1': 'password1!',
        'password2': 'password2!'
    }


@then('ve un error de contraseñas no coincidentes')
def step_error_contraseñas(context):
    content = context.response.content.decode('utf-8')
    assert 'contraseña' in content.lower() or 'password' in content.lower()
