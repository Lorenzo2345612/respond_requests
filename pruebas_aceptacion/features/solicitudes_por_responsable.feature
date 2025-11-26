Feature: Métrica - Solicitudes por Responsable
  Como administrador
  Quiero ver cuántas solicitudes están asignadas a cada responsable
  Para evaluar cargas de trabajo

  Scenario: Mostrar métricas por responsable
    Given existen solicitudes asignadas a varios responsables
    When ingreso a la página de métricas
    Then debo ver una tabla que muestre el responsable y el total asignado
