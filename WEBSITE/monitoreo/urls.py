from django.urls import path
from .views import analizar_ruta, inventario_por_ubicacion, mostrar_animacion, verificar_estado_dispositivo, mostrar_grafica, monitoreo_red

urlpatterns = [
    path('', monitoreo_red, name='analizar_ruta'),
    path("analizar_ruta/", analizar_ruta, name="analizar_ruta"),
    path('inventario/', inventario_por_ubicacion, name='inventario'),
    path('verificar_estado/', verificar_estado_dispositivo, name='verificar_estado'),
    path('grafica/', mostrar_grafica, name='mostrar_grafica'),
    path('animacion/', mostrar_animacion, name='mostrar_animacion'),
]
