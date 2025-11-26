from datetime import datetime, timedelta
import os
import csv
import io
import json
from django.http import HttpResponse
from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI
import matplotlib.pyplot as plt
from .forms import FormArchivoAdjunto, FormCampoFormulario, FormFormularioSolicitud, FormSolicitud, FormTipoSolicitud
from .models import ESTATUS, RESPOSABLES, SeguimientoSolicitud, Solicitud, TipoSolicitud, ArchivoAdjunto, CampoFormulario, FormularioSolicitud, RespuestaCampo
from .funcionalidad import FuncionesAvanzadas
from django.db.models import Max

@login_required
def bienvenida(request):
    return render(request, 'bienvenida.html')

@login_required
def lista_solicitudes(request):
    funciones_avanzadas = FuncionesAvanzadas()
    resultado = funciones_avanzadas.calculo_extremo(2, 2)

    context = {
        'tipo_solicitudes': TipoSolicitud.objects.all(),
        'resultado': resultado
    }
    return render(request, 'lista_tipo_solicitudes.html', context)


@login_required
def agregar(request):
    if request.method == 'POST':
        form = FormTipoSolicitud(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tipo_solicitudes')   
    else:
        form = FormTipoSolicitud()

    return render(request, 'agregar_solicitud.html', {'form': form})

@login_required
def obtener_solicitudes(request):
    solicitudes = Solicitud.objects.all()
    tipos_solicitudes = TipoSolicitud.objects.all()
    contexto_solicitudes = {
        'solicitudes': solicitudes
    }
    return contexto_solicitudes

def filtrar_solicitudes_fecha(solicitudes, dia, mes, semana):
    if dia!= 0:
        solicitudes = solicitudes.filter(fecha_creacion__day=dia)
    elif mes!=0:
        solicitudes = solicitudes.filter(fecha_creacion__month=mes)
    elif semana!=0:
        year = datetime.now().year
        inicio = datetime.fromisocalendar(year, semana, 1)
        fin = datetime.fromisocalendar(year, semana, 7)
        solicitudes = solicitudes.filter(fecha_creacion__range=[inicio, fin])
    return solicitudes

def solicitudes_por_tipo(solicitudes_filtradas):
    solicitudes = (
        solicitudes_filtradas
        .values('tipo_solicitud__nombre')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    data = [
        {
            "tipo": s["tipo_solicitud__nombre"],
            "total": s["total"]
        }
        for s in solicitudes
    ]
    return data

@login_required
def vista_tres_graficas(request):
    hoy = datetime.now().date()
    año, semana, _ = hoy.isocalendar()
    solicitudes = Solicitud.objects.all()
    solicitudes_hoy = solicitudes.filter(fecha_creacion__date=hoy)
    data_hoy = solicitudes_por_tipo(solicitudes_hoy)
    inicio_semana = datetime.fromisocalendar(hoy.year, semana, 1)
    fin_semana = datetime.fromisocalendar(hoy.year, semana, 7)
    solicitudes_semana = solicitudes.filter(fecha_creacion__range=[inicio_semana, fin_semana])
    data_semana = solicitudes_por_tipo(solicitudes_semana)
    solicitudes_mes = solicitudes.filter(fecha_creacion__year=hoy.year, fecha_creacion__month=hoy.month)
    data_mes = solicitudes_por_tipo(solicitudes_mes)
    context = {
        "hoy": data_hoy,
        "semana": data_semana,
        "mes": data_mes,
    }
    return render(request, "grafica.html", context)

@login_required
def generar_pdf_graficas(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="graficas_solicitudes.pdf"'
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    elements = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#1458b1'), spaceAfter=30, alignment=TA_CENTER)
    title = Paragraph("Tendencias de Solicitudes", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    hoy = datetime.now().date()
    año, semana, _ = hoy.isocalendar()
    solicitudes = Solicitud.objects.all()
    solicitudes_hoy = solicitudes.filter(fecha_creacion__date=hoy)
    data_hoy = solicitudes_por_tipo(solicitudes_hoy)
    inicio_semana = datetime.fromisocalendar(hoy.year, semana, 1)
    fin_semana = datetime.fromisocalendar(hoy.year, semana, 7)
    solicitudes_semana = solicitudes.filter(fecha_creacion__range=[inicio_semana, fin_semana])
    data_semana = solicitudes_por_tipo(solicitudes_semana)
    solicitudes_mes = solicitudes.filter(fecha_creacion__year=hoy.year, fecha_creacion__month=hoy.month)
    data_mes = solicitudes_por_tipo(solicitudes_mes)
    def crear_grafico(data, titulo):
        if not data:
            return None
        fig, ax = plt.subplots(figsize=(8, 5))
        tipos = [item['tipo'] for item in data]
        totales = [item['total'] for item in data]
        colores_barras = ['#c9a24d', '#202146', '#d7d7d7', '#c9a24d', '#202146']
        bars = ax.bar(tipos, totales, color=colores_barras[:len(tipos)], width=0.6)
        max_valor = max(totales) if totales else 1
        ax.set_ylim(0, max_valor * 1.5)
        ax.set_xlabel('Tipo de Solicitud', fontweight='bold', fontsize=11)
        ax.set_ylabel('Número de Solicitudes', fontweight='bold', fontsize=11)
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        tipos_formateados = []
        for tipo in tipos:
            if len(tipo) > 15:
                palabras = tipo.split()
                lineas = []
                linea_actual = []
                for palabra in palabras:
                    linea_actual.append(palabra)
                    if len(' '.join(linea_actual)) > 15:
                        lineas.append(' '.join(linea_actual[:-1]))
                        linea_actual = [palabra]
                if linea_actual:
                    lineas.append(' '.join(linea_actual))
                tipos_formateados.append('\n'.join(lineas))
            else:
                tipos_formateados.append(tipo)
        ax.set_xticks(range(len(tipos)))
        ax.set_xticklabels(tipos_formateados, fontsize=9, ha='center')
        plt.yticks(fontsize=10)
        for i, v in enumerate(totales):
            ax.text(i, v + (max_valor * 0.02), str(v), ha='center', va='bottom', fontweight='bold', fontsize=11)
        ax.yaxis.grid(True, linestyle='--', alpha=0.3)
        ax.set_axisbelow(True)
        plt.tight_layout()
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
        img_buffer.seek(0)
        plt.close()
        return img_buffer
    def agregar_seccion(data, titulo_seccion):
        subtitle = Paragraph(titulo_seccion, styles['Heading2'])
        elements.append(subtitle)
        elements.append(Spacer(1, 0.1*inch))
        if data:
            img_buffer = crear_grafico(data, titulo_seccion)
            if img_buffer:
                img = Image(img_buffer, width=6*inch, height=3.5*inch)
                elements.append(img)
                elements.append(Spacer(1, 0.3*inch))
        else:
            elements.append(Paragraph("No hay datos para este período", styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))
    agregar_seccion(data_hoy, "Solicitudes de Hoy")
    agregar_seccion(data_semana, "Solicitudes de Esta Semana")
    agregar_seccion(data_mes, "Solicitudes de Este Mes")
    fecha_generacion = Paragraph(f"Reporte generado el {hoy.strftime('%d/%m/%Y')}", styles['Normal'])
    elements.append(Spacer(1, 0.3*inch))
    elements.append(fecha_generacion)
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

@login_required
def generar_csv_graficas(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="solicitudes.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Usuario', 'Tipo de Solicitud', 'Folio', 'Fecha de Creacion'])
    solicitudes = Solicitud.objects.all()
    for s in solicitudes:
        writer.writerow([s.id, s.usuario.username, s.tipo_solicitud.nombre, s.folio, s.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")])
    return response

@login_required
def metricas(request):
    total_tickets = Solicitud.objects.count()

    solicitudes_por_tipo = (
        Solicitud.objects
        .values('tipo_solicitud__nombre')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    solicitudes_por_responsable = (
        Solicitud.objects
        .values('tipo_solicitud__responsable')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    responsable_map = dict(RESPOSABLES)
    responsable_series = [
        {
            'responsable': responsable_map.get(item['tipo_solicitud__responsable'], item['tipo_solicitud__responsable']),
            'count': item['count']
        }
        for item in solicitudes_por_responsable
    ]

    tipo_list = list(solicitudes_por_tipo)
    labels = [t['tipo_solicitud__nombre'] for t in tipo_list]
    data_vals = [t['count'] for t in tipo_list]

    # Obtener el último estatus de cada solicitud desde SeguimientoSolicitud
    from django.db.models import OuterRef, Subquery
    
    # Subconsulta para obtener el último seguimiento de cada solicitud
    ultimo_seguimiento = SeguimientoSolicitud.objects.filter(
        solicitud=OuterRef('pk')
    ).order_by('-fecha_creacion')
    
    status_counts_query = (
        Solicitud.objects
        .annotate(ultimo_estatus=Subquery(ultimo_seguimiento.values('estatus')[:1]))
        .values('ultimo_estatus')
        .annotate(count=Count('id'))
        .order_by('ultimo_estatus')
    )

    status_counts = {item['ultimo_estatus']: item['count'] for item in status_counts_query if item['ultimo_estatus']}

    status_map = dict(ESTATUS)
    status_series = [{
        'code': code,
        'label': status_map.get(code, code),
        'count': status_counts.get(code, 0)
    } for code, _ in ESTATUS]

    # Cálculo del promedio de resolución basado en SeguimientoSolicitud
    promedio_resolucion = None
    
    # Obtener todas las solicitudes que tienen un seguimiento con estatus '3' (Terminada)
    solicitudes_terminadas = Solicitud.objects.filter(
        seguimientos__estatus='3'
    ).distinct()
    
    if solicitudes_terminadas.exists():
        total_seconds = 0
        count = 0
        
        for solicitud in solicitudes_terminadas:
            # Obtener el primer seguimiento (inicio) y el último con estatus '3' (terminado)
            primer_seguimiento = solicitud.seguimientos.order_by('fecha_creacion').first()
            seguimiento_terminado = solicitud.seguimientos.filter(estatus='3').order_by('-fecha_creacion').first()
            
            if primer_seguimiento and seguimiento_terminado:
                # Usar fecha_terminacion si está disponible, sino usar fecha_creacion
                fecha_fin = seguimiento_terminado.fecha_terminacion if seguimiento_terminado.fecha_terminacion else seguimiento_terminado.fecha_creacion
                # Calcular tiempo desde el primer seguimiento hasta que se terminó
                delta = fecha_fin - primer_seguimiento.fecha_creacion
                total_seconds += delta.total_seconds()
                count += 1
        
        if count > 0:
            avg_seconds = total_seconds / count
            
            # Formatear el tiempo de forma más precisa
            if avg_seconds < 60:
                # Menos de 1 minuto
                promedio_resolucion = f"{int(avg_seconds)}s"
            elif avg_seconds < 3600:
                # Menos de 1 hora
                minutes = int(avg_seconds / 60)
                seconds = int(avg_seconds % 60)
                promedio_resolucion = f"{minutes}min {seconds}s"
            elif avg_seconds < 86400:
                # Menos de 1 día
                hours = int(avg_seconds / 3600)
                minutes = int((avg_seconds % 3600) / 60)
                promedio_resolucion = f"{hours}h {minutes}min"
            else:
                # 1 día o más
                days = int(avg_seconds / 86400)
                hours = int((avg_seconds % 86400) / 3600)
                promedio_resolucion = f"{days}d {hours}h"

    context = {
        'total_tickets': total_tickets,
        'solicitudes_por_tipo': tipo_list,
        'solicitudes_por_responsable': responsable_series,
        'promedio_resolucion': promedio_resolucion,
        'labels_json': json.dumps(labels),
        'data_json': json.dumps(data_vals),
        'status_series': status_series,
    }

    return render(request, "tipo_solicitudes/metricas.html", context)

@login_required
def lista_formularios(request):
    context = {
        'formularios': FormularioSolicitud.objects.all(),
        'resultado': FormularioSolicitud.objects.all().count
    }
    return render(request, 'lista_formulario.html', context)

def generar_folio_unico():
    import uuid
    return f"FOLIO-{uuid.uuid4().hex[:8].upper()}"

@login_required
def crear_o_editar_formulario(request, pk=None):
    instancia = None
    if pk:
        instancia = get_object_or_404(FormularioSolicitud, pk=pk)

    if request.method == 'POST':
        form = FormFormularioSolicitud(request.POST, instance=instancia)
        
        if form.is_valid():
            form.save()
            return redirect('lista_formularios')
    else:
        form = FormFormularioSolicitud(instance=instancia)
        
    if instancia:
        titulo = "Editar Formulario de Solicitud"
    else:
        titulo = "Crear Nuevo Formulario de Solicitud"
        
    context = {
        'form': form,
        'titulo': titulo,
        'instancia': instancia,
    }
    return render(request, 'crear_formulario_solicitud.html', context)

@login_required
def crear_campos(request, formulario_id):
    formulario = get_object_or_404(FormularioSolicitud, pk=formulario_id)

    if request.method == "POST":
        form = FormCampoFormulario(request.POST, formulario=formulario)
        if form.is_valid():
            nuevo_campo = form.save(commit=False)
            nuevo_campo.formulario = formulario

            # Si el usuario no pone orden o pone 0 → poner al final
            if not nuevo_campo.orden or nuevo_campo.orden == 0:
                max_orden = formulario.campos.aggregate(Max('orden'))['orden__max'] or 0
                nuevo_campo.orden = max_orden + 1

            nuevo_campo.save()
            return redirect('crear_campos', formulario_id=formulario.id)

    else:
        form = FormCampoFormulario(formulario=formulario)

    campos_existentes = formulario.campos.all().order_by('orden')

    return render(request, 'preguntas_formulario.html', {
        'form': form,
        'formulario': formulario,
        'campos': campos_existentes,
    })


@login_required
def eliminar_campo(request, campo_id):
    campo = get_object_or_404(CampoFormulario, pk=campo_id)
    formulario_id = campo.formulario.id
    campo.delete()
    return redirect('crear_campos', formulario_id=formulario_id)
