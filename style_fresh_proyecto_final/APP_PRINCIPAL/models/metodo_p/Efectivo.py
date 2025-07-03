from django.db import models
from .Pago import Pago

class Efectivo(Pago):
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Efectivo {self.monto}"


