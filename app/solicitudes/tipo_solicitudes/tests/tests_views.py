from django.test import TestCase
from tipo_solicitudes.models import TipoSolicitud


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
        response = self.client.post('/tipo-solicitud/', data=data)
        self.assertEqual(1, TipoSolicitud.objects.count())

    def test_resultado_4_en_el_contexto(self):
        response = self.client.get('/tipo-solicitud/lista')
        self.assertEqual(4, response.context['resultado'])

    ####

    def test_obtener_datos_grafica(self):
        pass

    def test_generar_pdf(self):
        pass

    def test_generar_csv(self):
        pass

    def test_exportacion_pdf(self):
        pass

    def test_exportacion_csv(self):
        pass

    def test_graficas_pendejas3(self):
        print("Hola desde graficas pendejas 3")
        pass
