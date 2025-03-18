from rest_framework import generics
from .models import (
    Configuracion, Dependencia, DetallesTecnicos, 
    HistorialCambios, Incidentes, Inventario, Ubicacion
)
from .serializer import (
    ConfiguracionSerializer, DependenciaSerializer, DetallesTecnicosSerializer, 
    HistorialCambiosSerializer, IncidentesSerializer, InventarioSerializer, UbicacionSerializer
)

# Vistas para Configuración
class ConfiguracionListView(generics.ListCreateAPIView):
    queryset = Configuracion.objects.all()
    serializer_class = ConfiguracionSerializer

class ConfiguracionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Configuracion.objects.all()
    serializer_class = ConfiguracionSerializer

# Vistas para Dependencia
class DependenciaListView(generics.ListCreateAPIView):
    queryset = Dependencia.objects.all()
    serializer_class = DependenciaSerializer

class DependenciaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dependencia.objects.all()
    serializer_class = DependenciaSerializer

# Vistas para Detalles Técnicos
class DetallesTecnicosListView(generics.ListCreateAPIView):
    queryset = DetallesTecnicos.objects.all()
    serializer_class = DetallesTecnicosSerializer

class DetallesTecnicosDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetallesTecnicos.objects.all()
    serializer_class = DetallesTecnicosSerializer

# Vistas para Historial de Cambios
class HistorialCambiosListView(generics.ListCreateAPIView):
    queryset = HistorialCambios.objects.all()
    serializer_class = HistorialCambiosSerializer

class HistorialCambiosDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistorialCambios.objects.all()
    serializer_class = HistorialCambiosSerializer

# Vistas para Incidentes
class IncidentesListView(generics.ListCreateAPIView):
    queryset = Incidentes.objects.all()
    serializer_class = IncidentesSerializer

class IncidentesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Incidentes.objects.all()
    serializer_class = IncidentesSerializer

# Vistas para Inventario
class InventarioListView(generics.ListCreateAPIView):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer

class InventarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer

# Vistas para Ubicación
class UbicacionListView(generics.ListCreateAPIView):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer

class UbicacionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer
