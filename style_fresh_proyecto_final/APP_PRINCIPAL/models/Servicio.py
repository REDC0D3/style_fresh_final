from django.db import models

class Servicio(models.Model):
    TIPOS = [
        ('vip', 'VIP'),
        ('normal', 'Normal'),
        ('otro', 'Otro'),
    ]
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='imagenes_servicios/', null=True, blank=True)
    duracion = models.DurationField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"
