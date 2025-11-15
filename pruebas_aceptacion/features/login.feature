# language: es
Funcionalidad: Gestión de Login de Usuarios
  Como usuario del sistema
  Quiero poder iniciar sesión con mis credenciales
  Para acceder a las funcionalidades del sistema según mi rol

  Escenario: Login exitoso con credenciales válidas
    Dado que existe un usuario con username "alumno_test" y password "testpass123" y rol "alumno"
    Cuando el usuario visita la página de login
    Y ingresa username "alumno_test" y password "testpass123"
    Y hace clic en el botón de iniciar sesión
    Entonces el usuario es redirigido a la página de bienvenida
    Y ve el mensaje "¡Bienvenido"

  Escenario: Login fallido con credenciales incorrectas
    Dado que existe un usuario con username "alumno_test" y password "testpass123" y rol "alumno"
    Cuando el usuario visita la página de login
    Y ingresa username "alumno_test" y password "wrongpassword"
    Y hace clic en el botón de iniciar sesión
    Entonces el usuario permanece en la página de login
    Y ve el mensaje "Usuario o contraseña incorrectos"

  Escenario: Login con usuario inexistente
    Cuando el usuario visita la página de login
    Y ingresa username "usuario_inexistente" y password "cualquier_pass"
    Y hace clic en el botón de iniciar sesión
    Entonces el usuario permanece en la página de login
    Y ve el mensaje "Usuario o contraseña incorrectos"

  Escenario: Acceso a página protegida sin autenticación
    Cuando el usuario intenta acceder a la página de perfil sin estar autenticado
    Entonces el usuario es redirigido a la página de login

  Escenario: Logout exitoso
    Dado que el usuario "alumno_test" está autenticado
    Cuando el usuario hace clic en cerrar sesión
    Entonces el usuario es redirigido a la página de login
    Y ve el mensaje "Has cerrado sesión exitosamente"
