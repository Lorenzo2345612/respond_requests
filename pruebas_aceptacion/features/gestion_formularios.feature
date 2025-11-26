# language: es
Característica: Gestión de formularios de solicitud
    Como usuario de control escolar
    Deseo gestionar formularios de solicitud
    Para poder crear y configurar formularios asociados a tipos de solicitud

    Escenario: Agregar formulario de solicitud con datos correctos
        Dado que ingreso al sistema
        Y navego a la lista de formularios
        Cuando hago clic en el botón "Agregar"
        Y selecciono el tipo de solicitud "Constancia"
        Y lleno el campo formulario "nombre" con "Formulario de Constancia"
        Y lleno el campo formulario "descripcion" con "Formulario para solicitar constancias de estudio"
        Y presiono el botón "Crear Formulario"
        Entonces soy redirigido a la lista de formularios
        Y puedo ver el formulario "Formulario de Constancia" en la lista de formularios

    Escenario: Crear formulario exitosamente
        Dado que ingreso al sistema
        Y navego a la lista de formularios
        Cuando hago clic en el botón "Agregar"
        Y selecciono el tipo de solicitud "Beca"
        Y lleno el campo formulario "nombre" con "Formulario de Beca Académica"
        Y lleno el campo formulario "descripcion" con "Complete todos los campos requeridos"
        Y presiono el botón "Crear Formulario"
        Entonces veo el formulario "Formulario de Beca Académica" en la lista
        Y el contador de formularios aumenta en 1

    Escenario: Error al dejar el nombre del formulario vacío
        Dado que ingreso al sistema
        Y navego a la lista de formularios
        Cuando hago clic en el botón "Agregar"
        Y selecciono el tipo de solicitud "Constancia"
        Y dejo el campo formulario "nombre" vacío
        Y lleno el campo formulario "descripcion" con "Descripción de prueba"
        Y presiono el botón "Crear Formulario"
        Entonces veo un mensaje de error en el campo nombre del formulario
        Y permanezco en la página de crear formulario

    Escenario: Error al no seleccionar tipo de solicitud
        Dado que ingreso al sistema
        Y navego a la lista de formularios
        Cuando hago clic en el botón "Agregar"
        Y no selecciono ningún tipo de solicitud
        Y lleno el campo formulario "nombre" con "Formulario sin tipo"
        Y lleno el campo formulario "descripcion" con "Descripción de prueba"
        Y presiono el botón "Crear Formulario"
        Entonces veo un mensaje de error indicando que debe seleccionar un tipo de solicitud
        Y permanezco en la página de crear formulario

    Escenario: Cancelar la creación de un formulario
        Dado que ingreso al sistema
        Y navego a la lista de formularios
        Cuando hago clic en el botón "Agregar"
        Y selecciono el tipo de solicitud "Constancia"
        Y lleno el campo formulario "nombre" con "Formulario Temporal"
        Y lleno el campo formulario "descripcion" con "Este no se guardará"
        Y presiono el botón de cancelar en formulario
        Entonces soy redirigido a la lista de formularios
        Y no veo el formulario "Formulario Temporal" en la lista

    Escenario: Editar formulario exitosamente
        Dado que ingreso al sistema
        Y existe un formulario llamado "Formulario Original"
        Y navego a la lista de formularios
        Cuando hago clic en el botón de opciones del formulario "Formulario Original"
        Y selecciono la opción "Editar Formulario"
        Y modifico el campo formulario "nombre" a "Formulario Editado"
        Y modifico el campo formulario "descripcion" a "Descripción actualizada"
        Y presiono el botón "Guardar Cambios"
        Entonces soy redirigido a la lista de formularios
        Y puedo ver el formulario "Formulario Editado" en la lista de formularios
        Y no veo el formulario "Formulario Original" en la lista

    Escenario: Error al editar formulario dejando el nombre vacío
        Dado que ingreso al sistema
        Y existe un formulario llamado "Formulario a Editar"
        Y navego a la lista de formularios
        Cuando hago clic en el botón de opciones del formulario "Formulario a Editar"
        Y selecciono la opción "Editar Formulario"
        Y limpio el campo formulario "nombre"
        Y presiono el botón "Guardar Cambios"
        Entonces veo un mensaje de error en el campo nombre del formulario
        Y permanezco en la página de editar formulario

    Escenario: Cancelar la edición de un formulario
        Dado que ingreso al sistema
        Y existe un formulario llamado "Formulario a Cancelar"
        Y navego a la lista de formularios
        Cuando hago clic en el botón de opciones del formulario "Formulario a Cancelar"
        Y selecciono la opción "Editar Formulario"
        Y modifico el campo formulario "nombre" a "Cambio No Guardado"
        Y presiono el botón de cancelar en formulario
        Entonces soy redirigido a la lista de formularios
        Y puedo ver el formulario "Formulario a Cancelar" en la lista de formularios
        Y no veo el formulario "Cambio No Guardado" en la lista

    Escenario: Acceder a agregar preguntas desde la lista de formularios
        Dado que ingreso al sistema
        Y existe un formulario llamado "Formulario con Preguntas"
        Y navego a la lista de formularios
        Cuando hago clic en el botón de opciones del formulario "Formulario con Preguntas"
        Y selecciono la opción "Agregar Preguntas"
        Entonces soy redirigido a la página de configurar campos
        Y veo el título "Configurar campos del formulario: Formulario con Preguntas"
