from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Usuario
from .forms import RegistroUsuarioForm, LoginForm, ActualizarPerfilForm, GestionarUsuarioForm


def login_view(request):
    """Vista para login de usuarios"""
    if request.user.is_authenticated:
        return redirect('bienvenida')
    
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
                
                messages.success(request, f'¡Bienvenido {user.get_full_name()}!')
                
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
                messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = LoginForm()
    
    return render(request, 'solicitudes_app/login.html', {'form': form})


def registro_view(request):
    """Vista para registro de nuevos usuarios"""
    if request.user.is_authenticated:
        return redirect('bienvenida')
    
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente! Bienvenido.')
            return redirect('bienvenida')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
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
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('solicitudes_app:perfil')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
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
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('bienvenida')
    
    usuarios = Usuario.objects.all().order_by('-date_joined')
    return render(request, 'solicitudes_app/lista_usuarios.html', {
        'usuarios': usuarios
    })


@login_required
def editar_usuario_view(request, usuario_id):
    """Vista para editar un usuario (solo administradores)"""
    if not request.user.puede_gestionar_usuarios():
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('bienvenida')
    
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if request.method == 'POST':
        form = GestionarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuario {form.instance.get_full_name()} actualizado exitosamente.')
            return redirect('solicitudes_app:lista_usuarios')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
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
    
    # No permitir eliminar el propio usuario
    if usuario.id == request.user.id:
        messages.error(request, 'No puedes eliminar tu propia cuenta.')
        return redirect('solicitudes_app:lista_usuarios')
    
    username = usuario.username
    usuario.delete()
    messages.success(request, f'Usuario {username} eliminado exitosamente.')
    return redirect('solicitudes_app:lista_usuarios')

