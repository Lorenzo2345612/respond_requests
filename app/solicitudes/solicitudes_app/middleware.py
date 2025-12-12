from django.shortcuts import redirect
from django.urls import reverse


class CompletarPerfilMiddleware:
    """
    Middleware que redirige a los usuarios que deben cambiar su contraseña
    o completar su perfil
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # URLs que no requieren redirección (permitir acceso sin perfil completo)
        self.urls_permitidas = [
            '/auth/logout/',
            '/auth/perfil/',
            '/auth/cambiar-password/',
            '/admin/',
            '/static/',
            '/media/',
        ]

    def __call__(self, request):
        # Si el usuario está autenticado
        if request.user.is_authenticated:
            # Verificar si la URL actual está en las permitidas
            ruta_actual = request.path
            es_url_permitida = any(ruta_actual.startswith(url)
                                   for url in self.urls_permitidas)

            # Si debe cambiar contraseña y no está en la página de cambio
            if request.user.debe_cambiar_password and not es_url_permitida:
                if ruta_actual != reverse('solicitudes_app:cambiar_password'):
                    return redirect('solicitudes_app:cambiar_password')

            # Si no tiene perfil completo y no está en las páginas permitidas
            elif not request.user.perfil_completo and not es_url_permitida:
                if ruta_actual != reverse('solicitudes_app:perfil'):
                    return redirect('solicitudes_app:perfil')

        response = self.get_response(request)
        return response
