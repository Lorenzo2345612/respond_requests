# app/solicitudes/atender_solicitudes/tests/test_forms.py
from django.test import TestCase
from atender_solicitudes.forms import CerrarSolicitudForm

class SmokeAtenderSolicitudesTests(TestCase):
    def test_smoke(self):
        self.assertTrue(True)
        
class CerrarSolicitudFormTests(TestCase):
    def test_form_valido_con_datos_correctos(self):
        data = {
            "estatus": "3",
            "observaciones": "La solicitud fue atendida correctamente."
        }
        form = CerrarSolicitudForm(data=data)
        self.assertTrue(form.is_valid())
        # Se normalizan espacios
        self.assertEqual(form.cleaned_data["estatus"], "3")
        self.assertEqual(
            form.cleaned_data["observaciones"],
            "La solicitud fue atendida correctamente."
        )

    def test_falla_si_estatus_invalido(self):
        data = {
            "estatus": "5",   # valor no permitido
            "observaciones": "Texto cualquiera"
        }
        form = CerrarSolicitudForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("estatus", form.errors)
        self.assertIn("Estatus inválido", str(form.errors["estatus"]))

    def test_falla_si_observaciones_vacias(self):
        data = {
            "estatus": "3",
            "observaciones": "   ",  # solo espacios
        }
        form = CerrarSolicitudForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("observaciones", form.errors)
        self.assertIn("obligatorias", str(form.errors["observaciones"]))