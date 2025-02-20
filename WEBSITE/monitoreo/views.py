import subprocess
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import JsonResponse
import mysql.connector
import os

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '0506',
    'database': 'dbinventario'
}

import mysql.connector

# Función para conectar a la base de datos usando DB_CONFIG
def conectar_bd():
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)  # Usa los valores de DB_CONFIG
        return conexion
    except mysql.connector.Error as e:
        print(f"Error de conexión a la base de datos: {e}")
        return None  # Evita que el código crashee


# Función para hacer ping
def hacer_ping(ip):
    comando = f"ping -n 1 {ip}" if os.name == "nt" else f"ping -c 1 {ip}"
    return os.system(comando) == 0  # True si responde, False si no

# Obtener ID de un dispositivo desde su IP
def obtener_id_por_ip(ip):
    print(f"🔍 Buscando IP en la base de datos: '{ip}'")  # Depuración
    conexion = mysql.connector.connect(**DB_CONFIG)
    cursor = conexion.cursor()
    
    cursor.execute("SELECT id_inventario FROM Inventario WHERE ip = %s", (ip,))
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()
    
    if resultado:
        print(f"✅ ID encontrado: {resultado[0]}")
        return resultado[0]
    else:
        print(f"❌ No se encontró la IP: {ip}")
        return None



# Obtener dispositivos enlazados a un ID
def obtener_dispositivos_enlazados(id_inventario):
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
    
    # Filtrar dispositivos que realmente tengan una IP válida
    dispositivos = [(id_disp, ip) for id_disp, ip in dispositivos if ip and ip.count('.') == 3]

    print(f"Dispositivos conectados al ID {id_inventario}: {dispositivos}")  # Depuración
    
    cursor.close()
    conexion.close()
    
    return dispositivos


# Función para analizar la ruta entre origen y destino
def analizar_ruta(request):
    if request.method == "POST":
        ip_origen = request.POST.get("ip_origen")
        ip_destino = request.POST.get("ip_destino")

        ruta = []
        visitados = set()  # 🔹 Agregar esta línea para inicializar visitados

        def recorrer_red(ip_actual):
            if ip_actual in visitados:
                return False
            visitados.add(ip_actual)

            id_actual = obtener_id_por_ip(ip_actual)
            if not id_actual:
                return False

            ruta.append(ip_actual)

            if ip_actual == ip_destino:
                return True  

            dispositivos = obtener_dispositivos_enlazados(id_actual)
            for _, ip_conectado in dispositivos:
                if recorrer_red(ip_conectado):
                    return True

            ruta.pop()
            return False

        if recorrer_red(ip_origen):
            return render(request, "index.html", {"ruta": ruta})
        else:
            return render(request, "index.html", {"ruta": ["No hay conexión disponible"]})

    return render(request, "index.html")
