from django.urls import path
from .views import analizar_ruta, inventario_por_ubicacion, verificar_estado_dispositivo

urlpatterns = [
    path('', analizar_ruta, name='analizar_ruta'),
    path('inventario/', inventario_por_ubicacion, name='inventario'),
    path('verificar_estado/', verificar_estado_dispositivo, name='verificar_estado'),
]
