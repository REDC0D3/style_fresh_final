from django.db import models
from .Persona import Persona

class Cliente(Persona):
    direccion = models.CharField(max_length=255, null=True, blank=True)
    foto_perfil = models.ImageField(upload_to='clientes/perfiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.direccion}"
    
    def save(self, *args, **kwargs):
        self.tipo = 'cliente'
        super().save(*args, **kwargs)

