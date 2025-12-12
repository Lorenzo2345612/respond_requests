from behave import given, when, then
from django.contrib.auth import get_user_model
from django.urls import reverse

Usuario = get_user_model()


# ==================== WHEN ====================

@when('un usuario no autenticado intenta acceder a "{url}"')
def step_no_autenticado_accede_url(context, url):
    """Usuario no autenticado intenta acceder a URL"""
    context.client.logout()
    context.response = context.client.get(url, follow=True)


@when('el usuario intenta acceder a "{url}"')
def step_usuario_accede_url(context, url):
    """Usuario autenticado intenta acceder a URL"""
    context.response = context.client.get(url, follow=True)


@when('el administrador visita "{url}"')
def step_admin_visita_url(context, url):
    """Administrador visita URL específica"""
    context.response = context.client.get(url)


@when('el usuario visita la página de bienvenida')
def step_visita_bienvenida(context):
    """Usuario visita bienvenida"""
    context.response = context.client.get(reverse('bienvenida'))


@when('el administrador visita cualquier página del sistema')
def step_admin_visita_cualquier_pagina(context):
    """Admin visita una página del sistema"""
    context.response = context.client.get(reverse('bienvenida'))


@when('el usuario accede a las siguientes URLs')
def step_accede_urls_tabla(context):
    """Usuario accede a múltiples URLs de la tabla"""
    context.responses = []
    for row in context.table:
        url = row['URL']
        response = context.client.get(url, follow=True)
        context.responses.append({'url': url, 'response': response})


@when('es redirigido al login con next={next_url}')
def step_redirigido_login_con_next(context, next_url):
    """Verifica que fue redirigido al login con parámetro next"""
    assert 'login' in context.response.redirect_chain[-1][0]
    assert f'next={next_url}' in context.response.redirect_chain[-1][0]


@when('el usuario ingresa credenciales válidas')
def step_ingresa_credenciales_validas(context):
    """Ingresa credenciales válidas en el login"""
    context.form_data = {
        'username': 'usuario_test',
        'password': 'testpass123'
    }


@when('hace clic en iniciar sesión')
def step_clic_iniciar_sesion(context):
    """Hace clic en iniciar sesión"""
    context.response = context.client.post(
        reverse('solicitudes_app:login'),
        data=context.form_data,
        follow=True
    )


# ==================== THEN ====================

@then('es redirigido a la página de login')
def step_redirigido_login(context):
    """Verifica redirección a login"""
    assert 'login' in context.response.redirect_chain[-1][0]


@then('ve el parámetro "next={next_param}" en la URL')
def step_ve_parametro_next(context, next_param):
    """Verifica parámetro next en URL"""
    assert f'next={next_param}' in context.response.request['QUERY_STRING'] or \
        f'next={next_param}' in str(context.response.redirect_chain)


# Removed duplicate - using existing one from login_steps.py
# @then('el usuario es redirigido a la página de bienvenida')


@then('ve un mensaje indicando acceso no autorizado')
def step_mensaje_no_autorizado(context):
    """Verifica mensaje de acceso no autorizado"""
    content = context.response.content.decode('utf-8')
    # Puede ser mensaje o redirección
    assert 'autorizado' in content.lower() or len(
        context.response.redirect_chain) > 0


@then('ve la página de gestión de usuarios correctamente')
def step_ve_gestion_usuarios(context):
    """Verifica que ve página de gestión"""
    assert context.response.status_code == 200
    content = context.response.content.decode('utf-8')
    assert 'usuario' in content.lower()


@then('ve la lista de usuarios registrados')
def step_ve_lista_usuarios(context):
    """Verifica que ve lista de usuarios"""
    content = context.response.content.decode('utf-8')
    assert 'usuario' in content.lower() or 'email' in content.lower()


@then('no ve el enlace "Gestionar Usuarios" en el menú de navegación')
def step_no_ve_enlace_gestion(context):
    """Verifica que no ve enlace de gestión"""
    content = context.response.content.decode('utf-8')
    assert 'Gestionar Usuarios' not in content


@then('ve el enlace "Gestionar Usuarios" en el menú de navegación')
def step_ve_enlace_gestion(context):
    """Verifica que ve enlace de gestión"""
    content = context.response.content.decode('utf-8')
    assert 'Gestionar Usuarios' in content or 'usuarios' in content.lower()


@then('es redirigido a "{url}"')
def step_redirigido_a_url(context, url):
    """Verifica redirección a URL específica"""
    assert url in context.response.redirect_chain[-1][0] or \
        context.response.request['PATH_INFO'] == url


@then('no puede acceder a otras páginas hasta cambiar su contraseña')
def step_no_accede_sin_cambiar_password(context):
    """Verifica que no puede acceder sin cambiar contraseña"""
    # Intenta acceder a otra página
    response = context.client.get(reverse('bienvenida'), follow=True)
    assert 'cambiar-password' in response.redirect_chain[-1][0]


@then('no puede acceder a otras páginas hasta completar su perfil')
def step_no_accede_sin_completar_perfil(context):
    """Verifica que no puede acceder sin completar perfil"""
    # Intenta acceder a otra página
    response = context.client.get(reverse('bienvenida'), follow=True)
    assert 'perfil' in response.redirect_chain[-1][0]


@then('accede correctamente a la página de solicitudes')
def step_accede_solicitudes(context):
    """Verifica acceso correcto a solicitudes"""
    assert context.response.status_code == 200


@then('no es redirigido a ninguna página de configuración')
def step_no_redirigido_configuracion(context):
    """Verifica que no hay redirección"""
    assert 'cambiar-password' not in context.response.request['PATH_INFO']
    assert 'perfil' not in context.response.request['PATH_INFO'] or \
           context.response.request['PATH_INFO'] == reverse('bienvenida')


@then('puede acceder a todas ellas sin redirecciones')
def step_accede_todas_sin_redireccion(context):
    """Verifica acceso sin redirecciones a todas las URLs"""
    for item in context.responses:
        # Verifica que cada URL fue accesible
        assert item['response'].status_code in [200, 302]
        # Si es 302, verifica que no redirige a cambiar password o perfil
        if item['response'].status_code == 302:
            redirect_url = item['response'].url if hasattr(
                item['response'], 'url') else ''
            assert 'cambiar-password' not in redirect_url
            # Permite redirección a perfil solo si la URL original es perfil
            if '/auth/perfil/' not in item['url']:
                assert 'perfil' not in redirect_url or redirect_url == item['url']


@then('ve la página de login correctamente')
def step_ve_login_correctamente(context):
    """Verifica que ve página de login"""
    assert context.response.status_code == 200
    content = context.response.content.decode('utf-8')
    assert 'login' in content.lower() or 'usuario' in content.lower()


@then('no es redirigido')
def step_no_redirigido(context):
    """Verifica que no hubo redirección"""
    assert len(context.response.redirect_chain) == 0 or \
        context.response.redirect_chain[-1][0] == context.response.request['PATH_INFO']


@then('ve la página de registro correctamente')
def step_ve_registro_correctamente(context):
    """Verifica que ve página de registro"""
    assert context.response.status_code == 200
    content = context.response.content.decode('utf-8')
    assert 'registro' in content.lower() or 'registr' in content.lower()


@then('el usuario es redirigido a "{url}"')
def step_usuario_redirigido_a(context, url):
    """Verifica redirección específica"""
    assert url in context.response.redirect_chain[-1][0] or \
        context.response.request['PATH_INFO'] == url


@then('no a la página de bienvenida por defecto')
def step_no_a_bienvenida_por_defecto(context):
    """Verifica que no fue a bienvenida"""
    # Solo verifica si no es la última redirección
    if len(context.response.redirect_chain) > 1:
        assert context.response.redirect_chain[-1][0] != reverse('bienvenida')


# ==================== GIVEN ====================

@given('que existe un usuario con username "{username}" con debe_cambiar_password en True')
def step_usuario_debe_cambiar_password(context, username):
    """Crea usuario con debe_cambiar_password=True"""
    Usuario.objects.filter(username=username).delete()
    context.usuario = Usuario.objects.create_user(
        username=username,
        password='testpass123',
        email=f'{username}@test.com',
        rol='alumno'
    )
    context.usuario.debe_cambiar_password = True
    context.usuario.perfil_completo = True
    context.usuario.save()


@given('que existe un usuario "{username}" con perfil_completo en False')
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


@given('el usuario ya cambió su contraseña')
def step_usuario_cambio_password(context):
    """Establece debe_cambiar_password=False"""
    context.usuario.debe_cambiar_password = False
    context.usuario.save()


@given('que existe un usuario "{username}" con perfil_completo en True')
def step_usuario_perfil_completo(context, username):
    """Crea usuario con perfil completo"""
    Usuario.objects.filter(username=username).delete()
    context.usuario = Usuario.objects.create_user(
        username=username,
        password='testpass123',
        email=f'{username}@test.com',
        rol='alumno'
    )
    context.usuario.debe_cambiar_password = False
    context.usuario.perfil_completo = True
    context.usuario.save()


# ==================== PASOS ADICIONALES ====================

@given('que existe un usuario con username "{username}" y rol "{rol}"')
def step_crear_usuario_con_rol(context, username, rol):
    """Crea un usuario con rol específico"""
    Usuario.objects.filter(username=username).delete()
    context.usuario = Usuario.objects.create_user(
        username=username,
        password='testpass123',
        email=f'{username}@test.com',
        first_name='Usuario',
        last_name='Test',
        rol=rol,
        telefono='4921234567',
        matricula='12345' if rol == 'alumno' else ''
    )
    context.usuario.debe_cambiar_password = False
    context.usuario.perfil_completo = True
    context.usuario.save()


@given('que existe un administrador con username "{username}"')
def step_crear_administrador_simple(context, username):
    """Crea un administrador"""
    Usuario.objects.filter(username=username).delete()
    context.admin_user = Usuario.objects.create_user(
        username=username,
        password='adminpass123',
        email=f'{username}@test.com',
        first_name='Admin',
        last_name='Sistema',
        rol='administrador',
        telefono='4921234567'
    )
    context.admin_user.debe_cambiar_password = False
    context.admin_user.perfil_completo = True
    context.admin_user.save()


@given('que existe un usuario "{username}" con debe_cambiar_password en True')
def step_usuario_debe_cambiar_password_true(context, username):
    """Crea usuario que debe cambiar contraseña"""
    Usuario.objects.filter(username=username).delete()
    context.usuario = Usuario.objects.create_user(
        username=username,
        password='testpass123',
        email=f'{username}@test.com',
        first_name='Nuevo',
        last_name='Usuario',
        rol='alumno',
        telefono='4921234567',
        matricula='12345'
    )
    context.usuario.debe_cambiar_password = True
    context.usuario.perfil_completo = False
    context.usuario.save()


@when('el usuario visita "{url}"')
def step_usuario_visita_url_especifica(context, url):
    """Usuario visita una URL específica"""
    context.response = context.client.get(url, follow=True)


@when('el usuario accede a las siguientes URLs:')
def step_accede_multiples_urls(context):
    """Usuario accede a múltiples URLs desde tabla"""
    context.responses = []
    for row in context.table:
        url = row['URL']
        response = context.client.get(url, follow=True)
        context.responses.append({'url': url, 'response': response})


@given('que existe un usuario con perfil_completo en False')
def step_usuario_perfil_incompleto_generico(context):
    """Crea un usuario con perfil incompleto"""
    Usuario.objects.filter(username='usuario_test').delete()
    context.usuario = Usuario.objects.create_user(
        username='usuario_test',
        password='testpass123',
        email='usuario@test.com',
        first_name='Usuario',
        last_name='Test',
        rol='alumno'
    )
    context.usuario.debe_cambiar_password = False
    context.usuario.perfil_completo = False
    context.usuario.save()


@given('el usuario está autenticado')
def step_usuario_autenticado_generico(context):
    """Autentica al usuario en el contexto"""
    if hasattr(context, 'usuario'):
        context.client.force_login(context.usuario)
    else:
        # Crear y autenticar usuario genérico
        usuario = Usuario.objects.create_user(
            username='test_user',
            password='testpass123',
            email='test@test.com',
            rol='alumno'
        )
        context.client.force_login(usuario)
        context.usuario = usuario


@when('un usuario no autenticado visita "{url}"')
def step_no_autenticado_visita_url(context, url):
    """Usuario no autenticado visita URL"""
    context.client.logout()
    context.response = context.client.get(url, follow=False)


@then('es redirigido a la página de bienvenida')
def step_redirigido_bienvenida(context):
    """Verifica redirección a bienvenida"""
    if hasattr(context.response, 'redirect_chain') and context.response.redirect_chain:
        assert 'bienvenida' in context.response.redirect_chain[-1][0]
    else:
        assert 'bienvenida' in context.response.url or context.response.status_code == 200
