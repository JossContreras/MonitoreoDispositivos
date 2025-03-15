INSERT INTO Ubicacion (nombre_ubicacion, direccion, ciudad, pais) VALUES
('Oficina Principal', 'Av. Reforma 123', 'Ciudad de México', 'México'),
('Centro de Datos', 'Calle 10 #45', 'Guadalajara', 'México'),
('Sucursal Norte', 'Av. Insurgentes 234', 'Monterrey', 'México');

INSERT INTO Dependencia (nombre_dependencia, descripcion, contacto, telefono_contacto) VALUES
('Departamento de TI', 'Administración de la red y servidores', 'Carlos Pérez', '+52 55 1234 5678'),
('Infraestructura', 'Gestión de hardware y redes', 'Ana Gómez', '+52 33 8765 4321');

INSERT INTO Ubicacion_Dependencia (id_ubicacion, id_dependencia) VALUES
(1, 1),
(2, 1),
(3, 2);

INSERT INTO Inventario (nombre, tipo_elemento, estado, fecha_adquisicion, id_ubicacion, ip) VALUES
('Router Cisco A1', 'Router', 'Activo', '2023-01-15', 1, '192.168.1.1'),
('Switch HP ProCurve', 'Switch', 'Activo', '2022-11-20', 2, '192.168.1.2'),
('Access Point Ubiquiti 1', 'Access Point', 'Inactivo', '2023-05-10', 3, '192.168.1.3'),
('Router MikroTik R2', 'Router', 'Activo', '2023-02-25', 1, '192.168.1.4'),
('Switch Cisco Catalyst', 'Switch', 'Inactivo', '2022-09-10', 2, '192.168.1.5');


INSERT INTO Detalles_Tecnicos (id_inventario, marca, modelo, numero_serie, sistema_operativo, version_firmware) VALUES
(1, 'Cisco', 'ISR4321', 'SN12345678', 'IOS-XE', '16.9.5'),
(2, 'HP', 'ProCurve 2620', 'SN87654321', 'ProVision', '15.18'),
(3, 'Ubiquiti', 'Unifi AP', 'SN11223344', 'UniFi OS', '6.5.55'),
(4, 'MikroTik', 'RB750Gr3', 'SN55667788', 'RouterOS', '7.1.2'),
(5, 'Cisco', 'Catalyst 2960', 'SN99887766', 'IOS', '15.2(2)E');

INSERT INTO Configuracion (id_inventario, descripcion, parametros_personalizados, ultima_actualizacion) VALUES
(1, 'Configuración estándar de enrutamiento', 'Rutas estáticas configuradas', '2024-02-01'),
(2, 'Switch con VLANs configuradas', 'VLAN 10, 20, 30', '2024-01-20'),
(3, 'Access Point con SSID empresarial', 'SSID: EmpresaWiFi, Seguridad: WPA2', '2023-12-15'),
(4, 'Router MikroTik con reglas de firewall', 'Bloqueo de tráfico externo no autorizado', '2024-01-30'),
(5, 'Switch con QoS habilitado', 'Prioridad para VoIP en VLAN 20', '2024-02-10');

INSERT INTO Incidentes (id_inventario, fecha_mantenimiento, tipo_mantenimiento, descripcion, realizado_por) VALUES
(3, '2024-02-05', 'Revisión', 'Access Point dejó de emitir señal', 'Juan López'),
(5, '2024-01-15', 'Cambio de firmware', 'Actualización de IOS en switch Catalyst', 'María González');

INSERT INTO Historial_cambios (id_inventario, fecha_cambio, cambio_realizado, realizado_por) VALUES
(1, '2024-01-28', 'Se agregó una nueva ruta estática', 'Carlos Pérez'),
(4, '2024-01-10', 'Se cambiaron las reglas de firewall', 'Ana Gómez');

INSERT INTO Enlaces (dispositivo_origen, dispositivo_destino, estado) VALUES
(1, 2, 'Activo'),  -- Router Cisco A1 ↔ Switch HP ProCurve
(2, 3, 'Activo'),  -- Switch HP ProCurve ↔ Access Point Ubiquiti
(3, 4, 'Inactivo'),  -- Access Point Ubiquiti ↔ Router MikroTik
(4, 5, 'Activo'),  -- Router MikroTik ↔ Switch Cisco Catalyst
(1, 5, 'Activo');  -- Router Cisco A1 ↔ Switch Cisco Catalyst







INSERT INTO Inventario (id_inventario, nombre, tipo_elemento, estado, fecha_adquisicion, id_ubicacion)
VALUES 
(1, 'Router Central', 'Router', 'Activo', '2023-05-12', 1),
(2, 'Switch Principal', 'Switch', 'Activo', '2023-06-18', 1),
(3, 'Servidor DHCP', 'Servidor', 'Activo', '2022-10-25', 2),
(4, 'Firewall Externo', 'Firewall', 'Activo', '2023-02-14', 1),
(5, 'Punto de Acceso 1', 'Access Point', 'Activo', '2023-07-09', 3),
(6, 'Punto de Acceso 2', 'Access Point', 'Activo', '2023-07-09', 4),
(7, 'Router Secundario', 'Router', 'Activo', '2022-11-30', 5),
(8, 'Switch de Backup', 'Switch', 'Activo', '2023-04-22', 6),
(9, 'Servidor de Logs', 'Servidor', 'Activo', '2022-12-05', 2),
(10, 'Cámara de Seguridad 1', 'Cámara IP', 'Activo', '2023-08-21', 7),
(11, 'Cámara de Seguridad 2', 'Cámara IP', 'Activo', '2023-08-21', 8),
(12, 'Servidor Web', 'Servidor', 'Activo', '2023-03-15', 2);


INSERT INTO Detalles_Tecnicos (id_detalle, id_inventario, marca, modelo, numero_serie, sistema_operativo, version_firmware)
VALUES 
(1, 1, 'Cisco', 'ISR4451', 'SN123456', 'IOS XE', '17.3.3'),
(2, 2, 'HP', 'Aruba 2930F', 'SN789012', 'ProVision', 'WC.16.10'),
(3, 3, 'Dell', 'PowerEdge R740', 'SN345678', 'Ubuntu Server', '20.04'),
(4, 4, 'Palo Alto', 'PA-220', 'SN901234', 'PAN-OS', '10.1.6'),
(5, 5, 'Ubiquiti', 'UAP-AC-Pro', 'SN567890', 'AirOS', '5.6.15'),
(6, 6, 'Ubiquiti', 'UAP-AC-LR', 'SN678901', 'AirOS', '5.6.15'),
(7, 7, 'MikroTik', 'CCR1009', 'SN890123', 'RouterOS', '7.1'),
(8, 8, 'Cisco', 'Catalyst 9200', 'SN456789', 'IOS XE', '17.6.4'),
(9, 9, 'HP', 'ProLiant DL380', 'SN567891', 'Windows Server', '2019'),
(10, 10, 'Hikvision', 'DS-2CD2143G0', 'SN678912', 'Embedded Linux', 'V5.5.82'),
(11, 11, 'Hikvision', 'DS-2CD2043G0', 'SN789123', 'Embedded Linux', 'V5.5.82'),
(12, 12, 'Lenovo', 'ThinkSystem SR650', 'SN890234', 'Ubuntu Server', '22.04');


INSERT INTO Configuracion (id_configuracion, id_inventario, descripcion, parametros_personalizados, ultima_actualizacion)
VALUES 
(1, 1, 'Configuración principal del Router Central', '{"ip": "192.168.1.1", "mascara": "255.255.255.0", "puerta_enlace": "192.168.1.254"}', '2024-02-15'),
(2, 2, 'Switch Principal', '{"ip": "192.168.1.2", "mascara": "255.255.255.0"}', '2024-02-15'),
(3, 3, 'Servidor DHCP', '{"ip": "192.168.1.3"}', '2024-02-15'),
(4, 4, 'Firewall Externo', '{"ip": "192.168.1.254"}', '2024-02-15'),
(5, 5, 'Punto de Acceso 1', '{"ip": "192.168.1.10"}', '2024-02-15'),
(6, 6, 'Punto de Acceso 2', '{"ip": "192.168.1.11"}', '2024-02-15'),
(7, 7, 'Router Secundario', '{"ip": "192.168.2.1"}', '2024-02-15'),
(8, 8, 'Switch de Backup', '{"ip": "192.168.2.2"}', '2024-02-15'),
(9, 9, 'Servidor de Logs', '{"ip": "192.168.1.4"}', '2024-02-15'),
(10, 10, 'Cámara de Seguridad 1', '{"ip": "192.168.1.20"}', '2024-02-15'),
(11, 11, 'Cámara de Seguridad 2', '{"ip": "192.168.1.21"}', '2024-02-15'),
(12, 12, 'Servidor Web', '{"ip": "192.168.1.5"}', '2024-02-15');


INSERT INTO Enlaces (id_enlace, dispositivo_origen, dispositivo_destino, estado)
VALUES
(1, 1, 2, 'Activo'),  -- Router Central a Switch Principal
(2, 2, 3, 'Activo'),  -- Switch Principal a Servidor DHCP
(12, 4, 1, 'Activo'); -- Firewall Externo a Router Central


INSERT INTO Rutas (nombre_ruta, descripcion) 
VALUES 
('Ruta A', 'Ruta de monitoreo principal'),
('Ruta B', 'Segunda ruta de monitoreo principal');

INSERT INTO Ruta_Dispositivos (id_ruta, id_inventario, orden) 
VALUES 
(1, 1, 1),
(1, 3, 2),
(1, 2, 3),
(1, 4, 4);
(2, 1, 1),
(2, 3, 2);


-- PRUEBASs
INSERT INTO Rutas (nombre_ruta, descripcion) 
VALUES 
('Ruta C', 'Una ruta mas');

INSERT INTO Ruta_Dispositivos (id_ruta, id_inventario, orden) 
VALUES
(4, 4, 1),
(4, 2, 3),
(4, 1, 2),
(4, 3, 4);


SET FOREIGN_KEY_CHECKS = 0;

ALTER TABLE Inventario AUTO_INCREMENT = 1;
ALTER TABLE Ubicacion AUTO_INCREMENT = 1;
ALTER TABLE Dependencia AUTO_INCREMENT = 1;
ALTER TABLE Ubicacion_Dependencia AUTO_INCREMENT = 1;
ALTER TABLE Detalles_Tecnicos AUTO_INCREMENT = 1;
ALTER TABLE Configuracion AUTO_INCREMENT = 1;
ALTER TABLE Incidentes AUTO_INCREMENT = 1;
ALTER TABLE Historial_Cambios AUTO_INCREMENT = 1;
ALTER TABLE Enlaces AUTO_INCREMENT = 1;

SET FOREIGN_KEY_CHECKS = 1;



SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE Enlaces;
TRUNCATE TABLE Configuracion;
TRUNCATE TABLE Detalles_Tecnicos;
TRUNCATE TABLE Historial_Cambios;
TRUNCATE TABLE Incidentes;
TRUNCATE TABLE Inventario;
TRUNCATE TABLE Ubicacion_Dependencia;
TRUNCATE TABLE Dependencia;
TRUNCATE TABLE Ubicacion;

SET FOREIGN_KEY_CHECKS = 1;






-- PRUEBAS REALES CON MIS DISPOSITIVOS

INSERT INTO Ubicacion (nombre_ubicacion, direccion, ciudad, pais) VALUES
('Oficina Principal', 'Av. Reforma 123', 'Ciudad de México', 'México'),
('Centro de Datos', 'Calle 10 #45', 'Guadalajara', 'México'),
('Sucursal Norte', 'Av. Insurgentes 234', 'Monterrey', 'México');

INSERT INTO Dependencia (nombre_dependencia, descripcion, contacto, telefono_contacto) VALUES
('Departamento de TI', 'Administración de la red y servidores', 'Carlos Pérez', '+52 55 1234 5678'),
('Infraestructura', 'Gestión de hardware y redes', 'Ana Gómez', '+52 33 8765 4321');

INSERT INTO Ubicacion_Dependencia (id_ubicacion, id_dependencia) VALUES
(1, 1),
(2, 1),
(3, 2);

INSERT INTO Inventario (nombre, tipo_elemento, estado, fecha_adquisicion, id_ubicacion, ip) VALUES
('Router Principal', 'Router', 'Activo', '2022-10-10', 1, '192.168.1.1');

INSERT INTO Detalles_Tecnicos (id_inventario, marca, modelo, numero_serie, sistema_operativo, version_firmware) VALUES
(1, 'TP-Link', 'Archer AX50', 'SN12345678', 'Firmware', '1.2.3');

INSERT INTO Historial_cambios (id_inventario, fecha_cambio, cambio_realizado, realizado_por) VALUES
(1, '2024-01-28', 'Actualización de firmware del router', 'Carlos Pérez');

INSERT INTO Configuracion (id_inventario, descripcion, parametros_personalizados, ultima_actualizacion) VALUES
(1, 'Configuración del router principal', 'SSID: MiWiFi, Seguridad: WPA2, DHCP: Habilitado', '2024-02-19');

INSERT INTO Enlaces (dispositivo_origen, dispositivo_destino, estado) VALUES
(1, 2, 'Activo');  -- Router Principal <-> Mi PC

--------------------------------------------------------------------------------------------------------------------------


INSERT INTO Inventario (nombre, tipo_elemento, estado, fecha_adquisicion, id_ubicacion, ip) VALUES
('Laptop', 'Computadora', 'Activo', '2022-10-10', 1, '192.168.1.61');

INSERT INTO Detalles_Tecnicos (id_inventario, marca, modelo, numero_serie, sistema_operativo, version_firmware) VALUES
(2, 'TP-Link', 'Archer AX50', 'SN12345678', 'Firmware', '1.2.3');

INSERT INTO Historial_cambios (id_inventario, fecha_cambio, cambio_realizado, realizado_por) VALUES
(2, '2024-01-28', 'Actualización de firmware del router', 'Carlos Pérez');

INSERT INTO Configuracion (id_inventario, descripcion, parametros_personalizados, ultima_actualizacion) VALUES
(2, 'Configuración del router principal', 'SSID: MiWiFi, Seguridad: WPA2, DHCP: Habilitado', '2024-02-19');

--------------------------------------------------------------------------------------------------------------------------

INSERT INTO Inventario (nombre, tipo_elemento, estado, fecha_adquisicion, id_ubicacion, ip) VALUES
('Pixel 6 pro', 'Smartphone', 'Activo', '2022-10-10', 1, '192.168.1.3');

INSERT INTO Detalles_Tecnicos (id_inventario, marca, modelo, numero_serie, sistema_operativo, version_firmware) VALUES
(3, 'Pixel', 'Archer AX50', 'SN12345678', 'Firmware', '1.2.3');

INSERT INTO Configuracion (id_inventario, descripcion, parametros_personalizados, ultima_actualizacion) VALUES
(3, 'Configuración del router principal', 'SSID: MiWiFi, Seguridad: WPA2, DHCP: Habilitado', '2024-02-19');

--------------------------------------------------------------------------------------------------------------------------

INSERT INTO Inventario (nombre, tipo_elemento, estado, fecha_adquisicion, id_ubicacion, ip) VALUES
('PC Pavilion Gaming 15', 'Computadora', 'Activo', '2022-10-10', 1, '192.168.1.5');

INSERT INTO Detalles_Tecnicos (id_inventario, marca, modelo, numero_serie, sistema_operativo, version_firmware) VALUES
(4, 'HP', 'Archer AX50', 'SN12345678', 'Firmware', '1.2.3');

INSERT INTO Configuracion (id_inventario, descripcion, parametros_personalizados, ultima_actualizacion) VALUES
(4, 'Configuración del router principal', 'SSID: MiWiFi, Seguridad: WPA2, DHCP: Habilitado', '2024-02-19');

INSERT INTO Enlaces (dispositivo_origen, dispositivo_destino, estado) VALUES
(1, 4, 'Activo');  -- Router Principal <-> Mi PC