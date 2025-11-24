
Feature: Registro de Nuevos Usuarios
  Como visitante del sistema
  Quiero poder registrarme con mi información personal
  Para crear una cuenta y acceder al sistema

  Scenario: Registro exitoso de alumno con todos los datos requeridos
    When el usuario visita la página de registro
    And completa el formulario con los siguientes datos de alumno:
      | Campo       | Valor               |
      | username    | nuevo_alumno        |
      | email       | alumno@test.com     |
      | first_name  | Nuevo               |
      | last_name   | Alumno              |
      | rol         | alumno              |
      | matricula   | 12345               |
      | telefono    | 4921234567          |
      | password1   | testpass123!        |
      | password2   | testpass123!        |
    And hace clic en el botón de registrar
    Then el usuario es redirigido a la página de bienvenida
    And el usuario está autenticado
    And existe un usuario en la base de datos con username "nuevo_alumno"

  Scenario: Registro fallido de alumno sin matrícula
    When el usuario visita la página de registro
    And completa el formulario con los siguientes datos de alumno:
      | Campo       | Valor               |
      | username    | alumno_sin_mat      |
      | email       | sin_mat@test.com    |
      | first_name  | Sin                 |
      | last_name   | Matricula           |
      | rol         | alumno              |
      | matricula   |                     |
      | password1   | testpass123!        |
      | password2   | testpass123!        |
    And hace clic en el botón de registrar
    Then el usuario permanece en la página de registro
    And ve un error indicando que la matrícula es obligatoria para alumnos

  Scenario: Registro exitoso de administrador
    When el usuario visita la página de registro
    And completa el formulario con los siguientes datos de administrador:
      | Campo       | Valor               |
      | username    | nuevo_admin         |
      | email       | admin@test.com      |
      | first_name  | Nuevo               |
      | last_name   | Admin               |
      | rol         | administrador       |
      | area        | TI                  |
      | password1   | testpass123!        |
      | password2   | testpass123!        |
    And hace clic en el botón de registrar
    Then el usuario es redirigido a la página de bienvenida
    And existe en la base de datos un usuario con username "nuevo_admin" y rol "administrador"

  Scenario: Registro fallido con email duplicado
    Given que existe un usuario con email "duplicado@test.com"
    When el usuario visita la página de registro
    And completa el formulario con email "duplicado@test.com"
    And hace clic en el botón de registrar
    Then el usuario permanece en la página de registro
    And ve un error indicando que el email ya está registrado

  Scenario: Registro fallido con contraseñas que no coinciden
    When el usuario visita la página de registro
    And ingresa contraseñas diferentes en password1 y password2
    And hace clic en el botón de registrar
    Then el usuario permanece en la página de registro
    And ve un error de contraseñas no coincidentes
