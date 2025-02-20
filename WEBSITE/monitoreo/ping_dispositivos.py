import mysql
import ping3
import time
from datetime import datetime
import mysql.connector

# Configuración de conexión a la base de datos

DB_CONFIG = {
    'database': 'dbinventario',  # Cambia 'dbname' a 'database'
    'user': 'root',
    'password': '0506',
    'host': 'localhost',
    'port': '3306'  # Puerto por defecto de MySQL
}


# Conectar a la base de datos
def conectar_bd():
    return mysql.connector.connect(**DB_CONFIG)  # Para MySQL

# Función para hacer ping a una IP
def hacer_ping(ip):
    respuesta = ping3.ping(ip, timeout=2)
    return 'Activo' if respuesta else 'Inactivo'

# Función para actualizar el estado en la base de datos
def actualizar_estado_dispositivos():
    conexion = conectar_bd()
    cursor = conexion.cursor()

    # Obtener todos los dispositivos con IP registrada
    cursor.execute("SELECT id_inventario, ip FROM Inventario WHERE ip IS NOT NULL")
    dispositivos = cursor.fetchall()

    for dispositivo in dispositivos:
        id_dispositivo, ip = dispositivo
        estado = hacer_ping(ip)
        print(f"Ping a {ip} - Estado: {estado}")

        # Actualizar estado en la tabla Inventario
        cursor.execute("UPDATE Inventario SET estado = %s WHERE id_inventario = %s", (estado, id_dispositivo))

        # Insertar en historial de monitoreo
        cursor.execute("INSERT INTO Monitoreo (id_inventario, estado) VALUES (%s, %s)", (id_dispositivo, estado))

    conexion.commit()
    cursor.close()
    conexion.close()

# Ejecutar cada 60 segundos (puedes cambiar el tiempo)
if __name__ == "__main__":
    while True:
        actualizar_estado_dispositivos()
        print("Actualización completada. Esperando 60 segundos...")
        time.sleep(60)
