from django.conf import settings
from django.db import models

class HaircutRecommendation(models.Model):
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='recomendaciones'
    )
    frente = models.ImageField(upload_to='recomendaciones/frente/')
    lado_izq = models.ImageField(upload_to='recomendaciones/lado_izq/')
    lado_der = models.ImageField(upload_to='recomendaciones/lado_der/')
    atras = models.ImageField(upload_to='recomendaciones/atras/')
    recomendacion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recomendación de {self.cliente.username} - {self.fecha.strftime('%Y-%m-%d')}"
