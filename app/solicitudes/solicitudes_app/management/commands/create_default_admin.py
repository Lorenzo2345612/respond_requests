from django.core.management.base import BaseCommand
from solicitudes_app.models import Usuario


class Command(BaseCommand):
    help = 'Crea el usuario administrador por defecto si no existe'

    def handle(self, *args, **options):
        username = 'admin'
        password_default = 'admin'

        # Verificar si el usuario admin ya existe
        if Usuario.objects.filter(username=username).exists():
            admin_user = Usuario.objects.get(username=username)

            # Solo resetear si ya cambió la contraseña anteriormente
            # (esto evita resetear en cada reinicio del contenedor)
            if not admin_user.debe_cambiar_password:
                self.stdout.write(
                    self.style.WARNING(
                        f'El usuario "{username}" ya existe y ya cambió su contraseña. '
                        f'No se modificará.'
                    )
                )
                return
            else:
                # El admin existe pero aún no ha cambiado su contraseña
                # Asegurar que tenga la contraseña correcta
                admin_user.set_password(password_default)
                admin_user.debe_cambiar_password = True
                admin_user.perfil_completo = False
                admin_user.save()
                self.stdout.write(
                    self.style.WARNING(
                        f'El usuario "{username}" ya existe. '
                        f'Contraseña verificada y flags reseteados.'
                    )
                )
                return

        # Crear usuario admin por defecto
        admin_user = Usuario.objects.create_user(
            username=username,
            email='admin@solicitudes.local',
            password=password_default,
            first_name='Administrador',
            last_name='Sistema',
            rol='administrador',
            area='Administración General',
            is_staff=True,
            is_superuser=True
        )

        # Marcar que debe cambiar contraseña y completar perfil
        admin_user.debe_cambiar_password = True
        admin_user.perfil_completo = False
        admin_user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Usuario administrador creado exitosamente:\n'
                f'   Usuario: {username}\n'
                f'   Contraseña: {password_default}\n'
                f'IMPORTANTE: Cambia la contraseña en el primer inicio de sesión'
            )
        )
