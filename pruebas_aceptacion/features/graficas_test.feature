Característica: Mostrar graficas del dashboard
    Como administrador del sistema
    Deseo ver las graficas mas solicitadas por dia, mes y año 
    Para analizar las tendencias de solicitudes por periodo
    
    Escenario: Acceder a la página de gráficas
        Dado que ingreso al sistema
        Cuando hago clic en el menú "Graficas"
        Entonces deberia ver el titulo "Tendencias de Solicitudes"

    Escenario: Visualizar la gráfica de tendencias de solicitadas de hoy
        Dado que ingreso al sistema
        Cuando hago clic en el menú "Graficas"
        Entonces debería ver la grafica con titulo "Solicitudes de Hoy"
        Y la grafica "Solicitudes de Hoy" deberia mostrar datos

    Escenario: Visualizar la gráfica de tendencias de solicitadas de Esta Semana
        Dado que ingreso al sistema
        Cuando hago clic en el menú "Graficas"
        Entonces debería ver la grafica con titulo "Solicitudes de Esta Semana"
        Y la grafica "Solicitudes de Esta Semana" deberia mostrar datos

    Escenario: Visualizar la gráfica de tendencias de solicitadas de Este Mes
        Dado que ingreso al sistema
        Cuando hago clic en el menú "Graficas"
        Entonces debería ver la grafica con titulo "Solicitudes de Este Mes"
        Y la grafica "Solicitudes de Este Mes" deberia mostrar datos
    
    Escenario: Visualizar todas las gráficas de tendencias al mismo tiempo
        Dado que ingreso al sistema
        Cuando hago clic en el menú "Graficas"
        Entonces debería ver la grafica con titulo "Solicitudes de Hoy"
        Y debería ver la grafica con titulo "Solicitudes de Esta Semana"
        Y debería ver la grafica con titulo "Solicitudes de Este Mes"

    Escenario: Interactuar con las graficas de tendencias
        Dado que ingreso al sistema
        Cuando hago clic en el menú "Graficas"
        Y paso el mouse sobre una barra de la grafica con titulo "Solicitudes de Hoy"
        Entonces deberia aparecer un recuadro con la informacion detallada
        Y el recuadro deberia mostrar el tipo de solicitud
        Y el recuadro deberia mostrar la cantidad de los tipos de solicitud
