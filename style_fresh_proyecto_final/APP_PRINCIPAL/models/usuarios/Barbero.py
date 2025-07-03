from django.db import models
from .Persona import Persona  # Asegúrate de que Persona esté bien importada

class Barbero(Persona):
    especialidad = models.TextField(null=True, blank=True)
    fecha_de_laburo = models.DateField(null=True, blank=True)
    hora_de_entrada = models.TimeField(null=True, blank=True)
    hora_de_salida = models.TimeField(null=True, blank=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    fecha_de_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    redes_sociales = models.TextField(null=True, blank=True)
    foto_perfil = models.ImageField(upload_to='clientes/perfiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.especialidad or 'Sin especialidad'}"

    def save(self, *args, **kwargs):
        self.tipo = 'barbero'  # Asegura que se guarde como tipo barbero
        super().save(*args, **kwargs)

@property
def foto_url(self):
    if self.foto_perfil:
        return self.foto_perfil.url
    return ''
