# app/solicitudes/atender_solicitudes/tests/test_models.py
from django.test import TestCase
from atender_solicitudes.test_data_factory import (
    crear_datos_de_prueba,
    limpiar_datos_de_prueba,
)
from tipo_solicitudes.models import Solicitud, SeguimientoSolicitud, TipoSolicitud


class SolicitudTestDataFactoryTests(TestCase):
    def setUp(self):
        # Creamos un conjunto pequeño de datos para no tardar mucho
        self.datos = crear_datos_de_prueba(usuarios=3, solicitudes=8)

    def test_crea_solicitudes_y_seguimientos(self):
        # Se crearon las solicitudes pedidas
        self.assertEqual(len(self.datos["solicitudes"]), 8)
        self.assertEqual(Solicitud.objects.count(), 8)

        # Cada solicitud debe tener al menos un seguimiento (estatus '1' por defecto)
        for solicitud in self.datos["solicitudes"]:
            self.assertTrue(
                solicitud.seguimientos.exists(),
                msg=f"La solicitud {solicitud.id} no tiene seguimientos",
            )

    def test_crea_tipos_de_solicitud_y_formularios(self):
        # Debe haber varios tipos de solicitud creados
        self.assertGreaterEqual(TipoSolicitud.objects.count(), 3)
        # Cada tipo tiene un formulario asociado (formulario es FK en test_data_factory)
        for tipo in TipoSolicitud.objects.all():
            self.assertIsNotNone(getattr(tipo, "formulario", None))

    def test_limpiar_datos_de_prueba_elimina_todo(self):
        # Llamamos al helper que limpia la BD de los datos creados
        limpiar_datos_de_prueba()
        self.assertEqual(Solicitud.objects.count(), 0)
        self.assertEqual(SeguimientoSolicitud.objects.count(), 0)
        self.assertEqual(TipoSolicitud.objects.count(), 0)