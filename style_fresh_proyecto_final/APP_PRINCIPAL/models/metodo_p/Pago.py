from django.db import models

class Pago(models.Model):
    TIPO_PAGO_CHOICES = [
        ('credito', 'Crédito'),
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
    ]
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('cancelado', 'Cancelado'),
    ]

    tipo_pago = models.CharField(max_length=20, choices=TIPO_PAGO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)

    def __str__(self):
        return f"{self.get_tipo_pago_display()} - {self.get_estado_display()}"
