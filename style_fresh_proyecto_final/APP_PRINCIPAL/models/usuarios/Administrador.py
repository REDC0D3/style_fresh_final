from django.db import models
from .Persona import Persona 

class Administrador(Persona):
    fecha_de_laburo = models.DateField(null=True, blank=True)
    hora_de_entrada = models.TimeField(null=True, blank=True)
    hora_de_salida = models.TimeField(null=True, blank=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    foto_perfil = models.ImageField(upload_to='clientes/perfiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def save(self, *args, **kwargs):
        self.tipo = 'admin'
        super().save(*args, **kwargs)
