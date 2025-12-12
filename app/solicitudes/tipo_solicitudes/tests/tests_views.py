from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from tipo_solicitudes.models import (
    TipoSolicitud, Solicitud, SeguimientoSolicitud
)

Usuario = get_user_model()


class TestSmokeTest(TestCase):

    # def test_hola_mundo(self):
    #     self.assertEqual('hola mundo', 'hola mundo')

    # url --> urlConf, view, template
    def test_estatus_200_lista_tipo_solicitud(self):
        response = self.client.get('/tipo-solicitud/lista')
        # print(response.content)
        self.assertEqual(200, response.status_code)

    def test_template_correcto_tipo_solicitud(self):
        response = self.client.get('/tipo-solicitud/lista')
        self.assertTemplateUsed(response, 'lista_tipo_solicitudes.html')

    # def test_template_correcto_tipo_solicitud(self):
    #     response = self.client.get('/tipo-solicitud/lista')
    #     titulo = '<title> Sistema de Solicitudes IS </title>'
    #     print(response.content)
    #     # print(response.)
    #     self.assertInHTML(titulo, str(response.content))

    def test_agrega_tipo_solicitud(self):
        data = {
            'nombre': 'Constancia',
            'descripcion': 'Constancia para servicio social'
        }
        self.client.post('/tipo-solicitud/', data=data)
        self.assertEqual(1, TipoSolicitud.objects.count())

    def test_resultado_4_en_el_contexto(self):
        response = self.client.get('/tipo-solicitud/lista')
        self.assertEqual(4, response.context['resultado'])

    def test_obtener_solicitudes(self):
        pass


class TestMetricasView(TestCase):
    """Pruebas unitarias para la vista de métricas"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.user = Usuario.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            rol='administrador',
            perfil_completo=True
        )
        self.client.force_login(self.user)

        # Crear tipos de solicitud con diferentes responsables
        self.tipo1 = TipoSolicitud.objects.create(
            nombre='Tipo A',
            descripcion='Descripción A',
            responsable='1'
        )
        self.tipo2 = TipoSolicitud.objects.create(
            nombre='Tipo B',
            descripcion='Descripción B',
            responsable='2'
        )

    def test_metricas_url_responde_200(self):
        """Verifica que la URL de métricas responde correctamente"""
        response = self.client.get('/tipo-solicitud/metricas/')
        self.assertEqual(response.status_code, 200)

    def test_metricas_usa_template_correcto(self):
        """Verifica que se usa el template correcto"""
        response = self.client.get('/tipo-solicitud/metricas/')
        self.assertTemplateUsed(
            response, 'tipo_solicitudes/metricas.html'
        )

    def test_metricas_requiere_autenticacion(self):
        """Verifica que la vista requiere autenticación"""
        self.client.logout()
        response = self.client.get('/tipo-solicitud/metricas/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_total_tickets_sin_solicitudes(self):
        """Verifica conteo de tickets cuando no hay solicitudes"""
        response = self.client.get('/tipo-solicitud/metricas/')
        self.assertEqual(response.context['total_tickets'], 0)

    def test_total_tickets_con_solicitudes(self):
        """Verifica conteo correcto de tickets"""
        for i in range(5):
            solicitud = Solicitud.objects.create(
                usuario=self.user,
                tipo_solicitud=self.tipo1,
                folio=f'FOLIO-{i}'
            )
            SeguimientoSolicitud.objects.create(
                solicitud=solicitud,
                estatus='1',
                observaciones='Test'
            )

        response = self.client.get('/tipo-solicitud/metricas/')
        self.assertEqual(response.context['total_tickets'], 5)

    def test_solicitudes_por_tipo(self):
        """Verifica conteo de solicitudes por tipo"""
        # 3 solicitudes tipo A
        for i in range(3):
            solicitud = Solicitud.objects.create(
                usuario=self.user,
                tipo_solicitud=self.tipo1,
                folio=f'A-{i}'
            )
            SeguimientoSolicitud.objects.create(
                solicitud=solicitud,
                estatus='1',
                observaciones='Test'
            )

        # 2 solicitudes tipo B
        for i in range(2):
            solicitud = Solicitud.objects.create(
                usuario=self.user,
                tipo_solicitud=self.tipo2,
                folio=f'B-{i}'
            )
            SeguimientoSolicitud.objects.create(
                solicitud=solicitud,
                estatus='1',
                observaciones='Test'
            )

        response = self.client.get('/tipo-solicitud/metricas/')
        solicitudes_tipo = response.context['solicitudes_por_tipo']

        tipos_dict = {item['tipo_solicitud__nombre']: item['count']
                      for item in solicitudes_tipo}
        self.assertEqual(tipos_dict['Tipo A'], 3)
        self.assertEqual(tipos_dict['Tipo B'], 2)

    def test_solicitudes_por_estatus(self):
        """Verifica conteo de solicitudes por estatus"""
        # 2 Creadas
        for i in range(2):
            solicitud = Solicitud.objects.create(
                usuario=self.user,
                tipo_solicitud=self.tipo1,
                folio=f'CREADA-{i}'
            )
            SeguimientoSolicitud.objects.create(
                solicitud=solicitud,
                estatus='1',
                observaciones='Creada'
            )

        # 3 En proceso
        for i in range(3):
            solicitud = Solicitud.objects.create(
                usuario=self.user,
                tipo_solicitud=self.tipo1,
                folio=f'PROCESO-{i}'
            )
            SeguimientoSolicitud.objects.create(
                solicitud=solicitud,
                estatus='2',
                observaciones='En proceso'
            )

        # 1 Terminada
        solicitud = Solicitud.objects.create(
            usuario=self.user,
            tipo_solicitud=self.tipo1,
            folio='TERMINADA-1'
        )
        SeguimientoSolicitud.objects.create(
            solicitud=solicitud,
            estatus='3',
            observaciones='Terminada'
        )

        response = self.client.get('/tipo-solicitud/metricas/')
        status_series = response.context['status_series']

        status_dict = {item['code']: item['count']
                       for item in status_series}
        self.assertEqual(status_dict['1'], 2)
        self.assertEqual(status_dict['2'], 3)
        self.assertEqual(status_dict['3'], 1)
        self.assertEqual(status_dict['4'], 0)

    def test_promedio_resolucion_sin_terminadas(self):
        """Verifica promedio cuando no hay solicitudes terminadas"""
        solicitud = Solicitud.objects.create(
            usuario=self.user,
            tipo_solicitud=self.tipo1,
            folio='TEST-1'
        )
        SeguimientoSolicitud.objects.create(
            solicitud=solicitud,
            estatus='1',
            observaciones='Creada'
        )

        response = self.client.get('/tipo-solicitud/metricas/')
        self.assertIsNone(response.context['promedio_resolucion'])

    def test_promedio_resolucion_con_terminadas(self):
        """Verifica cálculo de promedio de resolución"""
        now = timezone.now()

        # Solicitud 1: 1 hora de resolución
        sol1 = Solicitud.objects.create(
            usuario=self.user,
            tipo_solicitud=self.tipo1,
            folio='RES-1'
        )
        SeguimientoSolicitud.objects.create(
            solicitud=sol1,
            estatus='1',
            observaciones='Inicio',
            fecha_creacion=now - timedelta(hours=1)
        )
        seg_term = SeguimientoSolicitud.objects.create(
            solicitud=sol1,
            estatus='3',
            observaciones='Terminada',
            fecha_creacion=now
        )
        seg_term.fecha_terminacion = now
        seg_term.save()

        response = self.client.get('/tipo-solicitud/metricas/')
        promedio = response.context['promedio_resolucion']
        self.assertIsNotNone(promedio)
        # Puede ser 's', 'min', 'h' o 'd' dependiendo del tiempo
        self.assertTrue(any(u in promedio for u in ['s', 'min', 'h', 'd']))

    def test_solicitudes_por_responsable(self):
        """Verifica conteo de solicitudes por responsable"""
        # 2 solicitudes con responsable '1'
        for i in range(2):
            solicitud = Solicitud.objects.create(
                usuario=self.user,
                tipo_solicitud=self.tipo1,
                folio=f'R1-{i}'
            )
            SeguimientoSolicitud.objects.create(
                solicitud=solicitud,
                estatus='1',
                observaciones='Test'
            )

        # 3 solicitudes con responsable '2'
        for i in range(3):
            solicitud = Solicitud.objects.create(
                usuario=self.user,
                tipo_solicitud=self.tipo2,
                folio=f'R2-{i}'
            )
            SeguimientoSolicitud.objects.create(
                solicitud=solicitud,
                estatus='1',
                observaciones='Test'
            )

        response = self.client.get('/tipo-solicitud/metricas/')
        responsables = response.context['solicitudes_por_responsable']

        resp_dict = {item['responsable']: item['count']
                     for item in responsables}
        self.assertEqual(resp_dict['Control escolar'], 2)
        self.assertEqual(resp_dict['Responsable de programa'], 3)

    def test_metricas_contexto_completo(self):
        """Verifica que el contexto contiene todas las claves esperadas"""
        response = self.client.get('/tipo-solicitud/metricas/')

        self.assertIn('total_tickets', response.context)
        self.assertIn('solicitudes_por_tipo', response.context)
        self.assertIn('solicitudes_por_responsable', response.context)
        self.assertIn('promedio_resolucion', response.context)
        self.assertIn('status_series', response.context)
        self.assertIn('labels_json', response.context)
        self.assertIn('data_json', response.context)

    def test_promedio_formato_segundos(self):
        """Verifica formato cuando el promedio es menor a 1 minuto"""
        now = timezone.now()
        sol = Solicitud.objects.create(
            usuario=self.user,
            tipo_solicitud=self.tipo1,
            folio='SEC-1'
        )
        SeguimientoSolicitud.objects.create(
            solicitud=sol,
            estatus='1',
            observaciones='Inicio',
            fecha_creacion=now - timedelta(seconds=30)
        )
        seg_term = SeguimientoSolicitud.objects.create(
            solicitud=sol,
            estatus='3',
            observaciones='Terminada',
            fecha_creacion=now
        )
        seg_term.fecha_terminacion = now
        seg_term.save()

        response = self.client.get('/tipo-solicitud/metricas/')
        promedio = response.context['promedio_resolucion']
        self.assertIn('s', promedio)
        self.assertNotIn('min', promedio)

    def test_promedio_formato_minutos(self):
        """Verifica formato cuando el promedio está en minutos"""
        now = timezone.now()
        inicio = now - timedelta(minutes=30)
        sol = Solicitud.objects.create(
            usuario=self.user,
            tipo_solicitud=self.tipo1,
            folio='MIN-1'
        )
        seg_inicial = SeguimientoSolicitud.objects.create(
            solicitud=sol,
            estatus='1',
            observaciones='Inicio'
        )
        seg_inicial.fecha_creacion = inicio
        seg_inicial.save()

        seg_term = SeguimientoSolicitud.objects.create(
            solicitud=sol,
            estatus='3',
            observaciones='Terminada'
        )
        seg_term.fecha_creacion = now
        seg_term.fecha_terminacion = now
        seg_term.save()

        response = self.client.get('/tipo-solicitud/metricas/')
        promedio = response.context['promedio_resolucion']
        self.assertIn('min', promedio)

    def test_promedio_formato_horas(self):
        """Verifica formato cuando el promedio está en horas"""
        now = timezone.now()
        inicio = now - timedelta(hours=5)
        sol = Solicitud.objects.create(
            usuario=self.user,
            tipo_solicitud=self.tipo1,
            folio='HOUR-1'
        )
        seg_inicial = SeguimientoSolicitud.objects.create(
            solicitud=sol,
            estatus='1',
            observaciones='Inicio'
        )
        seg_inicial.fecha_creacion = inicio
        seg_inicial.save()

        seg_term = SeguimientoSolicitud.objects.create(
            solicitud=sol,
            estatus='3',
            observaciones='Terminada'
        )
        seg_term.fecha_creacion = now
        seg_term.fecha_terminacion = now
        seg_term.save()

        response = self.client.get('/tipo-solicitud/metricas/')
        promedio = response.context['promedio_resolucion']
        self.assertIn('h', promedio)

    def test_promedio_formato_dias(self):
        """Verifica formato cuando el promedio está en días"""
        now = timezone.now()
        inicio = now - timedelta(days=2)
        sol = Solicitud.objects.create(
            usuario=self.user,
            tipo_solicitud=self.tipo1,
            folio='DAY-1'
        )
        seg_inicial = SeguimientoSolicitud.objects.create(
            solicitud=sol,
            estatus='1',
            observaciones='Inicio'
        )
        seg_inicial.fecha_creacion = inicio
        seg_inicial.save()

        seg_term = SeguimientoSolicitud.objects.create(
            solicitud=sol,
            estatus='3',
            observaciones='Terminada'
        )
        seg_term.fecha_creacion = now
        seg_term.fecha_terminacion = now
        seg_term.save()

        response = self.client.get('/tipo-solicitud/metricas/')
        promedio = response.context['promedio_resolucion']
        self.assertIn('d', promedio)

    def test_promedio_con_multiples_terminadas(self):
        """Verifica cálculo correcto con múltiples solicitudes terminadas"""
        now = timezone.now()

        # Solicitud 1: 2 horas
        sol1 = Solicitud.objects.create(
            usuario=self.user,
            tipo_solicitud=self.tipo1,
            folio='MULTI-1'
        )
        seg1_inicio = SeguimientoSolicitud.objects.create(
            solicitud=sol1,
            estatus='1',
            observaciones='Inicio'
        )
        seg1_inicio.fecha_creacion = now - timedelta(hours=2)
        seg1_inicio.save()

        seg1 = SeguimientoSolicitud.objects.create(
            solicitud=sol1,
            estatus='3',
            observaciones='Terminada'
        )
        seg1.fecha_creacion = now
        seg1.fecha_terminacion = now
        seg1.save()

        # Solicitud 2: 4 horas
        sol2 = Solicitud.objects.create(
            usuario=self.user,
            tipo_solicitud=self.tipo1,
            folio='MULTI-2'
        )
        seg2_inicio = SeguimientoSolicitud.objects.create(
            solicitud=sol2,
            estatus='1',
            observaciones='Inicio'
        )
        seg2_inicio.fecha_creacion = now - timedelta(hours=4)
        seg2_inicio.save()

        seg2 = SeguimientoSolicitud.objects.create(
            solicitud=sol2,
            estatus='3',
            observaciones='Terminada'
        )
        seg2.fecha_creacion = now
        seg2.fecha_terminacion = now
        seg2.save()

        response = self.client.get('/tipo-solicitud/metricas/')
        promedio = response.context['promedio_resolucion']
        # Promedio debería ser 3h
        self.assertIsNotNone(promedio)
        self.assertIn('h', promedio)

    def test_solicitud_con_seguimientos_multiples(self):
        """Verifica que usa el primer y último seguimiento correctamente"""
        now = timezone.now()

        sol = Solicitud.objects.create(
            usuario=self.user,
            tipo_solicitud=self.tipo1,
            folio='MULTI-SEG'
        )
        # Primer seguimiento: Creada
        seg1 = SeguimientoSolicitud.objects.create(
            solicitud=sol,
            estatus='1',
            observaciones='Creada'
        )
        seg1.fecha_creacion = now - timedelta(hours=5)
        seg1.save()

        # Segundo seguimiento: En proceso
        seg2 = SeguimientoSolicitud.objects.create(
            solicitud=sol,
            estatus='2',
            observaciones='En proceso'
        )
        seg2.fecha_creacion = now - timedelta(hours=3)
        seg2.save()

        # Tercer seguimiento: Terminada
        seg_term = SeguimientoSolicitud.objects.create(
            solicitud=sol,
            estatus='3',
            observaciones='Terminada'
        )
        seg_term.fecha_creacion = now
        seg_term.fecha_terminacion = now
        seg_term.save()

        response = self.client.get('/tipo-solicitud/metricas/')
        promedio = response.context['promedio_resolucion']
        # Debería calcular desde el primer seguimiento (5h)
        self.assertIsNotNone(promedio)
        self.assertIn('h', promedio)

    def test_labels_json_formato_correcto(self):
        """Verifica que labels_json está en formato JSON válido"""
        import json

        solicitud = Solicitud.objects.create(
            usuario=self.user,
            tipo_solicitud=self.tipo1,
            folio='JSON-1'
        )
        SeguimientoSolicitud.objects.create(
            solicitud=solicitud,
            estatus='1',
            observaciones='Test'
        )

        response = self.client.get('/tipo-solicitud/metricas/')
        labels_json = response.context['labels_json']

        # Debe ser JSON válido
        labels = json.loads(labels_json)
        self.assertIsInstance(labels, list)
        self.assertIn('Tipo A', labels)

    def test_data_json_formato_correcto(self):
        """Verifica que data_json está en formato JSON válido"""
        import json

        for i in range(3):
            solicitud = Solicitud.objects.create(
                usuario=self.user,
                tipo_solicitud=self.tipo1,
                folio=f'DATA-{i}'
            )
            SeguimientoSolicitud.objects.create(
                solicitud=solicitud,
                estatus='1',
                observaciones='Test'
            )

        response = self.client.get('/tipo-solicitud/metricas/')
        data_json = response.context['data_json']

        # Debe ser JSON válido
        data = json.loads(data_json)
        self.assertIsInstance(data, list)
        self.assertEqual(data[0], 3)

    def test_status_series_incluye_todos_estatus(self):
        """Verifica que status_series incluye los 4 estatus posibles"""
        response = self.client.get('/tipo-solicitud/metricas/')
        status_series = response.context['status_series']

        codes = [item['code'] for item in status_series]
        self.assertIn('1', codes)
        self.assertIn('2', codes)
        self.assertIn('3', codes)
        self.assertIn('4', codes)
        self.assertEqual(len(status_series), 4)

    def test_status_series_labels_correctos(self):
        """Verifica que los labels de estatus son correctos"""
        response = self.client.get('/tipo-solicitud/metricas/')
        status_series = response.context['status_series']

        labels = {item['code']: item['label'] for item in status_series}
        self.assertEqual(labels['1'], 'Creada')
        self.assertEqual(labels['2'], 'En proceso')
        self.assertEqual(labels['3'], 'Terminada')
        self.assertEqual(labels['4'], 'Cancelada')

    def test_solicitudes_canceladas_no_afectan_promedio(self):
        """Verifica que solicitudes canceladas no se incluyen en promedio"""
        now = timezone.now()

        # Solicitud cancelada
        sol_cancel = Solicitud.objects.create(
            usuario=self.user,
            tipo_solicitud=self.tipo1,
            folio='CANCEL-1'
        )
        SeguimientoSolicitud.objects.create(
            solicitud=sol_cancel,
            estatus='4',
            observaciones='Cancelada',
            fecha_creacion=now
        )

        response = self.client.get('/tipo-solicitud/metricas/')
        promedio = response.context['promedio_resolucion']
        # No debe haber promedio porque solo hay canceladas
        self.assertIsNone(promedio)

    def test_multiples_tipos_ordenados_por_cantidad(self):
        """Verifica que tipos se ordenan por cantidad descendente"""
        tipo3 = TipoSolicitud.objects.create(
            nombre='Tipo C',
            descripcion='Descripción C',
            responsable='3'
        )

        # 5 del tipo3, 2 del tipo2, 3 del tipo1
        for i in range(5):
            sol = Solicitud.objects.create(
                usuario=self.user,
                tipo_solicitud=tipo3,
                folio=f'TC-{i}'
            )
            SeguimientoSolicitud.objects.create(
                solicitud=sol,
                estatus='1',
                observaciones='Test'
            )

        for i in range(2):
            sol = Solicitud.objects.create(
                usuario=self.user,
                tipo_solicitud=self.tipo2,
                folio=f'TB-{i}'
            )
            SeguimientoSolicitud.objects.create(
                solicitud=sol,
                estatus='1',
                observaciones='Test'
            )

        for i in range(3):
            sol = Solicitud.objects.create(
                usuario=self.user,
                tipo_solicitud=self.tipo1,
                folio=f'TA-{i}'
            )
            SeguimientoSolicitud.objects.create(
                solicitud=sol,
                estatus='1',
                observaciones='Test'
            )

        response = self.client.get('/tipo-solicitud/metricas/')
        solicitudes_tipo = response.context['solicitudes_por_tipo']

        # Debe estar ordenado por cantidad descendente
        cantidades = [item['count'] for item in solicitudes_tipo]
        self.assertEqual(cantidades, sorted(cantidades, reverse=True))
