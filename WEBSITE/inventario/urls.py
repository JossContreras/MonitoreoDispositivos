from django.urls import path
from .views import (
    ConfiguracionListView, ConfiguracionDetailView,
    DependenciaListView, DependenciaDetailView,
    DetallesTecnicosListView, DetallesTecnicosDetailView,
    HistorialCambiosListView, HistorialCambiosDetailView,
    IncidentesListView, IncidentesDetailView,
    InventarioListView, InventarioDetailView,
    UbicacionListView, UbicacionDetailView
)

urlpatterns = [
    # Rutas Configuración
    path('configuracion/', ConfiguracionListView.as_view(), name='configuracion-list'),
    path('configuracion/<int:pk>/', ConfiguracionDetailView.as_view(), name='configuracion-detail'),

    # Rutas Dependencia
    path('dependencia/', DependenciaListView.as_view(), name='dependencia-list'),
    path('dependencia/<int:pk>/', DependenciaDetailView.as_view(), name='dependencia-detail'),

    # Rutas Detalles Técnicos
    path('detalles_tecnicos/', DetallesTecnicosListView.as_view(), name='detalles-tecnicos-list'),
    path('detalles_tecnicos/<int:pk>/', DetallesTecnicosDetailView.as_view(), name='detalles-tecnicos-detail'),

    # Rutas Historial de Cambios
    path('historial_cambios/', HistorialCambiosListView.as_view(), name='historial-cambios-list'),
    path('historial_cambios/<int:pk>/', HistorialCambiosDetailView.as_view(), name='historial-cambios-detail'),

    # Rutas Incidentes
    path('incidentes/', IncidentesListView.as_view(), name='incidentes-list'),
    path('incidentes/<int:pk>/', IncidentesDetailView.as_view(), name='incidentes-detail'),

    # Rutas Inventario
    path('inventario/', InventarioListView.as_view(), name='inventario-list'),
    path('inventario/<int:pk>/', InventarioDetailView.as_view(), name='inventario-detail'),

    # Rutas Ubicación
    path('ubicacion/', UbicacionListView.as_view(), name='ubicacion-list'),
    path('ubicacion/<int:pk>/', UbicacionDetailView.as_view(), name='ubicacion-detail'),
]
