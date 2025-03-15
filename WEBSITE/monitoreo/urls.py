from django.urls import path
from .views import agregar_ruta_definida, analizar_ruta, editar_ruta, eliminar_dispositivo_ruta_definida, eliminar_ruta, formulario_agregar_ruta_definida, inventario_por_ubicacion, mostrar_animacion, ping_ruta, verificar_estado_dispositivo, mostrar_grafica, monitoreo_red, agregar_ruta, lista_rutas

urlpatterns = [
    path('', monitoreo_red, name='analizar_ruta'),
    path("analizar_ruta/", analizar_ruta, name="analizar_ruta"),
    path('inventario/', inventario_por_ubicacion, name='inventario'),
    path('verificar_estado/', verificar_estado_dispositivo, name='verificar_estado'),

    path("ruta/agregar/", agregar_ruta_definida, name="agregar_ruta"),
    path('ruta/agregar/ruta_definida', formulario_agregar_ruta_definida, name='formulario_agregar_ruta'),
    path('editar_ruta/<int:id_ruta>/', editar_ruta, name='editar_ruta'),

    path('ruta/<int:id_ruta>/eliminar-dispositivo/<int:id_dispositivo>/', eliminar_dispositivo_ruta_definida, name='eliminar_dispositivo_ruta_definida'),



    path('ping_ruta/<int:id_ruta>/', ping_ruta, name='ping_ruta'),
    path('verificar_estado/<str:ip>/', verificar_estado_dispositivo, name='verificar_estado_dispositivo'),

    

    path('lista_rutas/', lista_rutas, name='lista_rutas'),
    path('agregar_ruta/', agregar_ruta, name='agregar_ruta'),

    path('eliminar_ruta/<int:id_ruta>/', eliminar_ruta, name='eliminar_ruta'),


    path('grafica/', mostrar_grafica, name='mostrar_grafica'),
    path('animacion/', mostrar_animacion, name='mostrar_animacion'),
]
