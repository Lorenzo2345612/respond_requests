Feature: Métrica - Promedio de tiempo de resolución
  Como usuario administrador
  Quiero ver el tiempo promedio de resolución de las solicitudes
  Para evaluar eficiencia de respuesta

  Scenario: Se muestra un promedio válido cuando existen tickets resueltos
    Given existen solicitudes con tiempos de resolución calculables
    When ingreso a la página de métricas
    Then se debe mostrar un valor numérico en "Promedio Resolución"

  Scenario: No se muestra promedio cuando no hay tickets resueltos
    Given no existen solicitudes completadas
    When ingreso a la página de métricas
    Then debe mostrarse "Pendiente" en "Promedio Resolución"
