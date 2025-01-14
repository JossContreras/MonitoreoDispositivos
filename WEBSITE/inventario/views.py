from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render (request, 'paginas/index.html')

def inicio(request):
    return render (request, 'paginas/inicio.html')

def crear_dispositivo(request):
    return render (request, 'dispositivos/crear.html')

def cambiar_dispositivo(request):
    return render (request, 'dispositivos/cambios.html')

def editar_dispositivo(request):
    return render (request, 'dispositivos/editar.html')

def incidentes(request):
    return render (request, 'dispositivos/incidentes.html')

def eliminar_dispositivo(request):
    return render (request, 'dispositivos/eliminar.html')

def iniciar_cuenta(request):
    return render (request, 'login/login.html')

def registrar_cuenta(request):
    return render (request, 'login/registrar.html')