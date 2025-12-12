# language: es
Característica: Alta de tipos de solicitud
    Como usuario de control escolar
    Deseo agregar un nuevo tipo de solicitud
    Para poder crear distintas solicitudes en función del catálogo tipo.

    Escenario: Agregar tipo con datos correctos
        Dado que ingreso al sistema
        Y navego a la lista de tipos de solicitudes
        Cuando hago clic en el botón "Agregar"
        Y lleno el campo "nombre" con "Kardex"
        Y lleno el campo "descripcion" con "Kardex de calificaciones"
        Y selecciono el responsable "Control escolar"
        Y presiono el botón "Guardar"
        Entonces puedo ver el tipo "Kardex" en la lista de tipos de solicitudes