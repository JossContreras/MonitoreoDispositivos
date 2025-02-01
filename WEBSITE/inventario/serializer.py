from rest_framework import serializers
from .models import Ubicacion

class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = '__all__'  # O puedes especificar los campos: ['id_ubicacion', 'nombre_ubicacion']

""""
class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = ['id', 'nombre_ubicacion', 'descripcion_ubicacion']
"""