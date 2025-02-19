from datetime import date
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets
from .models import Configuracion, DetallesTecnicos, Inventario, Ubicacion, Dispositivo
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

#==================================================================================================

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from datetime import date
from .models import Inventario, Ubicacion, DetallesTecnicos, Configuracion

@csrf_exempt  # 🔥 Desactiva la verificación CSRF para esta función
def insertar_dispositivo(request):
    if request.method == "POST":
        try:
            # 📌 Cargar los datos desde JSON (para Postman)
            data = json.loads(request.body.decode("utf-8"))

            # Obtener los datos
            nombre = data.get("nombre_dispositivo")
            tipo_elemento = data.get("tipo_elemento")
            estado = data.get("estado")
            fecha_adquisicion = data.get("fecha_adquisicion")
            id_ubicacion = data.get("ubicacion")

            marca = data.get("marca")
            modelo = data.get("modelo")
            numero_serie = data.get("numero_serie")
            sistema_operativo = data.get("sistema_operativo")
            version_firmware = data.get("version_firmware")

            descripcion_configuracion = data.get("descripcion_configuracion")
            parametros_personalizados = data.get("parametros_personalizados")

            # Verificar si la ubicación existe
            ubicacion = get_object_or_404(Ubicacion, id_ubicacion=id_ubicacion)

            # Guardar en la tabla Inventario
            nuevo_dispositivo = Inventario.objects.create(
                nombre=nombre,
                tipo_elemento=tipo_elemento,
                estado=estado,
                fecha_adquisicion=fecha_adquisicion,
                id_ubicacion=ubicacion
            )

            # Guardar en la tabla DetallesTecnicos
            DetallesTecnicos.objects.create(
                id_inventario=nuevo_dispositivo,
                marca=marca,
                modelo=modelo,
                numero_serie=numero_serie,
                sistema_operativo=sistema_operativo,
                version_firmware=version_firmware
            )

            # Guardar en la tabla Configuracion
            Configuracion.objects.create(
                id_inventario=nuevo_dispositivo,
                descripcion=descripcion_configuracion,
                parametros_personalizados=parametros_personalizados,
                ultima_actualizacion=date.today()
            )

            return JsonResponse({"mensaje": "Dispositivo insertado correctamente"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)


#==================================================================================================

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Inventario, Configuracion, DetallesTecnicos

@api_view(["DELETE"])
def eliminar_inventario_api(request, id_inventario):
    """Elimina un inventario junto con su configuración y detalles técnicos."""
    try:
        # Buscar el inventario
        inventario = Inventario.objects.get(id_inventario=id_inventario)

        # Eliminar registros dependientes
        configuraciones_eliminadas, _ = Configuracion.objects.filter(id_inventario=id_inventario).delete()
        detalles_eliminados, _ = DetallesTecnicos.objects.filter(id_inventario=id_inventario).delete()

        # Eliminar el inventario
        inventario.delete()

        return Response({
            "mensaje": f"Inventario con ID {id_inventario} eliminado correctamente.",
            "detalles_eliminados": detalles_eliminados,
            "configuraciones_eliminadas": configuraciones_eliminadas,
        }, status=200)

    except Inventario.DoesNotExist:
        return Response({"error": "No se encontró un inventario con ese ID."}, status=404)

#==================================================================================================

def eliminar_inventario(request):
    return render(request, "dispositivos/eliminar.html")

#==================================================================================================

import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from .models import Inventario, DetallesTecnicos, Configuracion, Ubicacion

@csrf_exempt  # 🔥 Desactiva CSRF para pruebas (en producción, usa protección CSRF)
def actualizar_dispositivo(request, id_inventario):
    """Actualiza un dispositivo ya existente."""
    
    # Si es una petición POST (desde formulario HTML)
    if request.method == "POST":
        try:
            # Obtener datos del formulario
            nombre = request.POST.get("nombre_dispositivo")
            tipo_elemento = request.POST.get("tipo_elemento")
            estado = request.POST.get("estado")
            fecha_adquisicion = request.POST.get("fecha_adquisicion")
            id_ubicacion = request.POST.get("ubicacion")

            marca = request.POST.get("marca")
            modelo = request.POST.get("modelo")
            numero_serie = request.POST.get("numero_serie")
            sistema_operativo = request.POST.get("sistema_operativo")
            version_firmware = request.POST.get("version_firmware")

            descripcion_configuracion = request.POST.get("descripcion_configuracion")
            parametros_personalizados = request.POST.get("parametros_personalizados")

            # Buscar inventario
            inventario = get_object_or_404(Inventario, id_inventario=id_inventario)

            # Actualizar datos
            inventario.nombre = nombre
            inventario.tipo_elemento = tipo_elemento
            inventario.estado = estado
            inventario.fecha_adquisicion = fecha_adquisicion

            if id_ubicacion:
                ubicacion = get_object_or_404(Ubicacion, id_ubicacion=id_ubicacion)
                inventario.id_ubicacion = ubicacion

            inventario.save()

            # Actualizar detalles técnicos
            detalles = DetallesTecnicos.objects.filter(id_inventario=id_inventario).first()
            if detalles:
                detalles.marca = marca
                detalles.modelo = modelo
                detalles.numero_serie = numero_serie
                detalles.sistema_operativo = sistema_operativo
                detalles.version_firmware = version_firmware
                detalles.save()

            # Actualizar configuración
            configuracion = Configuracion.objects.filter(id_inventario=id_inventario).first()
            if configuracion:
                configuracion.descripcion = descripcion_configuracion
                configuracion.parametros_personalizados = parametros_personalizados
                configuracion.ultima_actualizacion = date.today()
                configuracion.save()

            return redirect("inicioo")  # Redirigir a la página principal

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    # Si es una petición GET, cargar datos en el formulario
    else:
        inventario = get_object_or_404(Inventario, id_inventario=id_inventario)
        detalles = DetallesTecnicos.objects.filter(id_inventario=id_inventario).first()
        configuracion = Configuracion.objects.filter(id_inventario=id_inventario).first()
        ubicaciones = Ubicacion.objects.all()

        return render(request, "dispositivos/editar.html", {
            "inventario": inventario,
            "detalles": detalles,
            "configuracion": configuracion,
            "ubicaciones": ubicaciones
        })

#==================================================================================================

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Incidentes, Inventario

@csrf_exempt
def agregar_incidente(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            # Obtener los datos del JSON
            id_inventario = data.get("id_inventario")
            fecha_mantenimiento = data.get("fecha_mantenimiento")
            tipo_mantenimiento = data.get("tipo_mantenimiento")
            descripcion = data.get("descripcion")
            realizado_por = data.get("realizado_por")

            # Validar que el inventario existe
            inventario = Inventario.objects.get(id_inventario=id_inventario)

            # Crear el incidente
            nuevo_incidente = Incidentes.objects.create(
                id_inventario=inventario,
                fecha_mantenimiento=fecha_mantenimiento,
                tipo_mantenimiento=tipo_mantenimiento,
                descripcion=descripcion,
                realizado_por=realizado_por
            )

            return JsonResponse({"mensaje": "Incidente registrado correctamente"}, status=201)

        except Inventario.DoesNotExist:
            return JsonResponse({"error": "El inventario no existe"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)

#==================================================================================================

from django.shortcuts import render
from .models import Inventario

def formulario_incidente(request):
    inventarios = Inventario.objects.all()  # Obtener inventarios disponibles
    return render(request, "dispositivos/incidentes.html", {"inventarios": inventarios})
