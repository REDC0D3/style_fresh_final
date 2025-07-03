from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from APP_PRINCIPAL.models.calendario.Evento import Evento
from APP_PRINCIPAL.models.usuarios.Cliente import Cliente

class Calificacion(models.Model):
    evento = models.OneToOneField(Evento, on_delete=models.CASCADE, related_name='calificacion', null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='calificaciones', null=True, blank=True)
    puntuacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    comentario = models.TextField(blank=True, null=True)
    creado_fecha_hora = models.DateTimeField(auto_now_add=True)
    no_molestar = models.BooleanField(default=False)  # Para el botón "No molestar"

    def __str__(self):
        return f"Puntuación: {self.puntuacion} - {self.comentario[:30]}..."


