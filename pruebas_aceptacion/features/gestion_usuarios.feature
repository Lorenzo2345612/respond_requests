Feature: Gestión de Usuarios por Administrador
  Como administrador del sistema
  Quiero poder gestionar los usuarios registrados
  Para mantener control sobre quién tiene acceso al sistema

  Background:
    Given que existe un administrador con username "admin" y password "adminpass123"
    And el administrador "admin" está autenticado

  Scenario: Visualizar lista de usuarios
    Given que existen los siguientes usuarios en el sistema:
      | username  | email           | rol                    |
      | alumno1   | al1@test.com    | alumno                 |
      | control1  | con1@test.com   | control_escolar        |
      | director1 | dir1@test.com   | director               |
    When el administrador visita la página de gestión de usuarios
    Then ve una lista con 4 usuarios
    And ve el usuario "alumno1" en la lista
    And ve el usuario "control1" en la lista
    And ve el usuario "director1" en la lista

  Scenario: Editar información de un usuario
    Given que existe previamente un usuario con username "alumno_edit" y email "antes@test.com"
    When el administrador visita la página de edición del usuario "alumno_edit"
    And cambia el email a "despues@test.com"
    And cambia el first_name a "Editado"
    And guarda los cambios
    Then el usuario "alumno_edit" tiene email "despues@test.com"
    And el usuario "alumno_edit" tiene first_name "Editado"

  Scenario: Cambiar el rol de un usuario
    Given que existe un usuario registrado con username "cambio_rol" y rol "alumno"
    When el administrador visita la página de edición del usuario "cambio_rol"
    And cambia el rol a "control_escolar"
    And guarda los cambios
    Then el usuario "cambio_rol" tiene rol "control_escolar"

  Scenario: Desactivar usuario
    Given que existe previamente un usuario con username "usuario_activo" y está activo
    When el administrador visita la página de edición del usuario "usuario_activo"
    And marca el usuario como inactivo
    And guarda los cambios
    Then el usuario "usuario_activo" está inactivo

  Scenario: Eliminar un usuario
    Given que existe previamente un usuario con username "usuario_eliminar"
    When el administrador visita la página de gestión de usuarios
    And elimina el usuario "usuario_eliminar"
    Then no existe un usuario con username "usuario_eliminar" en la base de datos

  Scenario: Administrador no puede eliminarse a sí mismo
    When el administrador visita la página de gestión de usuarios
    Then no ve el botón de eliminar junto a su propio usuario

  Scenario: Usuario no administrador no puede acceder a gestión de usuarios
    Given que existe un usuario con username "alumno_no_admin" y password "pass123" y rol "alumno"
    And el usuario "alumno_no_admin" está autenticado
    When el usuario intenta acceder a la página de gestión de usuarios
    Then el usuario es redirigido a la página de bienvenida

