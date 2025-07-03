from django.db import models
from .usuario import Usuario

class Persona(Usuario):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    imagen = models.ImageField(upload_to='imagenes_personas/', null=True, blank=True)

    

    def __str__(self):
        return f"{self.nombre} {self.apellido}"