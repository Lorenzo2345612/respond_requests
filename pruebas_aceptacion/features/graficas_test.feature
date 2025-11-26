Feature: Mostrar graficas del dashboard
    Como administrador del sistema
    Deseo ver las graficas mas solicitadas por dia, mes y año 
    Para analizar las tendencias de solicitudes por periodo
    
    Scenario: Acceder a la página de gráficas
        Given que ingreso al sistema
        When hago clic en el menú "Graficas"
        Then deberia ver el titulo "Tendencias de Solicitudes"

    Scenario: Visualizar la gráfica de tendencias de solicitadas de hoy
        Given que ingreso al sistema
        When hago clic en el menú "Graficas"
        Then debería ver la grafica con titulo "Solicitudes de Hoy"
        And la grafica "Solicitudes de Hoy" deberia mostrar datos

    Scenario: Visualizar la gráfica de tendencias de solicitadas de Esta Semana
        Given que ingreso al sistema
        When hago clic en el menú "Graficas"
        Then debería ver la grafica con titulo "Solicitudes de Esta Semana"
        And la grafica "Solicitudes de Esta Semana" deberia mostrar datos

    Scenario: Visualizar la gráfica de tendencias de solicitadas de Este Mes
        Given que ingreso al sistema
        When hago clic en el menú "Graficas"
        Then debería ver la grafica con titulo "Solicitudes de Este Mes"
        And la grafica "Solicitudes de Este Mes" deberia mostrar datos
    
    Scenario: Visualizar todas las gráficas de tendencias al mismo tiempo
        Given que ingreso al sistema
        When hago clic en el menú "Graficas"
        Then debería ver la grafica con titulo "Solicitudes de Hoy"
        And debería ver la grafica con titulo "Solicitudes de Esta Semana"
        And debería ver la grafica con titulo "Solicitudes de Este Mes"

    Scenario: Interactuar con las graficas de tendencias
        Given que ingreso al sistema
        When hago clic en el menú "Graficas"
        And paso el mouse sobre una barra de la grafica con titulo "Solicitudes de Hoy"
        Then deberia aparecer un recuadro con la informacion detallada
        And el recuadro deberia mostrar el tipo de solicitud
        And el recuadro deberia mostrar la cantidad de los tipos de solicitud
