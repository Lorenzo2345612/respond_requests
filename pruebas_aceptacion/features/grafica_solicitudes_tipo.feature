Feature: Gráfica de Solicitudes por Tipo
  Como usuario
  Quiero ver un gráfico que muestre la distribución de solicitudes por tipo
  Para analizar tendencias visualmente

  Scenario: Cargar gráfica con datos correctos
    Given existen varios tipos de solicitud con datos registrados
    When ingreso a la página de métricas
    Then la gráfica de tipo "bar" debe renderizarse
      And las etiquetas deben coincidir con los nombres de los tipos de solicitud
      And los valores deben coincidir con los conteos reales
