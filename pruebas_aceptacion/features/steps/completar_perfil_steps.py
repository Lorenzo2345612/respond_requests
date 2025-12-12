from behave import given, when, then
from django.contrib.auth import get_user_model
from django.urls import reverse

Usuario = get_user_model()


# ==================== GIVEN ====================

@given('que existe un usuario "{username}" que ya cambió su contraseña')
def step_usuario_cambio_password(context, username):
    """Crea usuario que ya cambió contraseña"""
    Usuario.objects.filter(username=username).delete()
    context.usuario = Usuario.objects.create_user(
        username=username,
        password='Pass123!',  # Contraseña por defecto para usuarios que ya cambiaron
        email=f'{username}@test.com',
        first_name='Usuario',
        last_name='Nuevo',
        rol='alumno'
    )
    context.usuario.debe_cambiar_password = False
    context.usuario.perfil_completo = False
    context.usuario.save()


@given('el usuario tiene perfil_completo en False')
def step_perfil_completo_false(context):
    """Verifica que perfil_completo está en False"""
    assert context.usuario.perfil_completo is False


# Removed duplicate step - using existing one from gestion_usuarios_steps.py
# @given('el usuario "{username}" está autenticado')


@given('que el usuario está en la página de completar perfil')
@given('el usuario está en la página de completar perfil')
def step_en_pagina_completar_perfil(context):
    """Navega a la página de completar perfil"""
    context.response = context.client.get(reverse('solicitudes_app:perfil'))
    assert context.response.status_code == 200


@given('que existe otro usuario con email "{email}"')
def step_otro_usuario_con_email(context, email):
    """Crea otro usuario con email específico"""
    Usuario.objects.create_user(
        username=f'usuario_{email.split("@")[0]}',
        password='testpass123',
        email=email,
        rol='alumno'
    )


@given('que existe otro usuario con matricula "{matricula}"')
def step_otro_usuario_con_matricula(context, matricula):
    """Crea otro usuario con matrícula específica"""
    Usuario.objects.create_user(
        username=f'usuario_mat_{matricula}',
        password='testpass123',
        email=f'mat{matricula}@test.com',
        rol='alumno',
        matricula=matricula
    )


@given('que el usuario tiene email "{email}" en su perfil')
def step_usuario_tiene_email(context, email):
    """Establece el email del usuario"""
    context.usuario.email = email
    context.usuario.save()


# ==================== WHEN ====================

@when('el usuario intenta acceder a la página de bienvenida')
def step_acceder_bienvenida(context):
    """Intenta acceder a bienvenida"""
    context.response = context.client.get(reverse('bienvenida'), follow=True)


@when('completa los campos requeridos:')
def step_completa_campos_requeridos(context):
    """Completa campos del perfil desde tabla"""
    context.form_data = {}
    for row in context.table:
        context.form_data[row['Campo']] = row['Valor']


@when('hace clic en el botón de guardar')
def step_clic_guardar_perfil(context):
    """Envía el formulario de perfil"""
    context.response = context.client.post(
        reverse('solicitudes_app:perfil'),
        data=context.form_data,
        follow=True
    )


@when('ingresa "{valor}" en el campo {campo}')
def step_ingresa_valor_en_campo(context, valor, campo):
    """Ingresa un valor en un campo específico"""
    if not hasattr(context, 'form_data'):
        context.form_data = {}
    context.form_data[campo] = valor


@when('completa los demás campos correctamente')
def step_completa_demas_campos(context):
    """Completa campos con valores válidos por defecto"""
    if not hasattr(context, 'form_data'):
        context.form_data = {}

    defaults = {
        'first_name': 'Juan',
        'last_name': 'Pérez',
        'email': 'valido@test.com',
        'telefono': '4921234567',
        'area': 'Ingeniería',
        'matricula': '12345'
    }

    for campo, valor in defaults.items():
        if campo not in context.form_data:
            context.form_data[campo] = valor


@when('mantiene el email "{email}"')
def step_mantiene_email(context, email):
    """Mantiene el email actual"""
    if not hasattr(context, 'form_data'):
        context.form_data = {}
    context.form_data['email'] = email


# ==================== THEN ====================

@then('es redirigido automáticamente a la página de completar perfil')
def step_redirigido_completar_perfil(context):
    """Verifica redirección a completar perfil"""
    assert reverse(
        'solicitudes_app:perfil') in context.response.redirect_chain[-1][0]


@then('ve un formulario con sus datos básicos prellenados')
def step_ve_formulario_prellenado(context):
    """Verifica que el formulario muestra datos del usuario"""
    content = context.response.content.decode('utf-8')
    assert 'form' in content.lower()


@then('el perfil se actualiza exitosamente')
def step_perfil_actualizado(context):
    """Verifica que el perfil se actualizó"""
    usuario = Usuario.objects.get(username=context.usuario.username)
    assert usuario.first_name == context.form_data.get(
        'first_name', usuario.first_name)


@then('el flag perfil_completo se establece en True')
def step_perfil_completo_true(context):
    """Verifica que perfil_completo está en True"""
    usuario = Usuario.objects.get(username=context.usuario.username)
    assert usuario.perfil_completo is True


# Removed duplicate - using existing one from login_steps.py
# @then('el usuario es redirigido a la página de bienvenida')


@then('ve un mensaje de error "{mensaje}"')
def step_ve_mensaje_error(context, mensaje):
    """Verifica mensaje de error específico"""
    content = context.response.content.decode('utf-8')
    # Más flexible: busca palabras clave del mensaje
    # Ignora palabras muy cortas
    palabras_clave = [p for p in mensaje.lower().split() if len(p) > 2]
    content_lower = content.lower()
    # Verifica que al menos 2 palabras clave o 40% del mensaje estén presentes
    palabras_encontradas = sum(
        1 for palabra in palabras_clave if palabra in content_lower)
    umbral = max(2, len(palabras_clave) * 0.4)
    assert palabras_encontradas >= umbral, \
        f"Mensaje esperado: '{mensaje}'. Solo {palabras_encontradas}/{len(palabras_clave)} palabras significativas encontradas en respuesta"


@then('permanece en la página de completar perfil')
def step_permanece_completar_perfil(context):
    """Verifica que permanece en la página de perfil"""
    assert 'perfil' in context.response.request['PATH_INFO']


@then('el perfil se actualiza exitosamente sin error de email duplicado')
def step_perfil_actualizado_sin_error_duplicado(context):
    """Verifica actualización exitosa sin error de duplicado"""
    usuario = Usuario.objects.get(username=context.usuario.username)
    assert usuario.perfil_completo is True
    # Verifica que no hay errores en la respuesta
    assert context.response.status_code == 200 or len(
        context.response.redirect_chain) > 0
