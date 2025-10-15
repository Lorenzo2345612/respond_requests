from django.shortcuts import render

def bienvenida(request):
    return render(request, 'bienvenida.html')


def agregar(request):
    return render(request, 'agregar_solicitud.html')