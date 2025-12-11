from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from solicitudes_app.decorators import puede_atender_solicitudes
from tipo_solicitudes.models import Solicitud, SeguimientoSolicitud
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CerrarSolicitudForm
from django.db.models import OuterRef, Subquery, Q
from django.core.paginator import Paginator


MATCH_RESPONSABLES = {
    'control_escolar': '1',
    'responsable_programa': '2',
    'responsable_tutorias': '3',
    'director': '4',
}


@login_required
@puede_atender_solicitudes
def atender_solicitud(request, solicitud_id: int):
    if request.method != 'GET':
        messages.error(request, 'Método no permitido.')
        return JsonResponse({'error': 'Metodo no permitido.'}, status=405)
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    ultimo = solicitud.seguimientos.order_by('-fecha_creacion').first()
    responsable_rol = MATCH_RESPONSABLES.get(request.user.rol) or "5"
    if solicitud.tipo_solicitud.responsable != responsable_rol:
        messages.error(
            request, 'No tienes permiso para atender esta solicitud.')
        return redirect('bienvenida')
    context = {
        'solicitud': solicitud,
        'ultimo': ultimo
    }
    return render(request, 'atender_solicitud.html', context)


@login_required
@puede_atender_solicitudes
def marcar_solicitud_en_proceso(request, solicitud_id: int):
    if request.method != 'POST':
        messages.error(request, 'Método no permitido.')
        return redirect('atender_solicitud', solicitud_id=solicitud_id)
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    ultimo = solicitud.seguimientos.order_by('-fecha_creacion').first()
    responsable_rol = MATCH_RESPONSABLES.get(request.user.rol) or "5"
    if solicitud.tipo_solicitud.responsable != responsable_rol:
        messages.error(
            request, 'No tienes permiso para atender esta solicitud.')
        return redirect('bienvenida')
    if not ultimo or ultimo.estatus != '1':
        messages.error(
            request,
            (
                'No se puede cambiar el estatus: '
                'la solicitud no está en estado Creada.'
            )
        )

        return redirect('atender_solicitud', solicitud_id=solicitud_id)
    SeguimientoSolicitud.objects.create(
        solicitud=solicitud, estatus='2', observaciones='')
    messages.success(request, 'La solicitud fue marcada como En proceso.')
    return redirect('atender_solicitud', solicitud_id=solicitud_id)


@login_required
@puede_atender_solicitudes
def cerrar_solicitud(request, solicitud_id: int):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    responsable_rol = MATCH_RESPONSABLES.get(request.user.rol) or "5"
    if solicitud.tipo_solicitud.responsable != responsable_rol:
        messages.error(
            request, 'No tienes permiso para atender esta solicitud.')
        return redirect('bienvenida')
    ultimo = solicitud.seguimientos.order_by('-fecha_creacion').first()
    if not ultimo or ultimo.estatus != '2':
        messages.error(request, 'Solo se puede cerrar si está En proceso.')
        return redirect('atender_solicitud', solicitud_id=solicitud_id)
    if request.method != 'POST':
        messages.error(request, 'Método no permitido.')
        return redirect('atender_solicitud', solicitud_id=solicitud_id)

    form = CerrarSolicitudForm(request.POST)
    if not form.is_valid():
        for error in form.errors.values():
            messages.error(request, error)
        return redirect('atender_solicitud', solicitud_id=solicitud_id)

    estatus = form.cleaned_data['estatus']  # normalizado a '3' o '4'
    observaciones = form.cleaned_data['observaciones'].strip()

    SeguimientoSolicitud.objects.create(
        solicitud=solicitud,
        estatus=estatus,
        observaciones=observaciones
    )
    messages.success(request, 'Solicitud cerrada correctamente.')
    return redirect('atender_solicitud', solicitud_id=solicitud_id)


@login_required
@puede_atender_solicitudes
def listar_solicitudes(request):
    estatus, search, per_page = obtener_parametros(request)
    responsable_rol = MATCH_RESPONSABLES.get(request.user.rol) or "5"

    solicitudes_qs = obtener_solicitudes_filtradas(
        responsable_rol,
        search,
        estatus
    )
    conteos = calcular_conteos(solicitudes_qs, responsable_rol)

    page_obj = paginar_solicitudes(
        solicitudes_qs,
        per_page,
        request.GET.get('page')
    )

    return render(request, 'solicitudes_table.html', {
        'page_obj': page_obj,
        'solicitudes': page_obj,
        'estatus_activo': estatus or 'todos',
        'conteos': conteos,
        'search': search,
        'per_page': per_page,
    })


def obtener_parametros(request):
    estatus = request.GET.get('estatus')
    search = (request.GET.get('search') or '').strip()
    try:
        per_page = int(request.GET.get('per_page', 10))
    except ValueError:
        per_page = 10
    if per_page not in [5, 10, 25, 50]:
        per_page = 10
    return estatus, search, per_page


def obtener_solicitudes_filtradas(responsable_rol, search, estatus):
    ult_seguimiento = SeguimientoSolicitud.objects.filter(
        solicitud=OuterRef('pk')
    ).order_by('-fecha_creacion')

    solicitudes_qs = Solicitud.objects.annotate(
        ultimo_estatus=Subquery(ult_seguimiento.values('estatus')[:1])
    )

    if responsable_rol in ['1', '2', '3', '4']:
        solicitudes_qs = solicitudes_qs.filter(
            tipo_solicitud__responsable=responsable_rol
        )

    if search:
        solicitudes_qs = solicitudes_qs.filter(
            Q(folio__icontains=search)
            | Q(usuario__username__icontains=search)
            | Q(usuario__first_name__icontains=search)
            | Q(usuario__last_name__icontains=search)
            | Q(tipo_solicitud__nombre__icontains=search)
        )

    if estatus and estatus in ['1', '2', '3', '4']:
        if estatus == '1':
            solicitudes_qs = solicitudes_qs.filter(
                Q(ultimo_estatus='1') | Q(ultimo_estatus__isnull=True)
            )
        else:
            solicitudes_qs = solicitudes_qs.filter(ultimo_estatus=estatus)

    return solicitudes_qs


def calcular_conteos(solicitudes_qs, responsable_rol):
    base_qs = solicitudes_qs
    if responsable_rol in ['1', '2', '3', '4']:
        base_qs = base_qs.filter(tipo_solicitud__responsable=responsable_rol)

    return {
        '1': base_qs.filter(
            Q(ultimo_estatus='1') | Q(ultimo_estatus__isnull=True)
        ).count(),
        '2': base_qs.filter(ultimo_estatus='2').count(),
        '3': base_qs.filter(ultimo_estatus='3').count(),
        '4': base_qs.filter(ultimo_estatus='4').count(),
        'todos': base_qs.count(),
    }


def paginar_solicitudes(solicitudes_qs, per_page, page_number):
    paginator = Paginator(solicitudes_qs.order_by('-fecha_creacion'), per_page)
    return paginator.get_page(page_number)
