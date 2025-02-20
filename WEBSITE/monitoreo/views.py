import subprocess
import mysql.connector
import os
import ipaddress
import time
from django.shortcuts import render
from django.http import JsonResponse

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
import os
import subprocess
import re
import os

import subprocess
import re
import os

def hacer_ping(ip):
    """Ejecuta un ping y devuelve el estado, la IP, el tiempo de respuesta y el motivo si hay error."""
    comando = ["ping", "-n", "1", ip] if os.name == "nt" else ["ping", "-c", "1", ip]

    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=2)

        if resultado.returncode == 0:
            # 🔍 Extraer el tiempo de respuesta con regex mejorado
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

def analizar_ruta(request):
    if request.method == "POST":
        ip_origen = request.POST.get("ip_origen")
        ip_destino = request.POST.get("ip_destino")

        ruta = []
        visitados = set()

        def recorrer_red(ip_actual):
            if ip_actual in visitados:
                return False
            visitados.add(ip_actual)

            id_actual = obtener_id_por_ip(ip_actual)
            if not id_actual:
                return False

            resultado_ping = hacer_ping(ip_actual)
            ruta.append(resultado_ping)  # 🔥 Ahora incluye el tiempo

            if resultado_ping["estado"] == "error":
                return False  # 🚨 Si hay error, se detiene el monitoreo

            if ip_actual == ip_destino:
                return True

            dispositivos = obtener_dispositivos_enlazados(id_actual)
            for _, ip_conectado in dispositivos:
                if recorrer_red(ip_conectado):
                    return True

            return False

        recorrer_red(ip_origen)

        return render(request, "index.html", {"ruta": ruta})

    return render(request, "index.html", {"ruta": []})
