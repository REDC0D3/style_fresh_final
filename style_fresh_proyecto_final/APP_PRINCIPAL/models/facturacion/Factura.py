from django.db import models
from APP_PRINCIPAL.models.Servicio import Servicio
from APP_PRINCIPAL.models.facturacion.Detalles_factura import DetalleFactura
from APP_PRINCIPAL.models.metodo_p.Credito import Credito
from APP_PRINCIPAL.models.metodo_p.Transferencia import Transferencia
from APP_PRINCIPAL.models.metodo_p.Efectivo import Efectivo

class Factura(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    detalle = models.ForeignKey(DetalleFactura, on_delete=models.CASCADE)
    credito = models.ForeignKey(Credito, on_delete=models.SET_NULL, null=True, blank=True)
    transferencia = models.ForeignKey(Transferencia, on_delete=models.SET_NULL, null=True, blank=True)
    efectivo = models.ForeignKey(Efectivo, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Factura {self.id} - Total: {self.total}"
