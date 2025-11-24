Feature: Métrica - Solicitudes por Estatus
  Como administrador
  Quiero visualizar cuántas solicitudes hay por cada estatus
  Para entender el flujo del sistema

  Scenario: Mostrar tabla de solicitudes por estatus
    Given existen solicitudes en estatus Creada, En proceso y Terminada
    When ingreso al dashboard de métricas
    Then debo ver una tabla con el conteo agrupado por estatus
