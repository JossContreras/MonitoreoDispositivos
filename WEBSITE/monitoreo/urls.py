from django.urls import path
from .views import analizar_ruta, eliminar_ruta, inventario_por_ubicacion, mostrar_animacion, ping_ruta, verificar_estado_dispositivo, mostrar_grafica, monitoreo_red, agregar_ruta, lista_rutas

urlpatterns = [
    path('', monitoreo_red, name='analizar_ruta'),
    path("analizar_ruta/", analizar_ruta, name="analizar_ruta"),
    path('inventario/', inventario_por_ubicacion, name='inventario'),
    path('verificar_estado/', verificar_estado_dispositivo, name='verificar_estado'),

    path('add/', agregar_ruta, name='agregar_ruta'),



    path('ping_ruta/<int:id_ruta>/', ping_ruta, name='ping_ruta'),
    path('verificar_estado/<str:ip>/', verificar_estado_dispositivo, name='verificar_estado_dispositivo'),

    

    path('lista_rutas/', lista_rutas, name='lista_rutas'),
    path('agregar_ruta/', agregar_ruta, name='agregar_ruta'),

    path('eliminar_ruta/<int:id_ruta>/', eliminar_ruta, name='eliminar_ruta'),


    path('grafica/', mostrar_grafica, name='mostrar_grafica'),
    path('animacion/', mostrar_animacion, name='mostrar_animacion'),
]
