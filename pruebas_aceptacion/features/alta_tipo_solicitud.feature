Feature: Alta de tipos de solicitud
    Como usuario de control escolar
              Deseo agregar un nuevo tipo de solicitud
    Para poder crear distintas solicitudes en función del catálogo tipo.

        Scenario: Agregar tipo con datos correctos.
            Given que ingreso al sistema
              And seleccion el menú Tipo de solicitudes
              And escribo en la caja de texto nombre "Kardex" y en la descripción "Kardex de calificaciones"
             When presiono el botón Agregar
             Then puedo ver el tipo "Kardex" en la lista de tipos de solicitudes.