from django.db import transaction
from django.forms import ValidationError, inlineformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from .forms import FormArchivoAdjunto, FormFormularioSolicitud, FormSolicitud, FormTipoSolicitud
from .models import ArchivoAdjunto, CampoFormulario, FormularioSolicitud, RespuestaCampo, Solicitud, TipoSolicitud
from .funcionalidad import FuncionesAvanzadas

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