# APP_PRINCIPAL/models/calendario/Evento.py
from django.db import models
from APP_PRINCIPAL.models.usuarios import Persona
from APP_PRINCIPAL.models.usuarios import Barbero

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    # Cambia el related_name para persona
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True, blank=True, related_name='eventos_como_cliente')
    # Cambia el related_name para barbero
    barbero = models.ForeignKey(Barbero, on_delete=models.SET_NULL, null=True, blank=True, related_name='eventos_como_barbero')

    def __str__(self):
        return self.titulo