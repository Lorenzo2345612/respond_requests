Feature: Metricas
    Como administrador del sistema
    Quiero ver un panel con métricas clave
    Para revisar el estado de las solicitudes y su distribución

    Scenario: El administrador visualiza el dashboard con métricas principales
        Cuando el administrador inicia sesión y abre "/tipo-solicitud/metricas"
        Entonces debería ver el título "Metricas"
        Y debería ver la línea que muestra "Total de tickets"
        Y debería ver la sección "Solicitudes por tipo"
        Y debería ver la sección "Solicitudes por responsable"
        Y debería existir un elemento con id "trendChart"

    Scenario: Un usuario no administrador no puede acceder a metricas
        Dado que existe un usuario normal con usuario "usuario" y contraseña "userpass"
        Cuando el usuario inicia sesión y abre "/tipo-solicitud/metricas/"
        Entonces debería ser redirigido a la página de login o ver un mensaje de acceso denegado

    Scenario: El dashboard muestra valores numéricos válidos para métricas
        Cuando el administrador inicia sesión y abre "/tipo-solicitud/metricas"
        Entonces el texto junto a "Total de tickets" debería contener un número
        Y la tabla de "Solicitudes por tipo" debería contener al menos una fila o el texto "No hay solicitudes"

    Scenario: Validación de métricas numéricas exactas
        Cuando el administrador inicia sesión y abre "/tipo-solicitud/metricas"
        Entonces el campo "Total de tickets" debería ser "<total>"
        Y el campo "En proceso" debería ser "<en_proceso>"
        Y el campo "Promedio de tiempo de resolución" debería ser "<promedio>"

    Scenario: Conteo por responsable
        Cuando el administrador inicia sesión y abre "/tipo-solicitud/metricas"
        Entonces la fila para el responsable "<responsable>" debería mostrar "<count>"
