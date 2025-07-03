from django.db import models

class Producto(models.Model):
    TIPOS = [
        ('merch', 'Merch'),
        ('comestible', 'Comestibles'),
        ('bebida', 'Bebidas'),
        ('belleza', 'Belleza'),
    ]
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"
