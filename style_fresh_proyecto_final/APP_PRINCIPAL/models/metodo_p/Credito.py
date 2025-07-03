from django.db import models
from .Pago import Pago

class Credito(Pago):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    intereses = models.DecimalField(max_digits=5, decimal_places=2)
    cuotas = models.PositiveIntegerField()

    def __str__(self):
        return f"Crédito {self.monto} - {self.cuotas} cuotas - {self.intereses}%"
