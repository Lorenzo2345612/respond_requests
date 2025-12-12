from django.db.models import Max
from .funcionalidad import FuncionesAvanzadas
from .models import ESTATUS
from .models import RESPOSABLES
from .models import SeguimientoSolicitud
from .models import Solicitud
from .models import TipoSolicitud
from .models import CampoFormulario
from .models import FormularioSolicitud
from .forms import FormCampoFormulario, FormFormularioSolicitud, FormTipoSolicitud
import matplotlib.pyplot as plt
from datetime import datetime
import csv
import io
import json
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import Paragraph, Spacer, PageBreak, Image
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI


@login_required
def bienvenida(request):
    return render(request, 'bienvenida.html')


@login_required
def lista_solicitudes(request):
    funciones_avanzadas = FuncionesAvanzadas()

    context = {
        'tipo_solicitudes': TipoSolicitud.objects.all(),
        'resultado': TipoSolicitud.objects.all().count
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
    solicitudes_semana = solicitudes.filter(
        fecha_creacion__range=[inicio_semana, fin_semana])
    data_semana = solicitudes_por_tipo(solicitudes_semana)
    solicitudes_mes = solicitudes.filter(
        fecha_creacion__year=hoy.year, fecha_creacion__month=hoy.month)
    data_mes = solicitudes_por_tipo(solicitudes_mes)
    context = {
        "hoy": data_hoy,
        "semana": data_semana,
        "mes": data_mes,
    }
    return render(request, "grafica.html", context)


@login_required
def generar_pdf_graficas(request):
    """Genera un PDF con gráficas y tabla de solicitudes."""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="graficas_solicitudes.pdf"'
    )
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter, rightMargin=72,
        leftMargin=72, topMargin=72, bottomMargin=18,
        title="Reporte de Graficas"
    )

    elements = _construir_elementos_pdf()
    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def _construir_elementos_pdf():
    """Construye todos los elementos del PDF."""
    elements = []
    styles = getSampleStyleSheet()

    title_style = _crear_estilo_titulo(styles)
    elements.append(Paragraph("Tendencias de Solicitudes", title_style))
    elements.append(Spacer(1, 0.2*inch))

    hoy = datetime.now()
    solicitudes = Solicitud.objects.all().select_related(
        'usuario', 'tipo_solicitud'
    )

    _agregar_graficas(elements, styles, hoy, solicitudes)
    _agregar_tabla_solicitudes(elements, styles, solicitudes, hoy)

    return elements


def _crear_estilo_titulo(styles):
    """Crea el estilo personalizado para títulos."""
    return ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1458b1'),
        spaceAfter=30,
        alignment=TA_CENTER
    )


def _crear_estilo_tabla():
    """Crea el estilo para la tabla de solicitudes."""
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1458b1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])


def _agregar_graficas(elements, styles, hoy, solicitudes):
    """Agrega las tres gráficas al documento."""
    data_hoy = _obtener_data_hoy(hoy, solicitudes)
    data_semana = _obtener_data_semana(hoy, solicitudes)
    data_mes = _obtener_data_mes(hoy, solicitudes)

    _agregar_seccion(elements, styles, data_hoy, "Solicitudes de Hoy")
    _agregar_seccion(
        elements, styles, data_semana, "Solicitudes de Esta Semana"
    )
    _agregar_seccion(elements, styles, data_mes, "Solicitudes de Este Mes")


def _obtener_data_hoy(hoy, solicitudes):
    """Obtiene datos de solicitudes del día actual."""
    solicitudes_hoy = solicitudes.filter(fecha_creacion__date=hoy)
    return solicitudes_por_tipo(solicitudes_hoy)


def _obtener_data_semana(hoy, solicitudes):
    """Obtiene datos de solicitudes de la semana actual."""
    anio, semana, _ = hoy.isocalendar()
    inicio_semana = datetime.fromisocalendar(hoy.year, semana, 1)
    fin_semana = datetime.fromisocalendar(hoy.year, semana, 7)
    solicitudes_semana = solicitudes.filter(
        fecha_creacion__range=[inicio_semana, fin_semana]
    )
    return solicitudes_por_tipo(solicitudes_semana)


def _obtener_data_mes(hoy, solicitudes):
    """Obtiene datos de solicitudes del mes actual."""
    solicitudes_mes = solicitudes.filter(
        fecha_creacion__year=hoy.year,
        fecha_creacion__month=hoy.month
    )
    return solicitudes_por_tipo(solicitudes_mes)


def _agregar_seccion(elements, styles, data, titulo_seccion):
    """Agrega una sección con gráfica al documento."""
    subtitle = Paragraph(titulo_seccion, styles['Heading2'])
    elements.append(subtitle)
    elements.append(Spacer(1, 0.1*inch))

    if data:
        img_buffer = _crear_grafico(data, titulo_seccion)
        if img_buffer:
            img = Image(img_buffer, width=6*inch, height=3.5*inch)
            elements.append(img)
            elements.append(Spacer(1, 0.3*inch))
    else:
        elements.append(
            Paragraph("No hay datos para este período", styles['Normal'])
        )
        elements.append(Spacer(1, 0.3*inch))


def _crear_grafico(data, titulo):
    """Crea un gráfico de barras y lo retorna como buffer de imagen."""
    if not data or data == []:
        return None

    data_top = _preparar_data_top5(data)
    fig, ax = plt.subplots(figsize=(10, 6))

    tipos = [item['tipo'] for item in data_top]
    totales = [item['total'] for item in data_top]

    _configurar_ejes_grafico(ax, tipos, totales, titulo)
    _agregar_valores_sobre_barras(ax, totales)

    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    plt.tight_layout(pad=2.0)

    return _guardar_grafico_en_buffer()


def _preparar_data_top5(data):
    """Prepara los top 5 tipos de solicitudes más el resto como 'Otros'."""
    data_sorted = sorted(data, key=lambda x: x['total'], reverse=True)
    data_top = data_sorted[:5]

    if len(data_sorted) > 5:
        otros_total = sum(item['total'] for item in data_sorted[5:])
        data_top.append({'tipo': 'Otros', 'total': otros_total})

    return data_top


def _configurar_ejes_grafico(ax, tipos, totales, titulo):
    """Configura los ejes y etiquetas del gráfico."""
    max_valor = max(totales) if totales else 1
    ax.set_ylim(0, max_valor * 1.5)

    min_categories = 5
    if len(tipos) < min_categories:
        ax.set_xlim(-0.5, min_categories - 0.5)
    else:
        ax.set_xlim(-0.5, len(tipos) - 0.5)

    colores = [
        '#c9a24d',
        '#202146',
        '#d7d7d7',
        '#c9a24d',
        '#202146',
        '#888888'
    ]
    ax.bar(range(len(tipos)), totales, color=colores[:len(tipos)])
    ax.set_xlabel('Tipo de Solicitud', fontweight='bold', fontsize=11)
    ax.set_ylabel('Número de Solicitudes', fontweight='bold', fontsize=11)
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)

    tipos_formateados = [_formatear_etiqueta(tipo) for tipo in tipos]
    ax.set_xticks(range(len(tipos)))
    ax.set_xticklabels(tipos_formateados, fontsize=9, ha='center')
    plt.yticks(fontsize=10)


def _formatear_etiqueta(tipo):
    """Formatea etiquetas largas para que se muestren en múltiples líneas."""
    if len(tipo) <= 20:
        return tipo

    palabras = tipo.split()
    if len(palabras) > 3:
        return _formatear_etiqueta_palabras(palabras)
    else:
        return _formatear_etiqueta_mitad(tipo)


def _formatear_etiqueta_palabras(palabras):
    """Formatea etiquetas con múltiples palabras."""
    linea1 = []
    linea2 = []
    chars_linea1 = 0

    for i, palabra in enumerate(palabras):
        if chars_linea1 + len(palabra) <= 20:
            linea1.append(palabra)
            chars_linea1 += len(palabra) + 1
        elif i < len(palabras) - 1:
            linea2.append(palabra)

    if linea2 and len(' '.join(linea2)) > 20:
        linea2_texto = ' '.join(linea2)[:17] + '...'
        return ' '.join(linea1) + '\n' + linea2_texto
    else:
        return ' '.join(linea1) + '\n' + ' '.join(linea2)


def _formatear_etiqueta_mitad(tipo):
    """Formatea etiquetas dividiéndolas por la mitad."""
    mitad = len(tipo) // 2
    espacio = tipo.find(' ', mitad)
    if espacio != -1:
        return tipo[:espacio] + '\n' + tipo[espacio+1:]
    else:
        return tipo[:20] + '\n' + tipo[20:40]


def _agregar_valores_sobre_barras(ax, totales):
    """Agrega los valores numéricos sobre cada barra."""
    max_valor = max(totales) if totales else 1
    for i, v in enumerate(totales):
        ax.text(
            i, v + (max_valor * 0.02), str(v),
            ha='center', va='bottom',
            fontweight='bold', fontsize=11
        )


def _guardar_grafico_en_buffer():
    """Guarda el gráfico actual en un buffer y cierra la figura."""
    img_buffer = io.BytesIO()
    plt.savefig(
        img_buffer, format='png', dpi=150,
        bbox_inches='tight', facecolor='white', edgecolor='none'
    )
    img_buffer.seek(0)
    plt.close()
    return img_buffer


def _agregar_tabla_solicitudes(elements, styles, solicitudes, hoy):
    """Agrega la tabla de todas las solicitudes al documento."""
    elements.append(PageBreak())

    table_title = Paragraph(
        "Detalle de Todas las Solicitudes", styles['Heading1']
    )
    elements.append(table_title)
    elements.append(Spacer(1, 0.3*inch))

    table_data = _construir_datos_tabla(solicitudes)
    tabla = _crear_tabla_con_estilo(table_data)

    elements.append(tabla)
    elements.append(Spacer(1, 0.3*inch))

    _agregar_resumen_final(elements, styles, solicitudes, hoy)


def _construir_datos_tabla(solicitudes):
    """Construye los datos para la tabla de solicitudes."""
    table_data = [
        ['ID', 'Usuario', 'Tipo de Solicitud', 'Folio', 'Fecha de Creación']
    ]

    for solicitud in solicitudes:
        table_data.append([
            str(solicitud.id),
            solicitud.usuario.username if solicitud.usuario else 'N/A',
            (solicitud.tipo_solicitud.nombre
             if solicitud.tipo_solicitud else 'N/A'),
            solicitud.folio or 'N/A',
            (solicitud.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
             if solicitud.fecha_creacion else 'N/A')
        ])

    return table_data


def _crear_tabla_con_estilo(table_data):
    """Crea la tabla con el estilo y anchos de columna apropiados."""
    doc_width = 468  # Ancho aproximado del documento con márgenes
    col_widths = [
        doc_width * 0.1,
        doc_width * 0.2,
        doc_width * 0.25,
        doc_width * 0.15,
        doc_width * 0.3
    ]

    tabla = Table(table_data, colWidths=col_widths)
    tabla.setStyle(_crear_estilo_tabla())
    return tabla


def _agregar_resumen_final(elements, styles, solicitudes, hoy):
    """Agrega el resumen final al documento."""
    elements.append(Spacer(1, 0.2*inch))

    total_solicitudes = Paragraph(
        f"Total de solicitudes en el sistema: {solicitudes.count()}",
        styles['Heading3']
    )
    elements.append(total_solicitudes)

    fecha_generacion = Paragraph(
        f"Reporte generado el {hoy.strftime('%d/%m/%Y a las %H:%M:%S')}",
        styles['Normal']
    )
    elements.append(Spacer(1, 0.1*inch))
    elements.append(fecha_generacion)


@login_required
def generar_csv_graficas(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="solicitudes.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Usuario', 'Tipo de Solicitud',
                    'Folio', 'Fecha de Creacion'])
    solicitudes = Solicitud.objects.all()
    for s in solicitudes:
        writer.writerow([s.id, s.usuario.username, s.tipo_solicitud.nombre,
                        s.folio, s.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")])
    return response


def _calcular_promedio_resolucion():
    """Calcula el promedio de tiempo de resolución de solicitudes terminadas"""
    solicitudes_terminadas = Solicitud.objects.filter(
        seguimientos__estatus='3'
    ).distinct()

    if not solicitudes_terminadas.exists():
        return None

    total_seconds = 0
    count = 0

    for solicitud in solicitudes_terminadas:
        primer_seguimiento = solicitud.seguimientos.order_by(
            'fecha_creacion').first()
        seguimiento_terminado = solicitud.seguimientos.filter(
            estatus='3').order_by('-fecha_creacion').first()

        if primer_seguimiento and seguimiento_terminado:
            fecha_fin = (
                seguimiento_terminado.fecha_terminacion
                if seguimiento_terminado.fecha_terminacion
                else seguimiento_terminado.fecha_creacion
            )
            delta = fecha_fin - primer_seguimiento.fecha_creacion
            total_seconds += delta.total_seconds()
            count += 1

    if count == 0:
        return None

    return _formatear_tiempo_promedio(total_seconds / count)


def _formatear_tiempo_promedio(avg_seconds):
    """Formatea segundos a un formato legible"""
    if avg_seconds < 60:
        return f"{int(avg_seconds)}s"
    elif avg_seconds < 3600:
        minutes = int(avg_seconds / 60)
        seconds = int(avg_seconds % 60)
        return f"{minutes}min {seconds}s"
    elif avg_seconds < 86400:
        hours = int(avg_seconds / 3600)
        minutes = int((avg_seconds % 3600) / 60)
        return f"{hours}h {minutes}min"
    else:
        days = int(avg_seconds / 86400)
        hours = int((avg_seconds % 86400) / 3600)
        return f"{days}d {hours}h"


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
            'responsable': responsable_map.get(
                item['tipo_solicitud__responsable'],
                item['tipo_solicitud__responsable']
            ),
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

    status_counts = {item['ultimo_estatus']: item['count']
                     for item in status_counts_query if item['ultimo_estatus']}

    status_map = dict(ESTATUS)
    status_series = [{
        'code': code,
        'label': status_map.get(code, code),
        'count': status_counts.get(code, 0)
    } for code, _ in ESTATUS]

    # Cálculo del promedio de resolución basado en SeguimientoSolicitud
    promedio_resolucion = _calcular_promedio_resolucion()

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
                max_orden = formulario.campos.aggregate(
                    Max('orden'))['orden__max'] or 0
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


# ----------------------
#  VISTAS DE SOLICITUDES
# ----------------------
@login_required
def crear_solicitud_usuario(request):
    """Vista para que un usuario cree una solicitud"""
    tipos_disponibles = TipoSolicitud.objects.all()

    tipo_id = request.GET.get('tipo')
    formulario_solicitud = None
    campos = []

    if tipo_id:
        try:
            tipo = get_object_or_404(TipoSolicitud, id=tipo_id)
            formulario_solicitud = FormularioSolicitud.objects.get(
                tipo_solicitud=tipo)
            campos = formulario_solicitud.campos.all().order_by('orden')
        except FormularioSolicitud.DoesNotExist:
            messages.error(
                request, 'Este tipo de solicitud no tiene formulario configurado.')
            return redirect('crear_solicitud_usuario')

    if request.method == 'POST' and tipo_id:
        tipo = get_object_or_404(TipoSolicitud, id=tipo_id)

        try:
            formulario_solicitud = get_object_or_404(
                FormularioSolicitud, tipo_solicitud=tipo)
        except:
            messages.error(
                request, 'No se encontró el formulario para este tipo de solicitud.')
            return redirect('crear_solicitud_usuario')

        campos = formulario_solicitud.campos.all().order_by('orden')

        errores = []

        # Validar campos requeridos
        for campo in campos:
            if campo.requerido:
                if campo.tipo == 'file':
                    archivos = request.FILES.getlist(f'campo_{campo.id}')
                    if not archivos:
                        errores.append(
                            f'El campo "{campo.etiqueta}" es obligatorio')
                else:
                    valor = request.POST.get(f'campo_{campo.id}', '').strip()
                    if not valor:
                        errores.append(
                            f'El campo "{campo.etiqueta}" es obligatorio')

        if errores:
            for error in errores:
                messages.error(request, error)
        else:
            # Crear la solicitud
            folio = generar_folio_unico()
            solicitud = Solicitud.objects.create(
                usuario=request.user,
                tipo_solicitud=tipo,
                folio=folio
            )

            # Guardar las respuestas
            for campo in campos:
                if campo.tipo == 'file':
                    archivos = request.FILES.getlist(f'campo_{campo.id}')
                    if archivos:
                        respuesta = RespuestaCampo.objects.create(
                            solicitud=solicitud,
                            campo=campo,
                            valor=f'{len(archivos)} archivo(s) adjunto(s)'
                        )

                        # Guardar cada archivo
                        for archivo in archivos[:campo.cantidad_archivos]:
                            ArchivoAdjunto.objects.create(
                                respuesta=respuesta,
                                solicitud=solicitud,
                                archivo=archivo,
                                nombre=archivo.name
                            )
                else:
                    valor = request.POST.get(f'campo_{campo.id}', '')
                    RespuestaCampo.objects.create(
                        solicitud=solicitud,
                        campo=campo,
                        valor=valor
                    )

            # Crear el seguimiento inicial
            SeguimientoSolicitud.objects.create(
                solicitud=solicitud,
                estatus='1',
                observaciones='Solicitud creada por el usuario'
            )

            messages.success(
                request, f'Solicitud creada exitosamente. Folio: {folio}')
            return redirect('mis_solicitudes')

    context = {
        'tipos_disponibles': tipos_disponibles,
        'formulario_solicitud': formulario_solicitud,
        'campos': campos,
        'tipo_seleccionado': tipo_id
    }
    return render(request, 'tipo_solicitudes/crear_solicitud.html', context)


@login_required
def mis_solicitudes(request):
    """Vista para que el usuario vea sus propias solicitudes"""
    from django.db.models import OuterRef, Subquery
    
    # Obtener el último estatus de cada solicitud
    ultimo_seguimiento = SeguimientoSolicitud.objects.filter(
        solicitud=OuterRef('pk')
    ).order_by('-fecha_creacion')
    
    solicitudes = Solicitud.objects.filter(
        usuario=request.user
    ).annotate(
        ultimo_estatus=Subquery(ultimo_seguimiento.values('estatus')[:1])
    ).order_by('-fecha_creacion')

    estatus_filtro = request.GET.get('estatus')
    if estatus_filtro:
        solicitudes = solicitudes.filter(ultimo_estatus=estatus_filtro)

    context = {
        'solicitudes': solicitudes,
        'estatus_choices': ESTATUS,
        'estatus_filtro': estatus_filtro
    }
    return render(request, 'tipo_solicitudes/mis_solicitudes.html', context)


@login_required
def detalle_solicitud(request, solicitud_id):
    """Vista para ver el detalle completo de una solicitud"""
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)

    puede_ver = (
        solicitud.usuario == request.user or
        request.user.puede_atender_solicitudes() or
        request.user.puede_ver_dashboard()
    )

    if not puede_ver:
        messages.error(request, 'No tienes permiso para ver esta solicitud.')
        return redirect('mis_solicitudes')

    respuestas = solicitud.respuestas.all().select_related('campo')
    seguimientos = solicitud.seguimientos.all().order_by('-fecha_creacion')

    context = {
        'solicitud': solicitud,
        'respuestas': respuestas,
        'seguimientos': seguimientos,
        'estatus_dict': dict(ESTATUS)
    }
    return render(request, 'tipo_solicitudes/detalle_solicitud.html', context)


@login_required
def seguimiento_solicitud(request, solicitud_id):
    """Vista para ver el seguimiento de una solicitud específica"""
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)

    puede_ver = (
        solicitud.usuario == request.user or
        request.user.puede_atender_solicitudes() or
        request.user.puede_ver_dashboard()
    )

    if not puede_ver:
        messages.error(request, 'No tienes permiso para ver esta solicitud.')
        return redirect('mis_solicitudes')

    seguimientos = solicitud.seguimientos.all().order_by('-fecha_creacion')

    context = {
        'solicitud': solicitud,
        'seguimientos': seguimientos,
        'estatus_dict': dict(ESTATUS)
    }
    return render(request, 'tipo_solicitudes/seguimiento_solicitud.html', context)
