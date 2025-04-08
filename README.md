Pasos para instalar el sistema:
Descargar archivos y abrirlo en el editor de texto (VS)

Requisitos Generales: Mysql (U otra base que maneje sql)
Una vez descargado e instalado procedemos a abrirlo y crearemos una base de datos, una vez creada vamos a buscar
el codigo SQL en los archivos del proyecto
- WEBSITE/inventario/bd.sql

Copiamos el codigo y lo ejecutamos en sql (No te preocupes, esta hecho para ejecutarse junto)
Nota: No olvides el nombre de tu base de datos, usuario (Si no asignaste uno es "ROOT"), contraseña (En caso de tener una).



Instalar Inventario


Requisitos instalados: Node.js 


Una vez estando en la carpeta general, existe una carpeta llamanda client, en esa entraremos mediante terminal
- cd client ( Nuestra ruta sera WEBSITE\client> )
  
Ya entrando a esta lo demas es sencilo, un comando para instalar todas las dependencias
- npm install
  
Se instalaran todas las herramientas que se usaron o descargaron, y de la siguiente manera se ejecuta
- npm run dev
  
Esto va a generar un localhost el cual permitira navegar entre el sistema de inventario el cual es un CRUD


Instalar Monitoreo

Requisitos Instalados: Python, PIP (Este se instala al instalar Node.js), Django.

Nos colocaremos en la raiz inicial del poryecto ( WEBSITE ), en esta se encuentran otra carpetas
- client
  
- inventario
  
- monitoreo
  
- WEBSITE (si, otra vez)
  

Primero abriremos la terminal, y colocaremos el siguiente comando que nos ayudara a instalara las dependencias
- pip install -r requirements.txt (Esto puede llevar un rato dependiendo la velocidad de tu internet)
  
Ahora, en caso de modificaciones migraremos las tablas para verificar que estan creadas en la bd
- python manage.py migrate
  
Ahora para finalizar es necesario conectar correctamente el proyecto con la base de datos que creamos, en los siguientes
archivos se encuentran las funciones para conectarla (hazlo desde un editor de codigo)
- WEBSITE/WEBSITE/setting.py (Line 91)
  
- WEBSITE/monitoreo/ping_dispositivos.py (Line 9)
  
- WEBSITE/monitoreo/views.py (Line 14)
  

Una vez conectado la base de datos asigandole sus parametros debidos, ya solo queda ejecutarlo
- python manage.py runserver
  
Igual va a generar un localhost donde se podra ver las interfaces en un navegador.
