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
    # Obtenemos las rutas y sus inventarios asociados a través del modelo intermedio
    rutas = Rutas.objects.all()

    for ruta in rutas:
        # Obtenemos los inventarios relacionados a través de RutaDispositivos
        inventarios = Inventario.objects.filter(rutadispositivos__id_ruta=ruta.id_ruta)

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
