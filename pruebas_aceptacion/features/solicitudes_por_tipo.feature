Feature: Métrica - Solicitudes por Tipo
  Como usuario responsable de análisis
  Quiero visualizar cuántas solicitudes corresponden a cada tipo
  Para identificar áreas con más carga

  Scenario: Mostrar tabla de solicitudes por tipo
    Given existen varios tipos de solicitud con datos registrados
    When ingreso a la página de métricas
    Then la tabla "Solicitudes por Tipo" debe listar cada tipo con su conteo
