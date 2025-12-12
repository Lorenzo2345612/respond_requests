from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Usuario
from .forms import RegistroUsuarioForm, LoginForm, ActualizarPerfilForm, GestionarUsuarioForm


def login_view(request):
    """Vista para login de usuarios"""
    if request.user.is_authenticated:
        return redirect('bienvenida')

    # Verificar si existe el admin predeterminado que aún no ha cambiado su contraseña
    mostrar_credenciales_admin = False
    try:
        admin_user = Usuario.objects.get(username='admin', rol='administrador')
        if admin_user.debe_cambiar_password:
            mostrar_credenciales_admin = True
    except Usuario.DoesNotExist:
        pass

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Configurar sesión
                if not remember_me:
                    request.session.set_expiry(0)

                messages.success(
                    request, f'¡Bienvenido {user.get_full_name()}!')

                # Redirigir según el rol
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('bienvenida')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            # Si el formulario no es válido (credenciales incorrectas)
            if form.errors.get('__all__'):
                messages.error(request, 'Usuario o contraseña incorrectos.')
            else:
                messages.error(
                    request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = LoginForm()

    return render(request, 'solicitudes_app/login.html', {
        'form': form,
        'mostrar_credenciales_admin': mostrar_credenciales_admin
    })


def registro_view(request):
    """Vista para registro de nuevos usuarios"""
    if request.user.is_authenticated:
        return redirect('bienvenida')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, '¡Cuenta creada exitosamente! Bienvenido.')
            return redirect('bienvenida')
        else:
            messages.error(
                request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'solicitudes_app/registro.html', {'form': form})


@login_required
def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('solicitudes_app:login')


@login_required
def perfil_view(request):
    """Vista para ver y editar el perfil del usuario"""
    if request.method == 'POST':
        form = ActualizarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            # Marcar perfil como completo
            user.perfil_completo = True
            user.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('bienvenida')
        else:
            messages.error(
                request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = ActualizarPerfilForm(instance=request.user)

    return render(request, 'solicitudes_app/perfil.html', {
        'form': form,
        'usuario': request.user
    })


@login_required
def lista_usuarios_view(request):
    """Vista para listar usuarios (solo administradores)"""
    if not request.user.puede_gestionar_usuarios():
        messages.error(
            request, 'No tienes permiso para acceder a esta página.')
        return redirect('bienvenida')

    usuarios = Usuario.objects.all().order_by('-date_joined')
    return render(request, 'solicitudes_app/lista_usuarios.html', {
        'usuarios': usuarios
    })


@login_required
def editar_usuario_view(request, usuario_id):
    """Vista para editar un usuario (solo administradores)"""
    if not request.user.puede_gestionar_usuarios():
        messages.error(
            request, 'No tienes permiso para acceder a esta página.')
        return redirect('bienvenida')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    # Validación: No permitir que el admin se quite su propio rol de administrador
    if request.method == 'POST':
        form = GestionarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            # Validar que el admin no se quite su propio rol de administrador
            if usuario.id == request.user.id and form.cleaned_data.get('rol') != 'administrador':
                messages.error(
                    request, 'No puedes quitarte tu propio rol de administrador.')
                return render(request, 'solicitudes_app/editar_usuario.html', {
                    'form': form,
                    'usuario': usuario
                })

            # Validar que no desactive su propia cuenta
            if usuario.id == request.user.id and not form.cleaned_data.get('is_active', True):
                messages.error(
                    request, 'No puedes desactivar tu propia cuenta.')
                return render(request, 'solicitudes_app/editar_usuario.html', {
                    'form': form,
                    'usuario': usuario
                })

            # Contar administradores activos antes de guardar
            admins_activos = Usuario.objects.filter(
                rol='administrador', is_active=True).count()

            # Si este es el último admin activo, no permitir cambio de rol o desactivación
            if (usuario.rol == 'administrador' and usuario.is_active and admins_activos <= 1):
                if (form.cleaned_data.get('rol') != 'administrador' or
                        not form.cleaned_data.get('is_active', True)):
                    messages.error(request,
                                   'No se puede modificar este usuario porque es el último administrador activo del sistema. '
                                   'Crea otro administrador primero.')
                    return render(request, 'solicitudes_app/editar_usuario.html', {
                        'form': form,
                        'usuario': usuario
                    })

            form.save()
            messages.success(
                request, f'Usuario {form.instance.get_full_name()} actualizado exitosamente.')
            return redirect('solicitudes_app:lista_usuarios')
        else:
            messages.error(
                request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = GestionarUsuarioForm(instance=usuario)

    return render(request, 'solicitudes_app/editar_usuario.html', {
        'form': form,
        'usuario': usuario
    })


@login_required
@require_http_methods(["POST"])
def eliminar_usuario_view(request, usuario_id):
    """Vista para eliminar un usuario (solo administradores)"""
    if not request.user.puede_gestionar_usuarios():
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('bienvenida')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    # Validación 1: No permitir eliminar el propio usuario
    if usuario.id == request.user.id:
        messages.error(request, 'No puedes eliminar tu propia cuenta.')
        return redirect('solicitudes_app:lista_usuarios')

    # Validación 2: No permitir eliminar el último administrador activo
    if usuario.rol == 'administrador' and usuario.is_active:
        admins_activos = Usuario.objects.filter(
            rol='administrador', is_active=True).count()
        if admins_activos <= 1:
            messages.error(request,
                           'No se puede eliminar el último administrador activo del sistema. '
                           'Crea otro administrador primero.')
            return redirect('solicitudes_app:lista_usuarios')

    username = usuario.username
    usuario.delete()
    messages.success(request, f'Usuario {username} eliminado exitosamente.')
    return redirect('solicitudes_app:lista_usuarios')


@login_required
def cambiar_password_view(request):
    """Vista para cambiar la contraseña (obligatorio para usuarios por defecto)"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Mantener la sesión activa
            update_session_auth_hash(request, user)

            # Marcar que ya cambió la contraseña
            user.debe_cambiar_password = False
            user.save()

            messages.success(request, '¡Contraseña cambiada exitosamente!')

            # Si aún no tiene perfil completo, redirigir a perfil
            if not user.perfil_completo:
                messages.info(
                    request, 'Ahora completa tu perfil con tus datos personales.')
                return redirect('solicitudes_app:perfil')

            return redirect('bienvenida')
        else:
            messages.error(
                request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'solicitudes_app/cambiar_password.html', {
        'form': form,
        'obligatorio': request.user.debe_cambiar_password
    })
