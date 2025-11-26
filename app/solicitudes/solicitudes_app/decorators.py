from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def rol_requerido(*roles):
    """
    Decorador para verificar que el usuario tenga uno de los roles especificados
    
    Uso:
    @rol_requerido('administrador', 'control_escolar')
    def mi_vista(request):
        ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('login')
            
            if request.user.rol not in roles:
                messages.error(request, 'No tienes permiso para acceder a esta página.')
                return redirect('bienvenida')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def administrador_requerido(view_func):
    """
    Decorador para verificar que el usuario sea administrador
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        
        if not request.user.puede_gestionar_usuarios():
            messages.error(request, 'Solo los administradores pueden acceder a esta página.')
            return redirect('bienvenida')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def puede_crear_tipos(view_func):
    """
    Decorador para verificar que el usuario pueda crear tipos de solicitud
    (Control escolar y administrador)
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        
        if not request.user.puede_crear_tipo_solicitud():
            messages.error(request, 'No tienes permiso para crear tipos de solicitud.')
            return redirect('bienvenida')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def puede_atender_solicitudes(view_func):
    """
    Decorador para verificar que el usuario pueda atender solicitudes
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        
        if not request.user.puede_atender_solicitudes():
            messages.error(request, 'No tienes permiso para atender solicitudes.')
            return redirect('bienvenida')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def puede_ver_dashboard(view_func):
    """
    Decorador para verificar que el usuario pueda ver el dashboard
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        
        if not request.user.puede_ver_dashboard():
            messages.error(request, 'Solo los administradores pueden ver el dashboard completo.')
            return redirect('bienvenida')
        
        return view_func(request, *args, **kwargs)
    return wrapper
