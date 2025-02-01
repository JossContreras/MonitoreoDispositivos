from django.shortcuts import redirect, render
from django.http import HttpResponse

from rest_framework import viewsets
from .models import Inventario, Ubicacion, Dispositivo
from .serializer import UbicacionSerializer

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

def index(request):
    return render (request, 'paginas/index.html')

def pagprin(request):
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

class UbicacionViewSet(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer


#LLAMAR API DESDE VISTAS
from django.shortcuts import render
import requests 

def ubicaciones_view(request):
    response = requests.get('http://127.0.0.1:8000/api/ubicaciones/')
    if response.status_code == 200:
        ubicaciones = response.json()  # Convert response to JSON
    else:
        ubicaciones = []
    return render(request, 'ubicaciones_list.html', {'ubicaciones': ubicaciones})

#==================================================================================================

def ubicacion_create(request):
    if request.method == 'POST':
        nombre_ubicacion = request.POST.get('nombre_ubicacion')
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        pais = request.POST.get('pais')

        # Crear una nueva ubicación en la base de datos
        ubicacion = Ubicacion.objects.create(
            nombre_ubicacion=nombre_ubicacion,
            direccion=direccion,
            ciudad=ciudad,
            pais=pais
        )

        # Redirigir a una página de éxito o a la lista de ubicaciones
        return redirect('ubicaciones_list')  # Cambiar a la vista que lista las ubicaciones

    return render(request, 'ubicaciones_form.html')

#==================================================================================================

def dispositivo_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        tipo_elemento = request.POST.get('tipo_elemento')
        estado = request.POST.get('estado')
        fecha_adquisicion = request.POST.get('fecha_adquisicion')
        ubicacion_id = request.POST.get('ubicacion')  # ID de la ubicación seleccionada

        # Validar que ubicacion_id no esté vacío
        if not ubicacion_id:
            return render(request, 'crear_dispositivo.html', {
                'error': 'Debe seleccionar una ubicación',
                'ubicaciones': Ubicacion.objects.all()
            })

        try:
            ubicacion = Ubicacion.objects.get(id_ubicacion=ubicacion_id)
        except Ubicacion.DoesNotExist:
            return render(request, 'crear_dispositivo.html', {
                'error': 'La ubicación seleccionada no existe',
                'ubicaciones': Ubicacion.objects.all()
            })

        # Crear el registro en la base de datos
        inventario = Inventario.objects.create(
            nombre=nombre,
            tipo_elemento=tipo_elemento,
            estado=estado,
            fecha_adquisicion=fecha_adquisicion,
            id_ubicacion=ubicacion
        )

        return redirect('ubicaciones_list')

    # Si el método no es POST, mostrar las ubicaciones
    ubicaciones = Ubicacion.objects.all()
    return render(request, 'crear_dispositivo.html', {'ubicaciones': ubicaciones})
