from django.db import models
from APP_PRINCIPAL.models.Productos import Producto

class DetalleFactura(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto} x {self.cantidad} - Subtotal: {self.subtotal}"
