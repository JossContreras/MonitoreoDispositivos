from django.db import router
from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from .views import UbicacionViewSet, eliminar_inventario_api

router = DefaultRouter()
router.register(r'ubicaciones', UbicacionViewSet)

urlpatterns = [
    #Pagina de inicio
    path('', views.index, name='principal'),
    path('inicioo', views.pagprin, name='inicio'),
    #paginas generales
    #Formularios ABRIR DE MANERA VISUAL SIN CARGAR DATOS
    path('crear_dispositivo', views.crear_dispositivo, name='crear_dispositivo'),
    path('cambiar_dispositivo', views.cambiar_dispositivo, name='cambiar_dispositivo'),
    path('editar_dispositivo', views.editar_dispositivo, name='editar_dispositivo'),
    path('eliminar_dispositivo', views.eliminar_dispositivo, name='eliminar_dispositivo'),
    path('incidente_dispositivo', views.incidentes, name='incidentes_dispositivo'),
    #inicio de sesion
    path('login', views.iniciar_cuenta, name='login'),
    path('registrar', views.registrar_cuenta, name='registrar'),

    #=========================================================================================

    # Vista Eliminar dispositvos
    path("dispositivo/eliminar", views.eliminar_inventario, name="eliminar_inventario"),
    # Eliminar dispositivos API
    path("api/eliminar_inventario/<int:id_inventario>/", eliminar_inventario_api, name="eliminar_inventario_api"),

    # Actualizar dispositivos API
    path("api/actualizar_dispositivo/<int:id_inventario>/", views.actualizar_dispositivo, name="actualizar_dispositivo"),

    path("dispositivos/editar/<int:id_inventario>/", views.actualizar_dispositivo, name="editar_dispositivo"),

    path('dispositivos/incidentes/', views.agregar_incidente, name='agregar_incidente'),
    path("dispositivos/incidentes/formulario/", views.formulario_incidente, name="formulario_incidente"),

     #=========================================================================================
    path('api/', include(router.urls)),

    path('ubicaciones/vista/', views.ubicaciones_view, name='ubicaciones_list'),
    path('ubicaciones/nueva/', views.ubicacion_create, name='ubicacion_create'),

    path('dispositivo/crear', views.insertar_dispositivo, name='crear_dispositivo'),
    path('eliminar_inventario/<int:id_inventario>/', views.eliminar_inventario_api, name='eliminar_inventario'),
    path("insertar_dispositivo/", views.insertar_dispositivo, name="insertar_dispositivo"),
]
