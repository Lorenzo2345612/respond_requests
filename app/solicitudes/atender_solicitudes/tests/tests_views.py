import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tipo_solicitudes.models import Solicitud, TipoSolicitud, SeguimientoSolicitud


class AtenderSolicitudesViewsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        # Usuario "responsable"
        self.usuario = User.objects.create_user(
            username="responsable", password="pass1234"
        )

        # Tipo de solicitud mínimo
        self.tipo = TipoSolicitud.objects.create(
            nombre="Constancia de estudios",
            descripcion="Prueba",
            responsable="1",  # mismo valor que usan en test_data_factory
        )

        # Solicitud base
        self.solicitud = Solicitud.objects.create(
            usuario=self.usuario,
            tipo_solicitud=self.tipo,
            folio="SOL-TEST-0001",
        )

    # ---------- atender_solicitud ----------

    def test_atender_solicitud_get_ok(self):
        seg = SeguimientoSolicitud.objects.create(
            solicitud=self.solicitud,
            estatus="1",
            observaciones="Creada",
        )

        url = reverse("atender_solicitud", args=[self.solicitud.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "atender_solicitud.html")
        self.assertIn("solicitud", resp.context)
        self.assertIn("ultimo", resp.context)
        self.assertEqual(resp.context["solicitud"].id, self.solicitud.id)
        self.assertEqual(resp.context["ultimo"].id, seg.id)

    def test_atender_solicitud_metodo_no_get_devuelve_405(self):
        url = reverse("atender_solicitud", args=[self.solicitud.id])
        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 405)
        # Se devuelve JSON: {"error": "..."}
        data = json.loads(resp.content.decode())
        self.assertEqual(data["error"], "Metodo no permitido.")

    # ---------- marcar_solicitud_en_proceso ----------

    def test_marcar_en_proceso_cuando_esta_creada_crea_seguimiento_en_proceso(self):
        SeguimientoSolicitud.objects.create(
            solicitud=self.solicitud,
            estatus="1",  # Creada
            observaciones="Creada",
        )
        url = reverse("marcar_solicitud_en_proceso", args=[self.solicitud.id])
        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            resp.url, reverse("atender_solicitud", args=[self.solicitud.id])
        )

        ultimo = self.solicitud.seguimientos.order_by("-fecha_creacion").first()
        self.assertEqual(ultimo.estatus, "2")

    def test_marcar_en_proceso_falla_si_ultimo_no_es_creada(self):
        SeguimientoSolicitud.objects.create(
            solicitud=self.solicitud,
            estatus="2",  # Ya está en proceso
            observaciones="En proceso",
        )
        url = reverse("marcar_solicitud_en_proceso", args=[self.solicitud.id])
        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.content.decode())
        # Mensaje genérico de error
        self.assertIn("No se puede cambiar el estatus", data["error"])
        self.assertEqual(self.solicitud.seguimientos.count(), 1)

    def test_marcar_en_proceso_metodo_no_post(self):
        url = reverse("marcar_solicitud_en_proceso", args=[self.solicitud.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 405)
        data = json.loads(resp.content.decode())
        self.assertEqual(data["error"], "Metodo no permitido.")

    # ---------- cerrar_solicitud ----------

    def test_cerrar_solicitud_falla_si_no_esta_en_proceso(self):
        # Último seguimiento NO está en proceso (estatus 1 = Creada)
        SeguimientoSolicitud.objects.create(
            solicitud=self.solicitud,
            estatus="1",
            observaciones="Creada",
        )
        url = reverse("cerrar_solicitud", args=[self.solicitud.id])
        resp = self.client.post(
            url,
            data={"estatus": "3", "observaciones": "Termino"},
        )

        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.content.decode())
        # Aquí Django ya decodifica los acentos del JSON (\u00e1 -> á)
        self.assertEqual(
            data["error"],
            "Solo se puede cerrar si está En proceso.",
        )
        self.assertEqual(self.solicitud.seguimientos.count(), 1)

    def test_cerrar_solicitud_con_form_valido_crea_seguimiento_terminada(self):
        SeguimientoSolicitud.objects.create(
            solicitud=self.solicitud,
            estatus="2",  # En proceso
            observaciones="En proceso",
        )
        url = reverse("cerrar_solicitud", args=[self.solicitud.id])
        data = {"estatus": "3", "observaciones": "Atendida correctamente"}
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            resp.url, reverse("atender_solicitud", args=[self.solicitud.id])
        )

        ultimo = self.solicitud.seguimientos.order_by("-fecha_creacion").first()
        self.assertEqual(ultimo.estatus, "3")
        self.assertEqual(ultimo.observaciones, "Atendida correctamente")

    def test_cerrar_solicitud_con_form_invalido_regresa_400(self):
        SeguimientoSolicitud.objects.create(
            solicitud=self.solicitud,
            estatus="2",  # En proceso
            observaciones="En proceso",
        )
        url = reverse("cerrar_solicitud", args=[self.solicitud.id])
        data = {
            "estatus": "5",  # valor inválido
            "observaciones": "X",
        }
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, 400)

        # El JSON viene doble:
        # {"error": "{\"estatus\": [{\"message\": \"Estatus inválido...\", ...}]}"}
        outer = json.loads(resp.content.decode())
        self.assertIn("error", outer)

        inner = json.loads(outer["error"])
        self.assertIn("estatus", inner)
        mensaje = inner["estatus"][0]["message"]
        self.assertIn("Estatus inválido", mensaje)

    def test_cerrar_solicitud_metodo_no_post(self):
        SeguimientoSolicitud.objects.create(
            solicitud=self.solicitud,
            estatus="2",
            observaciones="En proceso",
        )
        url = reverse("cerrar_solicitud", args=[self.solicitud.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 405)
        data = json.loads(resp.content.decode())
        self.assertEqual(data["error"], "Método no permitido.")

    # ---------- listar_solicitudes ----------

    def test_listar_solicitudes_status_200_y_template_correcto(self):
        # Crear varias solicitudes con distintos seguimientos
        for est in ["1", "2", "3"]:
            sol = Solicitud.objects.create(
                usuario=self.usuario,
                tipo_solicitud=self.tipo,
                folio=f"SOL-{est}",
            )
            SeguimientoSolicitud.objects.create(
                solicitud=sol, estatus=est, observaciones="Test"
            )

        url = reverse("listar_solicitudes")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "solicitudes_table.html")
        self.assertIn("page_obj", resp.context)
        self.assertIn("conteos", resp.context)
        self.assertGreaterEqual(resp.context["conteos"]["todos"], 1)

    def test_listar_solicitudes_filtra_por_estatus_y_search(self):
        # Solicitud en estatus 1 con folio BUSCAR-ME
        sol1 = Solicitud.objects.create(
            usuario=self.usuario,
            tipo_solicitud=self.tipo,
            folio="BUSCAR-ME",
        )
        SeguimientoSolicitud.objects.create(
            solicitud=sol1, estatus="1", observaciones="Creada"
        )

        # Otra en estatus 3 que no debe salir al filtrar por estatus=1
        sol2 = Solicitud.objects.create(
            usuario=self.usuario,
            tipo_solicitud=self.tipo,
            folio="OTRA-SOL",
        )
        SeguimientoSolicitud.objects.create(
            solicitud=sol2, estatus="3", observaciones="Terminada"
        )

        url = reverse("listar_solicitudes")
        resp = self.client.get(url, {"estatus": "1", "search": "BUSCAR"})

        self.assertEqual(resp.status_code, 200)
        contenido = resp.content.decode()
        self.assertIn("BUSCAR-ME", contenido)
        self.assertNotIn("OTRA-SOL", contenido)
