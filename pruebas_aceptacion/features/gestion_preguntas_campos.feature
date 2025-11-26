# language: es
Característica: Gestión de preguntas/campos en formularios
    Como usuario de control escolar
    Deseo agregar y gestionar campos en los formularios
    Para poder personalizar la información que se solicita

    Antecedentes:
        Dado que ingreso al sistema
        Y existe un formulario llamado "Formulario de Prueba"
        Y navego a la página de agregar preguntas del formulario "Formulario de Prueba"

    Escenario: Agregar pregunta de tipo texto corto exitosamente
        Cuando lleno el campo de pregunta "nombre" con "nombre_completo"
        Y lleno el campo de pregunta "etiqueta" con "Nombre completo del estudiante"
        Y selecciono el tipo de campo "Texto corto"
        Y marco el campo como requerido
        Y lleno el campo "orden" con "1"
        Y presiono el botón "Agregar campo"
        Entonces veo la pregunta "Nombre completo del estudiante" en la tabla de campos agregados
        Y el tipo de campo mostrado es "Texto corto"
        Y el campo aparece marcado como requerido

    Escenario: Agregar pregunta de tipo texto largo exitosamente
        Cuando lleno el campo de pregunta "nombre" con "justificacion"
        Y lleno el campo de pregunta "etiqueta" con "Justificación de la solicitud"
        Y selecciono el tipo de campo "Texto largo"
        Y marco el campo como requerido
        Y lleno el campo "orden" con "2"
        Y presiono el botón "Agregar campo"
        Entonces veo la pregunta "Justificación de la solicitud" en la tabla de campos agregados
        Y el tipo de campo mostrado es "Texto largo"

    Escenario: Agregar pregunta de tipo número exitosamente
        Cuando lleno el campo de pregunta "nombre" con "matricula"
        Y lleno el campo de pregunta "etiqueta" con "Número de matrícula"
        Y selecciono el tipo de campo "Número"
        Y marco el campo como requerido
        Y lleno el campo "orden" con "1"
        Y presiono el botón "Agregar campo"
        Entonces veo la pregunta "Número de matrícula" en la tabla de campos agregados
        Y el tipo de campo mostrado es "Número"

    Escenario: Agregar pregunta de tipo fecha exitosamente
        Cuando lleno el campo de pregunta "nombre" con "fecha_inicio"
        Y lleno el campo de pregunta "etiqueta" con "Fecha de inicio del periodo"
        Y selecciono el tipo de campo "Fecha"
        Y marco el campo como requerido
        Y lleno el campo "orden" con "3"
        Y presiono el botón "Agregar campo"
        Entonces veo la pregunta "Fecha de inicio del periodo" en la tabla de campos agregados
        Y el tipo de campo mostrado es "Fecha"

    Escenario: Agregar pregunta de tipo selección con opciones
        Cuando lleno el campo de pregunta "nombre" con "semestre"
        Y lleno el campo de pregunta "etiqueta" con "Semestre actual"
        Y selecciono el tipo de campo "Selección"
        Y lleno el campo "opciones" con "1,2,3,4,5,6,7,8,9"
        Y marco el campo como requerido
        Y lleno el campo "orden" con "4"
        Y presiono el botón "Agregar campo"
        Entonces veo la pregunta "Semestre actual" en la tabla de campos agregados
        Y el tipo de campo mostrado es "Selección"
        Y las opciones del campo se muestran correctamente

    Escenario: Agregar pregunta de tipo archivo con cantidad especificada
        Cuando lleno el campo de pregunta "nombre" con "comprobante"
        Y lleno el campo de pregunta "etiqueta" con "Comprobante de pago"
        Y selecciono el tipo de campo "Archivo"
        Y especifico la cantidad de archivos como "2"
        Y marco el campo como requerido
        Y lleno el campo "orden" con "5"
        Y presiono el botón "Agregar campo"
        Entonces veo la pregunta "Comprobante de pago" en la tabla de campos agregados
        Y el tipo de campo mostrado es "Archivo"
        Y la cantidad de archivos permitidos es "2"

    Escenario: Agregar campo no requerido
        Cuando lleno el campo de pregunta "nombre" con "comentarios"
        Y lleno el campo de pregunta "etiqueta" con "Comentarios adicionales"
        Y selecciono el tipo de campo "Texto largo"
        Y desmarco el campo como requerido
        Y lleno el campo "orden" con "10"
        Y presiono el botón "Agregar campo"
        Entonces veo la pregunta "Comentarios adicionales" en la tabla de campos agregados
        Y el campo aparece marcado como no requerido

    Escenario: Error al dejar el nombre del campo vacío
        Cuando dejo el campo de pregunta "nombre" vacío
        Y lleno el campo de pregunta "etiqueta" con "Etiqueta de prueba"
        Y selecciono el tipo de campo "Texto corto"
        Y lleno el campo "orden" con "1"
        Y presiono el botón "Agregar campo"
        Entonces veo un mensaje de error indicando que el nombre es obligatorio
        Y permanezco en la página de agregar preguntas

    Escenario: Error al dejar la etiqueta vacía
        Cuando lleno el campo de pregunta "nombre" con "campo_prueba"
        Y dejo el campo de pregunta "etiqueta" vacío
        Y selecciono el tipo de campo "Texto corto"
        Y lleno el campo "orden" con "1"
        Y presiono el botón "Agregar campo"
        Entonces veo un mensaje de error indicando que la etiqueta es obligatoria
        Y permanezco en la página de agregar preguntas

    Escenario: Error al no especificar el tipo de campo
        Cuando lleno el campo de pregunta "nombre" con "campo_sin_tipo"
        Y lleno el campo de pregunta "etiqueta" con "Campo sin tipo"
        Y no selecciono ningún tipo de campo
        Y lleno el campo "orden" con "1"
        Y presiono el botón "Agregar campo"
        Entonces veo un mensaje de error indicando que debe seleccionar un tipo de campo
        Y permanezco en la página de agregar preguntas

    Escenario: Error al usar un número de orden duplicado
        Y existe un campo con orden "1"
        Cuando lleno el campo de pregunta "nombre" con "campo_duplicado"
        Y lleno el campo de pregunta "etiqueta" con "Campo con orden duplicado"
        Y selecciono el tipo de campo "Texto corto"
        Y lleno el campo "orden" con "1"
        Y presiono el botón "Agregar campo"
        Entonces veo un mensaje de error indicando que el orden ya está en uso
        Y permanezco en la página de agregar preguntas

    Escenario: Error al no proporcionar opciones para campo de selección
        Cuando lleno el campo de pregunta "nombre" con "campo_select"
        Y lleno el campo de pregunta "etiqueta" con "Campo de selección sin opciones"
        Y selecciono el tipo de campo "Selección"
        Y dejo el campo "opciones" vacío
        Y lleno el campo "orden" con "6"
        Y presiono el botón "Agregar campo"
        Entonces veo un mensaje de error o advertencia sobre las opciones faltantes
        Y permanezco en la página de agregar preguntas

    Escenario: Eliminar una pregunta exitosamente
        Y existe un campo llamado "Campo a Eliminar"
        Cuando hago clic en el botón eliminar del campo "Campo a Eliminar"
        Entonces el campo "Campo a Eliminar" ya no aparece en la tabla de campos agregados
        Y veo una confirmación de eliminación exitosa

    Escenario: Ver lista de campos agregados vacía
        Y no existen campos agregados todavía
        Entonces veo el mensaje "No hay campos agregados todavía."

    Escenario: Agregar múltiples campos y verificar orden
        Y existen campos con orden "1", "2", "3"
        Cuando visualizo la tabla de campos agregados
        Entonces los campos aparecen ordenados por su número de orden
        Y puedo ver al menos 3 campos en la tabla

    Escenario: Cancelar la adición de campos y volver a la lista
        Cuando presiono el botón "Cancelar" en la página de preguntas
        Entonces soy redirigido a la lista de formularios
        Y no se guardaron los cambios realizados

    Escenario: Campo de opciones solo visible para tipo selección
        Cuando selecciono el tipo de campo "Texto corto"
        Entonces el campo "opciones" no es visible
        Cuando selecciono el tipo de campo "Selección"
        Entonces el campo "opciones" es visible

    Escenario: Campo de cantidad de archivos solo visible para tipo archivo
        Cuando selecciono el tipo de campo "Texto corto"
        Entonces el campo "cantidad_archivos" no es visible
        Cuando selecciono el tipo de campo "Archivo"
        Entonces el campo "cantidad_archivos" es visible
