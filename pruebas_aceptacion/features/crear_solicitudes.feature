Feature: Gestión de solicitudes
  Como alumno
  Quiero crear y visualizar solicitudes
  Para dar seguimiento a mis trámites

  Scenario: Crear una nueva solicitud
    Given que el usuario inició sesión
    And existe un tipo de solicitud con formulario
    When llena los campos requeridos y envía el formulario
    Then la solicitud se guarda exitosamente en la base de datos

  Scenario: Visualizar mis solicitudes
    Given que el usuario tiene solicitudes registradas
    When accede a la pantalla de "Mis solicitudes"
    Then puede ver la lista de solicitudes realizadas

  Scenario: Ver detalle y seguimiento de una solicitud
    Given que el usuario tiene una solicitud creada
    And existen registros de seguimiento
    When accede al detalle de la solicitud
    Then puede ver los campos llenados y el historial de seguimiento