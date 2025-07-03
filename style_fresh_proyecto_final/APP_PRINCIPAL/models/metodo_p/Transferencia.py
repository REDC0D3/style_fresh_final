from django.db import models
from .Pago import Pago

class Transferencia(Pago):
    banco = models.CharField(max_length=100)
    numero_cuenta = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Transferencia {self.banco} - {self.numero_cuenta} - {self.monto}"
