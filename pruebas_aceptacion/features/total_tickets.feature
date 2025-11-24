Feature: Métrica - Total de Tickets
  Como usuario que quiere ver las métricas
  Quiero visualizar el total de tickets creados
  Para conocer la carga general del sistema

  Scenario: Mostrar total de tickets correctamente
    Given existen 10 solicitudes registradas
    When ingreso a la página de listar solicitudes
    Then debe mostrarse el número "10" en el filtro "Todos"
