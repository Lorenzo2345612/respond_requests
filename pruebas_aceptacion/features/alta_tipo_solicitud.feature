# language: es
Característica: Alta de tipos de solicitud
    Como usuario de control escolar
    Deseo agregar un nuevo tipo de solicitud
    Para poder crear distintas solicitudes en función del catálogo tipo.

    Escenario: Agregar tipo con datos correctos
        Dado que ingreso al sistema
        Y seleccion el menú Tipo de solicitudes
        Y escribo en la caja de texto nombre "Kardex" y en la descripción "Kardex de calificaciones"
        Cuando presiono el botón Agregar
        Entonces puedo ver el tipo "Kardex" en la lista de tipos de solicitudes.