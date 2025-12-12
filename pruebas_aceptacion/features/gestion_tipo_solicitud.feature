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

    Escenario: Editar tipo de solicitud exitosamente
        Dado que ingreso al sistema
        Y existe un tipo de solicitud con nombre "Tipo Original"
        Y navego a la lista de tipos de solicitudes
        Cuando hago clic en el botón de opciones del tipo "Tipo Original"
        Y selecciono la opción "Editar Tipo de Solicitud"
        Y modifico el campo "nombre" a "Tipo Editado"
        Y modifico el campo "descripcion" a "Descripción actualizada"
        Y presiono el botón "Guardar"
        Entonces soy redirigido a la lista de tipos de solicitudes
        Y puedo ver el tipo "Tipo Editado" en la lista
        Y no veo el tipo "Tipo Original" en la lista

    Escenario: Eliminar tipo de solicitud exitosamente
        Dado que ingreso al sistema
        Y existe un tipo de solicitud con nombre "Tipo a Eliminar"
        Y navego a la lista de tipos de solicitudes
        Cuando hago clic en el botón de opciones del tipo "Tipo a Eliminar"
        Y selecciono la opción "Eliminar Tipo de Solicitud"
        Y confirmo la eliminación en el modal
        Entonces soy redirigido a la lista de tipos de solicitudes
        Y no veo el tipo "Tipo a Eliminar" en la lista
        Y veo un mensaje de éxito de eliminación

    Escenario: Cancelar eliminación de tipo de solicitud
        Dado que ingreso al sistema
        Y existe un tipo de solicitud con nombre "Tipo a Mantener"
        Y navego a la lista de tipos de solicitudes
        Cuando hago clic en el botón de opciones del tipo "Tipo a Mantener"
        Y selecciono la opción "Eliminar Tipo de Solicitud"
        Y cancelo la eliminación en el modal
        Entonces permanezco en la lista de tipos de solicitudes
        Y puedo ver el tipo "Tipo a Mantener" en la lista
