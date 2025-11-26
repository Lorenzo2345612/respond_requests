Feature: Página de bienvenida
    Como usuario logueado
    Quiero ver una página de bienvenida
    Para iniciar a realizar más actividades dentro del sistema.

        Scenario: Ver página de bienvenida
            Given que ingreso al url del sistema
             When me dirijo a raíz /
             Then puedo ver en la página de bienvenida el mensaje "Bienvenid@"
