Característica: Visualización y seguimiento de solicitudes
  Como usuario del sistema
  Quiero ver mis solicitudes y su historial
  Para conocer su progreso real

  Escenario: Ver listado de solicitudes existentes
    Dado que estoy en la página de listado de solicitudes
    Entonces debo ver una tabla con al menos una solicitud

  Escenario: Acceder al detalle de una solicitud
    Dado que estoy en la página de listado de solicitudes
    Cuando hago clic en el botón "Atender" de la primera solicitud
    Entonces debo ver el detalle de la solicitud
    Y debo ver un historial de seguimiento con al menos un registro

  Escenario: Filtrar solicitudes por estado específico
    Dado que estoy en la página de listado de solicitudes
    Cuando aplico filtro por estado "Cancelada"
    Entonces solo veo las solicitudes en estado "Cancelada"

  Escenario: Buscar un folio específico
    Dado que estoy en la página de listado de solicitudes
    Cuando escribo "FOLIO12345" en el buscador de folios
    Entonces debo ver en la tabla una fila con el folio "FOLIO12345"
