from django.urls import path
from tipo_solicitudes import views

# 'tipo-solicitud/'
urlpatterns = [
    path('', views.lista_solicitudes, name='lista_tipo_solicitudes'),
    path('agregar/', views.agregar, name='agrega_solicitud'),
    path('grafica_solicitudes/', views.vista_tres_graficas,
         name='grafica_solicitudes'),
    path('generar_pdf_graficas/', views.generar_pdf_graficas,
         name='generar_pdf_graficas'),
    path('generar_csv_graficas/', views.generar_csv_graficas,
         name='generar_csv_graficas'),
    path('metricas/', views.metricas, name='metricas'),
    path('formularios/', views.lista_formularios, name='lista_formularios'),
    path('formularios/crear/', views.crear_o_editar_formulario,
         name='crear_formulario'),
    path('formularios/editar/<int:pk>/',
         views.crear_o_editar_formulario, name='editar_formulario'),
    path('formulario/<int:formulario_id>/campos/',
         views.crear_campos, name='crear_campos'),
    path('formulario/campo/<int:campo_id>/eliminar/',
         views.eliminar_campo, name='eliminar_campo'),

    # NUEVAS RUTAS AGREGADAS
    path('solicitud/crear/', views.crear_solicitud_usuario,
         name='crear_solicitud_usuario'),
    path('solicitud/mis-solicitudes/',
         views.mis_solicitudes, name='mis_solicitudes'),
    path('solicitud/<int:solicitud_id>/detalle/',
         views.detalle_solicitud, name='detalle_solicitud'),
    path('solicitud/<int:solicitud_id>/seguimiento/',
         views.seguimiento_solicitud, name='seguimiento_solicitud'),
]
