# language: es
Funcionalidad: Registro de Nuevos Usuarios
  Como visitante del sistema
  Quiero poder registrarme con mi información personal
  Para crear una cuenta y acceder al sistema

  Escenario: Registro exitoso de alumno con todos los datos requeridos
    Cuando el usuario visita la página de registro
    Y completa el formulario con los siguientes datos de alumno:
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
    Y hace clic en el botón de registrar
    Entonces el usuario es redirigido a la página de bienvenida
    Y el usuario está autenticado
    Y existe un usuario en la base de datos con username "nuevo_alumno"

  Escenario: Registro fallido de alumno sin matrícula
    Cuando el usuario visita la página de registro
    Y completa el formulario con los siguientes datos de alumno:
      | Campo       | Valor               |
      | username    | alumno_sin_mat      |
      | email       | sin_mat@test.com    |
      | first_name  | Sin                 |
      | last_name   | Matricula           |
      | rol         | alumno              |
      | matricula   |                     |
      | password1   | testpass123!        |
      | password2   | testpass123!        |
    Y hace clic en el botón de registrar
    Entonces el usuario permanece en la página de registro
    Y ve un error indicando que la matrícula es obligatoria para alumnos

  Escenario: Registro exitoso de administrador
    Cuando el usuario visita la página de registro
    Y completa el formulario con los siguientes datos de administrador:
      | Campo       | Valor               |
      | username    | nuevo_admin         |
      | email       | admin@test.com      |
      | first_name  | Nuevo               |
      | last_name   | Admin               |
      | rol         | administrador       |
      | area        | TI                  |
      | password1   | testpass123!        |
      | password2   | testpass123!        |
    Y hace clic en el botón de registrar
    Entonces el usuario es redirigido a la página de bienvenida
    Y existe un usuario en la base de datos con username "nuevo_admin" y rol "administrador"

  Escenario: Registro fallido con email duplicado
    Dado que existe un usuario con email "duplicado@test.com"
    Cuando el usuario visita la página de registro
    Y completa el formulario con email "duplicado@test.com"
    Y hace clic en el botón de registrar
    Entonces el usuario permanece en la página de registro
    Y ve un error indicando que el email ya está registrado

  Escenario: Registro fallido con contraseñas que no coinciden
    Cuando el usuario visita la página de registro
    Y ingresa contraseñas diferentes en password1 y password2
    Y hace clic en el botón de registrar
    Entonces el usuario permanece en la página de registro
    Y ve un error de contraseñas no coincidentes
