from django.urls import path
from . import views

urlpatterns = [
    #Pagina de inicio
    path('', views.index, name='principal'),
    #paginas generales
    path('inicio', views.inicio, name='inicio'),
    #Formularios
    path('crear_dispositivo', views.crear_dispositivo, name='crear_dispositivo'),
    path('cambiar_dispositivo', views.cambiar_dispositivo, name='cambiar_dispositivo'),
    path('editar_dispositivo', views.editar_dispositivo, name='editar_dispositivo'),
    path('eliminar_dispositivo', views.eliminar_dispositivo, name='eliminar_dispositivo'),
    path('incidente_dispositivo', views.incidentes, name='incidentes_dispositivo'),
    #inicio de sesion
    path('login', views.iniciar_cuenta, name='login'),
    path('registrar', views.registrar_cuenta, name='registrar'),
]
