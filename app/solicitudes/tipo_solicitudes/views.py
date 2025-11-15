from django.db import transaction
from django.forms import ValidationError, inlineformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from .forms import FormArchivoAdjunto, FormFormularioSolicitud, FormSolicitud, FormTipoSolicitud, FormCampoFormulario
from .models import ArchivoAdjunto, CampoFormulario, FormularioSolicitud, RespuestaCampo, Solicitud, TipoSolicitud
from .funcionalidad import FuncionesAvanzadas
from django.db.models import Max

def bienvenida(request):
    return render(request, 'bienvenida.html')


def lista_solicitudes(request):
    funciones_avanzadas = FuncionesAvanzadas()
    resultado = funciones_avanzadas.calculo_extremo(2, 2)

    context = {
        'tipo_solicitudes': TipoSolicitud.objects.all(),
        'resultado': resultado
    }
    return render(request, 'lista_tipo_solicitudes.html', context)


def agregar(request):
    if request.method == 'POST':
        form = FormTipoSolicitud(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tipo_solicitudes')   
    else:
        form = FormTipoSolicitud()

    return render(request, 'agregar_solicitud.html', {'form': form})



def generar_folio_unico():
    import uuid
    return f"FOLIO-{uuid.uuid4().hex[:8].upper()}"

def crear_formulario(request):
    if request.method == 'POST':
        form = FormFormularioSolicitud(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_formulario')
    else:
        form = FormFormularioSolicitud()
    context = {
        'form': form
    }
    return render(request, 'crear_formulario_solicitud.html', context)

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



def eliminar_campo(request, campo_id):
    campo = get_object_or_404(CampoFormulario, pk=campo_id)
    formulario_id = campo.formulario.id
    campo.delete()
    return redirect('crear_campos', formulario_id=formulario_id)
