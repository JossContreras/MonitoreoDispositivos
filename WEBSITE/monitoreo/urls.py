from django.urls import path
from .views import analizar_ruta

urlpatterns = [
    path('', analizar_ruta, name='analizar_ruta'),
]
