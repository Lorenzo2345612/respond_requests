
Feature: Gestión de Login de Usuarios
  Como usuario del sistema
  Quiero poder iniciar sesión con mis credenciales
  Para acceder a las funcionalidades del sistema según mi rol

  Scenario: Login exitoso con credenciales válidas
    Given que existe un usuario con username "alumno_test" y password "testpass123" y rol "alumno"
    When el usuario visita la página de login
    And ingresa username "alumno_test" y password "testpass123"
    And hace clic en el botón de iniciar sesión
    Then el usuario es redirigido a la página de bienvenida
    And ve el mensaje "Bienvenid@"

  Scenario: Login fallido con credenciales incorrectas
    Given que existe un usuario con username "alumno_test" y password "testpass123" y rol "alumno"
    When el usuario visita la página de login
    And ingresa username "alumno_test" y password "wrongpassword"
    And hace clic en el botón de iniciar sesión
    Then el usuario permanece en la página de login
    And ve el mensaje "Usuario o contraseña incorrectos"

  Scenario: Login con usuario inexistente
    When el usuario visita la página de login
    And ingresa username "usuario_inexistente" y password "cualquier_pass"
    And hace clic en el botón de iniciar sesión
    Then el usuario permanece en la página de login
    And ve el mensaje "Usuario o contraseña incorrectos"

  Scenario: Acceso a página protegida sin autenticación
    When el usuario intenta acceder a la página de perfil sin estar autenticado
    Then el usuario es redirigido a la página de login

  Scenario: Logout exitoso
    Given que el usuario "alumno_test" está autenticado
    When el usuario hace clic en cerrar sesión
    Then el usuario es redirigido a la página de login
