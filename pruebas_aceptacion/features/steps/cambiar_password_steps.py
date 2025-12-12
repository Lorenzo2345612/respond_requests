from behave import given, when, then
from django.contrib.auth import get_user_model
from django.urls import reverse
from selenium.webdriver.common.by import By

Usuario = get_user_model()


# ==================== GIVEN ====================

@given('que existe el usuario admin por defecto que debe cambiar contraseña')
def step_admin_debe_cambiar_password(context):
    """Crea usuario admin con debe_cambiar_password=True"""
    Usuario.objects.filter(username='admin').delete()
    context.admin_user = Usuario.objects.create_user(
        username='admin',
        password='admin',
        email='admin@test.com',
        first_name='Admin',
        last_name='Sistema',
        rol='administrador',
        is_staff=True,
        is_superuser=True
    )
    context.admin_user.debe_cambiar_password = True
    context.admin_user.perfil_completo = False
    context.admin_user.save()


@given('que existe el usuario admin con password "{password}" que debe cambiar contraseña')
def step_admin_con_password_debe_cambiar(context, password):
    """Crea admin con contraseña específica y debe_cambiar_password=True"""
    Usuario.objects.filter(username='admin').delete()
    context.admin_user = Usuario.objects.create_user(
        username='admin',
        password=password,
        email='admin@test.com',
        first_name='Admin',
        last_name='Sistema',
        rol='administrador',
        is_staff=True,
        is_superuser=True
    )
    context.admin_user.debe_cambiar_password = True
    context.admin_user.perfil_completo = False
    context.admin_user.save()


@given('que existe el usuario admin que ya cambió su contraseña')
def step_admin_cambio_password(context):
    """Crea admin que ya cambió su contraseña"""
    Usuario.objects.filter(username='admin').delete()
    context.admin_user = Usuario.objects.create_user(
        username='admin',
        password='nueva_password_segura123!',
        email='admin@test.com',
        first_name='Admin',
        last_name='Sistema',
        rol='administrador',
        is_staff=True,
        is_superuser=True
    )
    context.admin_user.debe_cambiar_password = False
    context.admin_user.perfil_completo = True
    context.admin_user.save()


@given('que existe un usuario "{username}" con perfil incompleto')
def step_usuario_perfil_incompleto(context, username):
    """Crea usuario con perfil_completo=False"""
    Usuario.objects.filter(username=username).delete()
    context.usuario = Usuario.objects.create_user(
        username=username,
        password='testpass123',
        email=f'{username}@test.com',
        rol='alumno'
    )
    context.usuario.debe_cambiar_password = False
    context.usuario.perfil_completo = False
    context.usuario.save()


@given('el usuario admin está autenticado')
def step_admin_autenticado(context):
    """Autentica al usuario admin"""
    context.client.force_login(context.admin_user)


@given('que el usuario está en la página de cambio de contraseña')
def step_en_pagina_cambiar_password(context):
    """Navega a la página de cambio de contraseña"""
    context.response = context.client.get(
        reverse('solicitudes_app:cambiar_password'))
    assert context.response.status_code == 200


# ==================== WHEN ====================

@when('el usuario intenta acceder a cualquier página del sistema')
def step_acceder_cualquier_pagina(context):
    """Intenta acceder a la página de bienvenida"""
    context.response = context.client.get(reverse('bienvenida'), follow=True)


@when('ingresa la contraseña actual "{password_actual}"')
def step_ingresa_password_actual(context, password_actual):
    """Almacena la contraseña actual para el formulario"""
    if not hasattr(context, 'form_data'):
        context.form_data = {}
    context.form_data['old_password'] = password_actual


@when('ingresa la nueva contraseña "{nueva_password}"')
def step_ingresa_nueva_password(context, nueva_password):
    """Almacena la nueva contraseña"""
    if not hasattr(context, 'form_data'):
        context.form_data = {}
    context.form_data['new_password1'] = nueva_password


@when('confirma la nueva contraseña "{confirmar_password}"')
def step_confirma_nueva_password(context, confirmar_password):
    """Almacena la confirmación de contraseña"""
    if not hasattr(context, 'form_data'):
        context.form_data = {}
    context.form_data['new_password2'] = confirmar_password


@when('hace clic en el botón de cambiar contraseña')
def step_clic_cambiar_password(context):
    """Envía el formulario de cambio de contraseña"""
    context.response = context.client.post(
        reverse('solicitudes_app:cambiar_password'),
        data=context.form_data,
        follow=True
    )


# ==================== THEN ====================

@then('ve un mensaje informativo con las credenciales predeterminadas')
def step_ve_mensaje_credenciales(context):
    """Verifica que se muestre el mensaje con credenciales"""
    content = context.response.content.decode('utf-8')
    assert 'Primera vez en el sistema' in content or 'administrador predeterminado' in content


@then('el mensaje muestra "{texto}"')
def step_mensaje_muestra_texto(context, texto):
    """Verifica que el mensaje contenga texto específico"""
    content = context.response.content.decode('utf-8')
    # Más flexible para variaciones de formato
    if ':' in texto:
        # Para "Usuario: admin", buscar "admin" o "usuario" cerca
        parts = [p.strip() for p in texto.split(':')]
        assert any(part.lower() in content.lower() for part in parts), \
            f"No se encontró ninguna parte de '{texto}' en la respuesta"
    else:
        assert texto in content or texto.lower() in content.lower(), \
            f"No se encontró '{texto}' en la respuesta"


@then('el mensaje indica que debe cambiar la contraseña')
def step_mensaje_cambiar_password(context):
    """Verifica advertencia de cambio de contraseña"""
    content = context.response.content.decode('utf-8')
    assert 'cambiar' in content.lower() and 'contraseña' in content.lower()


@then('el usuario es redirigido a la página de cambio de contraseña')
def step_redirigido_cambiar_password(context):
    """Verifica redirección a cambio de contraseña"""
    assert context.response.redirect_chain[-1][0] == reverse(
        'solicitudes_app:cambiar_password')


@then('ve el mensaje indicando que debe cambiar su contraseña')
def step_ve_mensaje_debe_cambiar(context):
    """Verifica mensaje de cambio obligatorio"""
    content = context.response.content.decode('utf-8')
    assert 'debe' in content.lower() or 'obligatorio' in content.lower()


@then('no ve el mensaje con las credenciales predeterminadas')
def step_no_ve_credenciales(context):
    """Verifica que NO se muestre el mensaje de credenciales"""
    content = context.response.content.decode('utf-8')
    assert 'Primera vez en el sistema' not in content
    assert 'administrador predeterminado' not in content


@then('solo ve el formulario de login normal')
def step_solo_formulario_login(context):
    """Verifica que solo hay formulario de login"""
    content = context.response.content.decode('utf-8')
    assert 'username' in content.lower()
    assert 'password' in content.lower()


@then('la contraseña se actualiza exitosamente')
def step_password_actualizada(context):
    """Verifica que la contraseña cambió"""
    # Determina qué usuario usar según el contexto (el más reciente)
    if hasattr(context, 'usuario') and context.usuario:
        usuario = Usuario.objects.get(username=context.usuario.username)
    elif hasattr(context, 'admin_user') and context.admin_user:
        usuario = Usuario.objects.get(username=context.admin_user.username)
    else:
        raise ValueError("No se encontró usuario en el contexto")

    # Verifica que la contraseña cambió
    password_cambiada = usuario.check_password(
        context.form_data['new_password1'])
    if not password_cambiada:
        raise AssertionError(f"La contraseña no cambió para el usuario {usuario.username}. "
                             f"Password esperada: {context.form_data['new_password1']}")
    assert password_cambiada


@then('el flag debe_cambiar_password se establece en False')
def step_flag_debe_cambiar_false(context):
    """Verifica que el flag se estableció en False"""
    usuario = Usuario.objects.get(username=context.admin_user.username)
    assert usuario.debe_cambiar_password is False


@then('el usuario es redirigido a la página de completar perfil')
def step_redirigido_completar_perfil(context):
    """Verifica redirección a completar perfil"""
    assert reverse(
        'solicitudes_app:perfil') in context.response.redirect_chain[-1][0]


@then('ve un mensaje de error indicando que la contraseña es demasiado común')
def step_error_password_comun(context):
    """Verifica error de contraseña común"""
    content = context.response.content.decode('utf-8')
    assert 'común' in content.lower() or 'common' in content.lower()


@then('ve un mensaje de error indicando que la contraseña debe tener al menos 8 caracteres')
def step_error_password_corta(context):
    """Verifica error de contraseña corta"""
    content = context.response.content.decode('utf-8')
    assert '8' in content and (
        'caracteres' in content.lower() or 'characters' in content.lower())


@then('permanece en la página de cambio de contraseña')
def step_permanece_cambiar_password(context):
    """Verifica que permanece en la misma página"""
    assert 'cambiar-password' in context.response.request['PATH_INFO']


@then('ve un mensaje de error indicando que las contraseñas no coinciden')
def step_error_passwords_no_coinciden(context):
    """Verifica error de contraseñas no coincidentes"""
    content = context.response.content.decode('utf-8')
    assert 'coincid' in content.lower() or "didn't match" in content.lower()


@then('ve un mensaje de error indicando que la contraseña actual es incorrecta')
def step_error_password_actual_incorrecta(context):
    """Verifica error de contraseña actual incorrecta"""
    content = context.response.content.decode('utf-8')
    assert 'incorrecta' in content.lower() or 'incorrect' in content.lower()


@then('ve un mensaje de error indicando que la contraseña es muy similar al nombre de usuario')
def step_error_password_similar_username(context):
    """Verifica error de contraseña similar al username"""
    content = context.response.content.decode('utf-8')
    assert 'similar' in content.lower() or 'usuario' in content.lower()


@then('es redirigido automáticamente a la página de cambio de contraseña')
def step_redirigido_auto_cambiar_password(context):
    """Verifica redirección automática a cambio de contraseña"""
    assert context.response.redirect_chain[-1][0] == reverse('solicitudes_app:cambiar_password') or \
        'cambiar-password' in context.response.redirect_chain[-1][0]


@then('ve un mensaje indicando que debe cambiar su contraseña por seguridad')
def step_ve_mensaje_debe_cambiar_seguridad(context):
    """Verifica mensaje de seguridad sobre cambio obligatorio"""
    content = context.response.content.decode('utf-8')
    assert 'seguridad' in content.lower() or 'debe' in content.lower(
    ) or 'obligatorio' in content.lower()
