# language: es
Característica: Gestión completa de tipos de solicitud
    Como usuario de control escolar
    Deseo gestionar tipos de solicitud
    Para poder crear, editar y administrar el catálogo de solicitudes

    Escenario: Agregar tipo de solicitud con datos correctos
        Dado que ingreso al sistema
        Y navego a la lista de tipos de solicitudes
        Y hago clic en el menú "Tipo solicitudes"
        Cuando lleno el campo "nombre" con "Constancia de Estudios"
        Y lleno el campo "descripcion" con "Constancia para validar que el estudiante está inscrito"
        Y selecciono el responsable "Control escolar"
        Y presiono el botón "Guardar"
        Entonces puedo ver el tipo "Constancia de Estudios" en la lista de tipos de solicitudes
        Y veo un mensaje de éxito

    Escenario: Guardar nuevo tipo de solicitud exitosamente
        Dado que ingreso al sistema
        Y navego a la lista de tipos de solicitudes
        Y hago clic en el menú "Tipo solicitudes"
        Cuando lleno el campo "nombre" con "Carta de Recomendación"
        Y lleno el campo "descripcion" con "Carta de recomendación para trámites externos"
        Y selecciono el responsable "Director"
        Y presiono el botón "Guardar"
        Entonces soy redirigido a la lista de tipos de solicitudes
        Y puedo ver el tipo "Carta de Recomendación" en la lista
        Y el contador de resultados aumenta en 1

    Escenario: Error al dejar campos requeridos vacíos
        Dado que ingreso al sistema
        Y navego a la lista de tipos de solicitudes
        Y hago clic en el menú "Tipo solicitudes"
        Cuando dejo el campo "nombre" vacío
        Y lleno el campo "descripcion" con "Alguna descripción"
        Y presiono el botón "Guardar"
        Entonces veo un mensaje de error indicando que el campo nombre es obligatorio
        Y permanezco en la página de agregar tipo de solicitud

    Escenario: Error al ingresar nombre duplicado
        Dado que ingreso al sistema
        Y navego a la lista de tipos de solicitudes
        Y hago clic en el menú "Tipo solicitudes"
        Y existe un tipo de solicitud con nombre "Beca Académica"
        Cuando lleno el campo "nombre" con "Beca Académica"
        Y lleno el campo "descripcion" con "Otra descripción"
        Y presiono el botón "Guardar"
        Entonces veo un mensaje de error indicando que el nombre ya existe
        Y permanezco en la página de agregar tipo de solicitud

    Escenario: Cancelar la creación de un tipo de solicitud
        Dado que ingreso al sistema
        Y navego a la lista de tipos de solicitudes
        Y hago clic en el menú "Tipo solicitudes"
        Cuando lleno el campo "nombre" con "Solicitud Temporal"
        Y lleno el campo "descripcion" con "Esta no se guardará"
        Y presiono el botón "Cancelar"
        Entonces soy redirigido a la lista de tipos de solicitudes
        Y no veo el tipo "Solicitud Temporal" en la lista

#    Escenario: Error al exceder el límite de caracteres en nombre
#        Dado que ingreso al sistema
#        Y navego a la lista de tipos de solicitudes
#        Y hago clic en el menú "Tipo solicitudes"
#        Cuando lleno el campo "nombre" con un texto de 200 caracteres
#        Y lleno el campo "descripcion" con "Descripción válida"
#        Y presiono el botón "Guardar"
#        Entonces veo un mensaje de error por exceder el límite de caracteres
#        Y permanezco en la página de agregar tipo de solicitud
#
#    Escenario: Error al exceder el límite de caracteres en descripción
#        Dado que ingreso al sistema
#        Y navego a la lista de tipos de solicitudes
#        Y hago clic en el menú "Tipo solicitudes"
#        Cuando lleno el campo "nombre" con "Nombre válido"
#        Y lleno el campo "descripcion" con un texto de 400 caracteres
#        Y presiono el botón "Guardar"
#        Entonces veo un mensaje de error por exceder el límite de caracteres en descripción
#        Y permanezco en la página de agregar tipo de solicitud
