# language: es
Funcionalidad: Gestión de Usuarios por Administrador
  Como administrador del sistema
  Quiero poder gestionar los usuarios registrados
  Para mantener control sobre quién tiene acceso al sistema

  Antecedentes:
    Dado que existe un administrador con username "admin" y password "adminpass123"
    Y el administrador "admin" está autenticado

  Escenario: Visualizar lista de usuarios
    Dado que existen los siguientes usuarios en el sistema:
      | username  | email           | rol                    |
      | alumno1   | al1@test.com    | alumno                 |
      | control1  | con1@test.com   | control_escolar        |
      | director1 | dir1@test.com   | director               |
    Cuando el administrador visita la página de gestión de usuarios
    Entonces ve una lista con 4 usuarios
    Y ve el usuario "alumno1" en la lista
    Y ve el usuario "control1" en la lista
    Y ve el usuario "director1" en la lista

  Escenario: Editar información de un usuario
    Dado que existe un usuario con username "alumno_edit" y email "antes@test.com"
    Cuando el administrador visita la página de edición del usuario "alumno_edit"
    Y cambia el email a "despues@test.com"
    Y cambia el first_name a "Editado"
    Y guarda los cambios
    Entonces el usuario "alumno_edit" tiene email "despues@test.com"
    Y el usuario "alumno_edit" tiene first_name "Editado"

  Escenario: Cambiar el rol de un usuario
    Dado que existe un usuario con username "cambio_rol" y rol "alumno"
    Cuando el administrador visita la página de edición del usuario "cambio_rol"
    Y cambia el rol a "control_escolar"
    Y guarda los cambios
    Entonces el usuario "cambio_rol" tiene rol "control_escolar"

  Escenario: Desactivar un usuario
    Dado que existe un usuario con username "usuario_activo" y está activo
    Cuando el administrador visita la página de edición del usuario "usuario_activo"
    Y marca el usuario como inactivo
    Y guarda los cambios
    Entonces el usuario "usuario_activo" está inactivo

  Escenario: Eliminar un usuario
    Dado que existe un usuario con username "usuario_eliminar"
    Cuando el administrador visita la página de gestión de usuarios
    Y elimina el usuario "usuario_eliminar"
    Entonces no existe un usuario con username "usuario_eliminar" en la base de datos

  Escenario: Administrador no puede eliminarse a sí mismo
    Cuando el administrador visita la página de gestión de usuarios
    Entonces no ve el botón de eliminar junto a su propio usuario

  Escenario: Usuario no administrador no puede acceder a gestión de usuarios
    Dado que existe un usuario con username "alumno_no_admin" y password "pass123" y rol "alumno"
    Y el usuario "alumno_no_admin" está autenticado
    Cuando el usuario intenta acceder a la página de gestión de usuarios
    Entonces el usuario es redirigido a la página de bienvenida
    Y ve el mensaje "No tienes permiso para acceder a esta página"
