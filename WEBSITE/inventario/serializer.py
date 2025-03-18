from rest_framework import serializers
from .models import (
    Configuracion, Dependencia, DetallesTecnicos, 
    HistorialCambios, Incidentes, Inventario, Ubicacion
)

# Serializer para Configuración
class ConfiguracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuracion
        fields = '__all__'

# Serializer para Dependencia
class DependenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependencia
        fields = '__all__'

# Serializer para Detalles Técnicos
class DetallesTecnicosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallesTecnicos
        fields = '__all__'

# Serializer para Historial de Cambios
class HistorialCambiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialCambios
        fields = '__all__'

# Serializer para Incidentes
class IncidentesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incidentes
        fields = '__all__'

# Serializer para Inventario
class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = '__all__'

# Serializer para Ubicación
class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = '__all__'
