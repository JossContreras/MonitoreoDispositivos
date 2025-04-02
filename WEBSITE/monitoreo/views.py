import subprocess
import django
from matplotlib.style import context
import mysql.connector
import os
import ipaddress
import time
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from .models import Inventario, Ubicacion

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '0506',
    'database': 'dbinventario'
}

def conectar_bd():
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        return conexion
    except mysql.connector.Error as e:
        print(f"Error de conexión a la base de datos: {e}")
        return None

def convertir_ipv6_a_ipv4(ip):
    """Convierte IPv6 a IPv4 si es una dirección mapeada."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        if isinstance(ip_obj, ipaddress.IPv6Address) and ip_obj.ipv4_mapped:
            return str(ip_obj.ipv4_mapped)
    except ValueError:
        pass
    return ip  # Si no es IPv6 mapeado, devolver la IP original

import subprocess
import re
import os

def hacer_ping(ip):
    """Ejecuta un ping y devuelve el estado, la IP, el tiempo de respuesta y el motivo si hay error."""
    if not ip:
        return {"estado": "error", "motivo": "IP no proporcionada"}

    comando = ["ping", "-n", "1", ip] if os.name == "nt" else ["ping", "-c", "1", ip]

    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=2)

        if resultado.returncode == 0:
            # 🔍 Extraer el tiempo de respuesta 
            if os.name == "nt":
                match = re.search(r"tiempo[=<]([\d]+)ms", resultado.stdout)  # Windows
            else:
                match = re.search(r"time[=<]?([\d.]+) ?ms", resultado.stdout)  # Linux/macOS

            tiempo_respuesta = match.group(1) + " ms" if match else "Desconocido"
            return {"estado": "exito", "ip": ip, "tiempo": tiempo_respuesta}

        else:
            motivo = resultado.stderr.strip() or resultado.stdout.strip()
            return {"estado": "error", "ip": ip, "motivo": motivo}

    except subprocess.TimeoutExpired:
        return {"estado": "error", "ip": ip, "motivo": "⏳ Tiempo de espera agotado."}
    except Exception as e:
        return {"estado": "error", "ip": ip, "motivo": f"⚠ Error inesperado: {str(e)}"}

def verificar_estado_dispositivo(request):
    """Recibe una IP desde la interfaz, ejecuta el ping y devuelve el resultado en JSON."""
    ip = request.GET.get('ip')

    if not ip:
        return JsonResponse({"estado": "error", "motivo": "IP no proporcionada"}, status=400)

    resultado = hacer_ping(ip)  # Llama a la función hacer_ping()
    return JsonResponse(resultado)

def obtener_id_por_ip(ip):
    """Obtiene el ID del dispositivo basado en su IP."""
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("SELECT id_inventario FROM Inventario WHERE ip = %s", (ip,))
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    return resultado[0] if resultado else None

def obtener_dispositivos_enlazados(id_inventario):
    """Obtiene los dispositivos conectados a un ID."""
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT i.id_inventario, i.ip 
        FROM Enlaces e
        JOIN Inventario i ON e.dispositivo_destino = i.id_inventario
        WHERE e.dispositivo_origen = %s
        UNION
        SELECT i.id_inventario, i.ip 
        FROM Enlaces e
        JOIN Inventario i ON e.dispositivo_origen = i.id_inventario
        WHERE e.dispositivo_destino = %s
    """, (id_inventario, id_inventario))

    dispositivos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return [(id_disp, convertir_ipv6_a_ipv4(ip)) for id_disp, ip in dispositivos if ip and ip.count('.') == 3]

from collections import deque
from collections import deque

from django.http import JsonResponse
from collections import deque

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from collections import deque

from django.http import JsonResponse
from collections import deque

def analizar_ruta(request):
    if request.method == "POST":
        ip_origen = request.POST.get("ip_origen")
        ip_destino = request.POST.get("ip_destino")

        id_origen = obtener_id_por_ip(ip_origen)
        id_destino = obtener_id_por_ip(ip_destino)

        if not id_origen or not id_destino:
            return JsonResponse({"error": "No se encontraron los dispositivos."}, status=400)

        # Paso 1: Buscar la ruta más corta con BFS
        visitados = set()
        cola = deque([(ip_origen, [])])
        ruta_mas_corta = []

        while cola:
            ip_actual, camino_actual = cola.popleft()

            if ip_actual in visitados:
                continue
            visitados.add(ip_actual)

            nuevo_camino = camino_actual + [ip_actual]

            if ip_actual == ip_destino:
                ruta_mas_corta = nuevo_camino
                break

            dispositivos = obtener_dispositivos_enlazados(obtener_id_por_ip(ip_actual))
            for _, ip_conectado in dispositivos:
                if ip_conectado not in visitados:
                    cola.append((ip_conectado, nuevo_camino))

        if not ruta_mas_corta:
            return JsonResponse({"error": "No hay conexión entre los dispositivos."}, status=400)

        # Paso 2: Hacer ping a los dispositivos en la ruta encontrada
        ruta_con_ping = []
        for ip in ruta_mas_corta:
            resultado_ping = hacer_ping(ip)
            ruta_con_ping.append(resultado_ping)

        # Devolver JSON en lugar de renderizar la plantilla
        return JsonResponse({"ruta": ruta_con_ping})

    return JsonResponse({"error": "Método no permitido"}, status=405)



 #=========================================================================================================
from django.shortcuts import render

def monitoreo_red(request):
    return render(request, "index.html")

from django.shortcuts import render
from django.http import JsonResponse
from .models import Inventario, Ubicacion, DetallesTecnicos

from django.shortcuts import render
from django.http import JsonResponse
from .models import Inventario, Ubicacion, DetallesTecnicos

def inventario_por_ubicacion(request):
    """Filtra el inventario con múltiples filtros seleccionables y devuelve datos en JSON si es AJAX."""
    ubicaciones = Ubicacion.objects.all()
    tipos = Inventario.objects.values_list('tipo_elemento', flat=True).distinct().exclude(tipo_elemento__isnull=True)
    marcas = DetallesTecnicos.objects.values_list('marca', flat=True).distinct().exclude(marca__isnull=True)
    sistemas = DetallesTecnicos.objects.values_list('sistema_operativo', flat=True).distinct().exclude(sistema_operativo__isnull=True)

    # 🔹 Obtener parámetros de búsqueda
    ubicacion_ids = request.GET.getlist('ubicacion[]')
    ip_busqueda = request.GET.get('ip')
    tipos_seleccionados = request.GET.getlist('tipo[]')
    marcas_seleccionadas = request.GET.getlist('marca[]')
    sistemas_seleccionados = request.GET.getlist('sistema[]')

    # 🔹 Aplicar filtros dinámicamente
    inventario = Inventario.objects.all()

    if ip_busqueda:
        inventario = inventario.filter(ip=ip_busqueda)
    if ubicacion_ids:
        inventario = inventario.filter(id_ubicacion__in=ubicacion_ids)
    if tipos_seleccionados:
        inventario = inventario.filter(tipo_elemento__in=tipos_seleccionados)
    if marcas_seleccionadas:
        inventario = inventario.filter(detallestecnicos__marca__in=marcas_seleccionadas)
    if sistemas_seleccionados:
        inventario = inventario.filter(detallestecnicos__sistema_operativo__in=sistemas_seleccionados)

    # 🔹 Si es una solicitud AJAX, devolver JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = [
            {
                "id_inventario": item.id_inventario,
                "nombre": item.nombre,
                "ubicacion": item.id_ubicacion.nombre_ubicacion,
                "ip": item.ip if item.ip else "No disponible",
                "tipo_elemento": item.tipo_elemento if item.tipo_elemento else "No especificado",
                "marca": item.detallestecnicos.marca if hasattr(item, 'detallestecnicos') else "No disponible",
                "sistema_operativo": item.detallestecnicos.sistema_operativo if hasattr(item, 'detallestecnicos') else "No disponible",
                "estado": item.estado if item.estado else "Desconocido",
                "fecha_adquisicion": item.fecha_adquisicion.strftime("%Y-%m-%d") if item.fecha_adquisicion else "No disponible"
            }
            for item in inventario
        ]
        return JsonResponse(data, safe=False)

    return render(request, 'monitoreo_tr.html', {
        'inventario': inventario,
        'ubicaciones': ubicaciones,
        'tipos': tipos,
        'marcas': marcas,
        'sistemas': sistemas
    })








import io
import networkx as nx
import matplotlib.pyplot as plt
from django.http import HttpResponse

def generar_grafica_red():
    G = nx.Graph()

    # Simulación de enlaces (debería venir de tu base de datos)
    enlaces = [(1, 2, "192.168.1.2"), (1, 3, "192.168.1.3"), (2, 4, "192.168.1.4"), (3, 4, "192.168.1.5")]

    for origen, destino, ip in enlaces:
        G.add_edge(origen, destino, label=ip)

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)  
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2000, font_size=10)

    labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()

    buf.seek(0)
    return buf

def mostrar_grafica(request):
    imagen = generar_grafica_red()
    return HttpResponse(imagen.getvalue(), content_type="image/png")
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tempfile
import os
from django.http import HttpResponse

def generar_animacion_red():
    # Crear un grafo dirigido
    G = nx.Graph()

    # Simulación de enlaces entre dispositivos (cambia esto por tus datos reales)
    enlaces = [
        (1, 2), (1, 3), (1, 4),  # Router conectado a dispositivos
        (2, 1), (3, 1), (4, 1)   # Dispositivos conectados de regreso
    ]

    G.add_edges_from(enlaces)

    # Posiciones de los nodos
    pos = nx.spring_layout(G)

    fig, ax = plt.subplots()

    # Función para actualizar cada frame de la animación
    def actualizar_frame(frame):
        ax.clear()
        nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightblue', edge_color='gray', node_size=700, font_size=10)
        
        # Resaltar enlaces hasta el frame actual
        if frame < len(enlaces):
            nx.draw_networkx_edges(G, pos, edgelist=[enlaces[frame]], ax=ax, edge_color='red', width=2.5)

    # Crear la animación
    ani = animation.FuncAnimation(fig, actualizar_frame, frames=len(enlaces), repeat=False)

    # Guardar en un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".gif") as temp_file:
        temp_path = temp_file.name
        ani.save(temp_path, writer="pillow", fps=1)

    with open(temp_path, "rb") as f:
        gif_data = f.read()

    os.remove(temp_path)  # Eliminar archivo temporal después de leerlo

    return HttpResponse(gif_data, content_type="image/gif")


def mostrar_animacion(request):
    imagen = generar_animacion_red()
    return HttpResponse(imagen.getvalue(), content_type="image/gif")

#==================================================================================================

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import JsonResponse
from .models import Rutas
from django.shortcuts import render
from django.http import JsonResponse
from .models import Rutas, Inventario

from django.shortcuts import render, redirect
from .models import Rutas, Inventario

# Agregar ruta
def agregar_ruta(request):
    if request.method == 'POST':
        nombre_ruta = request.POST.get('nombre_ruta')
        descripcion = request.POST.get('descripcion')
        dispositivos_seleccionados = request.POST.getlist('dispositivos')

        ruta = Rutas.objects.create(
            nombre_ruta=nombre_ruta,
            descripcion=descripcion
        )

        for dispositivo_id in dispositivos_seleccionados:
            dispositivo = Inventario.objects.get(id=dispositivo_id)
            ruta.dispositivos.add(dispositivo)

        return redirect('lista_rutas')

    dispositivos = Inventario.objects.all()
    return render(request, 'agregar_ruta.html', {'dispositivos': dispositivos})

# Listar rutas
from django.shortcuts import render
from .models import Rutas, RutaDispositivos, Inventario

def lista_rutas(request):
    # Obtenemos las rutas
    rutas = Rutas.objects.all()

    for ruta in rutas:
        # Obtenemos los inventarios relacionados a través de RutaDispositivos y los ordenamos por 'orden'
        inventarios = Inventario.objects.filter(rutadispositivos__id_ruta=ruta.id_ruta).order_by('rutadispositivos__orden')

        # Agregamos los inventarios a cada ruta para usarlos en la plantilla
        ruta.inventarios = inventarios

    return render(request, 'lista_rutas.html', {'rutas': rutas})


from django.shortcuts import render, get_object_or_404
from .models import Rutas, RutaDispositivos

def eliminar_ruta(request, id_ruta):
    # Obtener la ruta
    ruta = get_object_or_404(Rutas, id_ruta=id_ruta)
    
    # Obtener los dispositivos asociados a la ruta, ordenados por el campo 'orden'
    ruta_dispositivos = RutaDispositivos.objects.filter(id_ruta=ruta).order_by('orden')

    if request.method == 'POST':
        # Eliminar la ruta
        ruta.delete()
        return redirect('lista_rutas')
    
    # Renderizar la plantilla con los dispositivos ordenados
    return render(request, 'eliminar_ruta.html', {'ruta': ruta, 'ruta_dispositivos': ruta_dispositivos})

from django.shortcuts import render
from .models import Inventario

def ping_ruta(request, id_ruta):
    """
    Vista que obtiene los dispositivos asociados a una ruta específica.
    """
    # Obtener los dispositivos asociados a la ruta y convertirlos en una lista de diccionarios
    dispositivos = list(Inventario.objects.filter(rutadispositivos__id_ruta=id_ruta).order_by('rutadispositivos__orden').values('id_inventario', 'nombre', 'ip'))

    # Pasar los dispositivos al template como lista serializable
    return render(request, 'ping_ruta.html', {'dispositivos': dispositivos, 'id_ruta': id_ruta})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Rutas
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Rutas

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Rutas

@csrf_exempt  # 🔴 Solo para pruebas, luego usa protección CSRF
def agregar_ruta_definida(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nueva_ruta = Rutas.objects.create(
                nombre_ruta=data.get("nombre_ruta"),
                descripcion=data.get("descripcion", "")
            )
            return JsonResponse({"mensaje": "Ruta agregada correctamente"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)


from django.shortcuts import render

def formulario_agregar_ruta_definida(request):
    return render(request, 'agregar_ruta_definida.html')  # Asegúrate de que la ruta sea correcta

from django.shortcuts import render, get_object_or_404, redirect
from .models import Rutas
from django.shortcuts import render, get_object_or_404, redirect
from .models import Rutas, Inventario, RutaDispositivos

def editar_ruta(request, id_ruta):
    ruta = get_object_or_404(Rutas, id_ruta=id_ruta)
    
    # Obtener los dispositivos asociados a la ruta con su orden
    dispositivos_ruta = RutaDispositivos.objects.filter(id_ruta=ruta).select_related("id_inventario").order_by("orden")

    if request.method == "POST":
        ruta.nombre_ruta = request.POST.get("nombre_ruta")
        ruta.descripcion = request.POST.get("descripcion")
        ruta.save()
        return redirect("lista_rutas")  # Redirigir después de guardar

    return render(request, "editar_ruta.html", {"ruta": ruta, "dispositivos_ruta": dispositivos_ruta})



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import RutaDispositivos
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RutaDispositivos

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RutaDispositivos

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

@csrf_exempt
def eliminar_dispositivo_ruta_definida(request, id_ruta, id_dispositivo):
    if request.method == "POST":
        print(f"Intentando eliminar dispositivo con id: {id_dispositivo} en ruta: {id_ruta}")  # Debugging

        relacion = get_object_or_404(RutaDispositivos, id=id_dispositivo, id_ruta=id_ruta)
        relacion.delete()

        # Reordenar los dispositivos restantes en la ruta
        dispositivos_restantes = RutaDispositivos.objects.filter(id_ruta=id_ruta).order_by('orden')
        for i, dispositivo in enumerate(dispositivos_restantes, start=1):
            dispositivo.orden = i
            dispositivo.save()

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Método no permitido"}, status=405)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Inventario, Rutas, RutaDispositivos  # Asegúrate de usar los modelos correctos

@csrf_exempt
def agregar_dispositivo_por_ip(request, id_ruta):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ip = data.get("ip")

            # Buscar el dispositivo en la base de datos
            dispositivo = Inventario.objects.filter(ip=ip).first()

            if not dispositivo:
                return JsonResponse({"success": False, "error": "El dispositivo no existe"}, status=400)

            # Verificar si el dispositivo ya está en la ruta
            if RutaDispositivos.objects.filter(id_ruta_id=id_ruta, id_inventario=dispositivo).exists():
                return JsonResponse({"success": False, "error": "El dispositivo ya está en esta ruta"}, status=400)

            # Obtener el último orden y sumarle 1
            ultimo_orden = RutaDispositivos.objects.filter(id_ruta_id=id_ruta).order_by("-orden").first()
            nuevo_orden = (ultimo_orden.orden + 1) if ultimo_orden else 1

            # Crear la relación
            nueva_relacion = RutaDispositivos.objects.create(
                id_ruta_id=id_ruta,  # Cambiado de ruta_id a id_ruta_id
                id_inventario=dispositivo,
                orden=nuevo_orden
            )

            return JsonResponse({
                "success": True,
                "id": nueva_relacion.id,
                "nombre": dispositivo.nombre,
                "ip": dispositivo.ip,
                "orden": nuevo_orden
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

from django.http import JsonResponse
from .models import Inventario  # Asegúrate de importar tu modelo correctamente
from django.http import JsonResponse
from .models import Inventario  # Asegúrate de importar correctamente

def buscar_dispositivo(request):
    try:
        ip_query = request.GET.get('ip', '').strip()
        
        if not ip_query:
            return JsonResponse({'error': 'No se proporcionó una IP'}, status=400)

        # Consulta correcta sin renombrar claves
        dispositivos = Inventario.objects.filter(ip__icontains=ip_query).values('id_inventario', 'nombre', 'ip')

        # 🔹 Imprimir para depuración
        print("📡 Dispositivos encontrados:", list(dispositivos))

        return JsonResponse(list(dispositivos), safe=False)
    
    except Exception as e:
        print("❌ Error en buscar_dispositivo:", str(e))
        return JsonResponse({'error': str(e)}, status=500)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from monitoreo.models import Inventario, RutaDispositivos, Rutas

import json
from django.http import JsonResponse

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Rutas, Inventario, RutaDispositivos  # Asegúrate de importar los modelos adecuados

@csrf_exempt
def agregar_multiples_dispositivos(request, id_ruta):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("📩 Datos recibidos:", data)  # 🔹 Debug: Verificar si los datos llegan correctamente
            
            dispositivos = data.get('dispositivos', [])
            ruta = Rutas.objects.get(id_ruta=id_ruta)

            for index, dispositivo in enumerate(dispositivos, start=1):
                inventario = Inventario.objects.get(id_inventario=dispositivo['id'])
                RutaDispositivos.objects.create(
                    id_ruta=ruta,
                    id_inventario=inventario,
                    orden=index
                )

            return JsonResponse({'success': True})
        
        except Exception as e:
            print("❌ Error en la API:", str(e))
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

from django.http import JsonResponse
from .models import RutaDispositivos

def obtener_dispositivos_ruta(request, id_ruta):
    dispositivos = RutaDispositivos.objects.filter(id_ruta=id_ruta).select_related('id_inventario')
    
    data = []
    for dispositivo in dispositivos:
        data.append({
            "id": dispositivo.id,
            "id_ruta": id_ruta,
            "id_inventario": dispositivo.id_inventario.id_inventario,
            "nombre": dispositivo.id_inventario.nombre,  # 👈 Ahora enviamos el nombre correcto
            "ip": dispositivo.id_inventario.ip,  # 👈 Ahora enviamos la IP correcta
            "orden": dispositivo.orden
        })
    
    return JsonResponse({"dispositivos": data})


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import RutaDispositivos

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import RutaDispositivos, Rutas

def actualizar_orden(request, id_ruta):
    if request.method == "POST":
        # Obtener la lista de dispositivos con el nuevo orden
        dispositivos_data = request.POST.getlist('dispositivos[]')  # Recibimos la lista de dispositivos

        if not dispositivos_data:
            return JsonResponse({"error": "No se proporcionaron dispositivos para actualizar el orden."}, status=400)

        # Actualizar el orden en la base de datos
        for index, dispositivo in enumerate(dispositivos_data):
            dispositivo_id = dispositivo.split("_")[0]  # Extraemos el id del dispositivo
            try:
                # Obtener el objeto RutaDispositivo y actualizar su orden
                ruta_dispositivo = RutaDispositivos.objects.get(id_ruta=id_ruta, id_inventario=dispositivo_id)
                ruta_dispositivo.orden = index + 1  # Asignamos el nuevo orden (index+1 para que empiece desde 1)
                ruta_dispositivo.save()
            except RutaDispositivos.DoesNotExist:
                return JsonResponse({"error": f"Dispositivo con ID {dispositivo_id} no encontrado en la ruta."}, status=404)

        return JsonResponse({"success": "Orden actualizado correctamente"}, status=200)

    return JsonResponse({"error": "Método no permitido"}, status=405)

from django.http import JsonResponse
from .models import RutaDispositivos
import json

def actualizar_orden_id(request, id_ruta):
    if request.method == "POST":
        try:
            dispositivos_data = json.loads(request.body).get('dispositivos', [])

            if not dispositivos_data:
                return JsonResponse({"error": "No se proporcionaron dispositivos para actualizar el orden."}, status=400)

            for index, dispositivo_id in enumerate(dispositivos_data):
                try:
                    ruta_dispositivo = RutaDispositivos.objects.get(id_ruta=id_ruta, id_inventario=dispositivo_id)
                    ruta_dispositivo.orden = index + 1  # Orden nuevo comenzando desde 1
                    ruta_dispositivo.save()
                except RutaDispositivos.DoesNotExist:
                    return JsonResponse({"error": f"Dispositivo con ID {dispositivo_id} no encontrado en la ruta."}, status=404)

            return JsonResponse({"success": "Orden actualizado correctamente"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Datos inválidos proporcionados."}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)

from django.shortcuts import render

# Vista para la página principal de monitoreofrom django.shortcuts import render

# Asegúrate de que la vista 'monitoreo' esté definida aquí
def monitoreointerfaz(request):
    context = {
        'num_rutas': 10,  # Puedes personalizar con tus propios datos
        'num_dispositivos': 25,
        'estado_red': "Operativa",
    }
    return render(request, 'home.html', context)


def navbarinterfaz(request):
    return render(request, 'nav_bar.html')


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import HistorialRutaDispositivo
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # Si no estás usando CSRF en las peticiones AJAX, de lo contrario elimínalo

def guardar_historial(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ruta_id = data.get('ruta_id')
        dispositivos_con_error = data.get('dispositivos_con_error')
        fecha = data.get('fecha')

        # Crear un nuevo registro en la tabla Historial_Ruta_Dispositivo
        historial = HistorialRutaDispositivo(
            id_ruta=ruta_id,
            dispositivos_con_error=','.join(map(str, dispositivos_con_error)),  # Convertir la lista a cadena
            fecha=fecha
        )
        historial.save()

        return JsonResponse({'status': 'success', 'message': 'Historial agregado correctamente'}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

from django.shortcuts import render
from .models import Inventario, Ubicacion
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Vista para mostrar la interfaz de filtros
from django.shortcuts import render
from .models import Inventario, Ubicacion

def interfaz_filtros(request):
    # Obtener todos los dispositivos
    dispositivos = Inventario.objects.all()

    # Obtener listas únicas para cada campo (para poblar los dropdowns)
    modelos = Inventario.objects.values_list('modelo', flat=True).distinct()
    sistemas_operativos = Inventario.objects.values_list('sistema_operativo', flat=True).distinct()
    tipos_elementos = Inventario.objects.values_list('tipo_elemento', flat=True).distinct()
    ubicaciones = Ubicacion.objects.all()

    # Filtrar por los valores seleccionados
    modelo = request.GET.get('modelo', '')
    sistema_operativo = request.GET.get('sistema_operativo', '')
    tipo_elemento = request.GET.get('tipo_elemento', '')
    ubicacion = request.GET.get('ubicacion', '')

    if modelo:
        dispositivos = dispositivos.filter(modelo=modelo)
    if sistema_operativo:
        dispositivos = dispositivos.filter(sistema_operativo=sistema_operativo)
    if tipo_elemento:
        dispositivos = dispositivos.filter(tipo_elemento=tipo_elemento)
    if ubicacion:
        dispositivos = dispositivos.filter(id_ubicacion__nombre_ubicacion=ubicacion)

    context = {
        'dispositivos': dispositivos,
        'modelos': modelos,
        'sistemas_operativos': sistemas_operativos,
        'tipos_elementos': tipos_elementos,
        'ubicaciones': ubicaciones,
    }
    return render(request, 'reportes.html', context)


from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from .models import Inventario, DetallesTecnicos

def generar_pdf(request):
    dispositivos = Inventario.objects.all()  # Obtener todos los dispositivos inicialmente

    # Obtener los filtros de la URL (si existen)
    filtro_modelo = request.GET.get('modelo')
    filtro_sistema = request.GET.get('sistema_operativo')
    filtro_tipo = request.GET.get('tipo_elemento')
    filtro_ubicacion = request.GET.get('ubicacion')

    # Aplicar los filtros si existen
    if filtro_modelo:
        dispositivos = dispositivos.filter(detallestecnicos__modelo=filtro_modelo)
    if filtro_sistema:
        dispositivos = dispositivos.filter(detallestecnicos__sistema_operativo=filtro_sistema)
    if filtro_tipo:
        dispositivos = dispositivos.filter(tipo_elemento=filtro_tipo)
    if filtro_ubicacion:
        dispositivos = dispositivos.filter(id_ubicacion=filtro_ubicacion)

    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="dispositivos_filtrados.pdf"'

    # Usar `landscape(letter)` para orientación horizontal (paisaje)
    p = SimpleDocTemplate(response, pagesize=landscape(letter))  # Esto asegura que sea paisaje
    width, height = landscape(letter)  # Esto toma el tamaño de la página en orientación paisaje

    # Datos para la tabla
    data = [["Nombre", "Modelo", "Tipo", "Ubicación", "Sistema Operativo", "Número de Serie"]]

    for dispositivo in dispositivos:
        # Acceder a los detalles técnicos del dispositivo
        detalles_tecnicos = dispositivo.detallestecnicos_set.first()  # Relación inversa

        # Agregar los datos a la tabla
        if detalles_tecnicos:
            data.append([dispositivo.nombre,
                         detalles_tecnicos.modelo if detalles_tecnicos.modelo else "N/A",
                         dispositivo.tipo_elemento,
                         dispositivo.id_ubicacion.nombre_ubicacion,
                         detalles_tecnicos.sistema_operativo if detalles_tecnicos.sistema_operativo else "N/A",
                         detalles_tecnicos.numero_serie if detalles_tecnicos.numero_serie else "N/A"])
        else:
            data.append([dispositivo.nombre,
                         "N/A",
                         dispositivo.tipo_elemento,
                         dispositivo.id_ubicacion.nombre_ubicacion,
                         "N/A",
                         "N/A"])

    # Crear la tabla
    table = Table(data, colWidths=[width * 0.18, width * 0.12, width * 0.12, width * 0.18, width * 0.18, width * 0.18])

    # Establecer los estilos de la tabla
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Rejilla de la tabla
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Color de fondo de la cabecera
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Color del texto de la cabecera
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear todo al centro
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Usar Arial como fuente
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Fuente pequeña (Arial tamaño 10)
        ('TOPPADDING', (0, 0), (-1, -1), 5),  # Espaciado superior de las celdas
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # Espaciado inferior de las celdas
        ('LEFTPADDING', (0, 0), (-1, -1), 5),  # Espaciado izquierdo de las celdas
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),  # Espaciado derecho de las celdas
        ('WORDSPACE', (0, 0), (-1, -1), 2),  # Separación entre palabras (para mejorar ajuste)
        ('WORDWRAP', (0, 0), (-1, -1), True),  # Ajustar el texto
    ]))

    # Construir el documento PDF
    elements = [table]
    p.build(elements)

    return response

from django.shortcuts import render
from .models import DetallesTecnicos, Inventario, Ubicacion

from django.shortcuts import render
from .models import DetallesTecnicos, Inventario, Ubicacion

from django.shortcuts import render
from .models import Inventario, DetallesTecnicos, Ubicacion

def filtro_dispositivos(request):
    dispositivos = Inventario.objects.all()
    ubicaciones = Ubicacion.objects.all()
    modelos = DetallesTecnicos.objects.values_list('modelo', flat=True).distinct()
    sistemas_operativos = DetallesTecnicos.objects.values_list('sistema_operativo', flat=True).distinct()
    tipos_elemento = Inventario.objects.values_list('tipo_elemento', flat=True).distinct()

    # Ahora recibimos los filtros usando GET
    filtro_modelo = request.GET.get('modelo')
    filtro_sistema = request.GET.get('sistema_operativo')
    filtro_tipo = request.GET.get('tipo_elemento')
    filtro_ubicacion = request.GET.get('ubicacion')

    # Aplicamos los filtros si los parámetros están presentes
    if filtro_modelo:
        dispositivos = dispositivos.filter(detallestecnicos__modelo=filtro_modelo)
    if filtro_sistema:
        dispositivos = dispositivos.filter(detallestecnicos__sistema_operativo=filtro_sistema)
    if filtro_tipo:
        dispositivos = dispositivos.filter(tipo_elemento=filtro_tipo)
    if filtro_ubicacion:
        dispositivos = dispositivos.filter(id_ubicacion=filtro_ubicacion)

    context = {
        'dispositivos': dispositivos,
        'ubicaciones': ubicaciones,
        'modelos': modelos,
        'sistemas_operativos': sistemas_operativos,
        'tipos_elemento': tipos_elemento,
    }

    return render(request, 'reportes.html', context)

import openpyxl
from django.http import HttpResponse
from .models import Inventario, DetallesTecnicos, Ubicacion

import openpyxl
from django.http import HttpResponse
from .models import Inventario, DetallesTecnicos, Ubicacion

def generar_excel(request):
    dispositivos = Inventario.objects.all()

    # Recuperamos los filtros de la URL
    filtro_modelo = request.GET.get('modelo')
    filtro_sistema = request.GET.get('sistema_operativo')
    filtro_tipo = request.GET.get('tipo_elemento')
    filtro_ubicacion = request.GET.get('ubicacion')

    # Aplicar los filtros según los parámetros pasados
    if filtro_modelo:
        dispositivos = dispositivos.filter(detallestecnicos__modelo=filtro_modelo)
    if filtro_sistema:
        dispositivos = dispositivos.filter(detallestecnicos__sistema_operativo=filtro_sistema)
    if filtro_tipo:
        dispositivos = dispositivos.filter(tipo_elemento=filtro_tipo)
    if filtro_ubicacion:
        dispositivos = dispositivos.filter(id_ubicacion=filtro_ubicacion)

    # Crear un libro de trabajo de Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Dispositivos Filtrados"

    # Escribir encabezados en el archivo Excel
    encabezados = ["Nombre", "Modelo", "Tipo", "Ubicación", "Sistema Operativo", "Número de Serie"]
    ws.append(encabezados)

    # Llenar los datos de los dispositivos en el archivo Excel
    for dispositivo in dispositivos:
        detalles_tecnicos = dispositivo.detallestecnicos_set.first()  # Relación inversa

        if detalles_tecnicos:
            ws.append([dispositivo.nombre,
                       detalles_tecnicos.modelo if detalles_tecnicos.modelo else "N/A",
                       dispositivo.tipo_elemento,
                       dispositivo.id_ubicacion.nombre_ubicacion,
                       detalles_tecnicos.sistema_operativo if detalles_tecnicos.sistema_operativo else "N/A",
                       detalles_tecnicos.numero_serie if detalles_tecnicos.numero_serie else "N/A"])
        else:
            ws.append([dispositivo.nombre,
                       "N/A",
                       dispositivo.tipo_elemento,
                       dispositivo.id_ubicacion.nombre_ubicacion,
                       "N/A",
                       "N/A"])

    # Crear la respuesta HTTP con el archivo Excel como contenido
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="dispositivos_filtrados.xlsx"'

    # Guardar el archivo Excel en la respuesta
    wb.save(response)
    
    return response
