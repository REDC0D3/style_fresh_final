from django.db import models
from .Servicio import Servicio
from .Calificacion import Calificacion
from .usuarios.Barbero import Barbero
from .usuarios.Cliente import Cliente

class Agenda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    barbero = models.ForeignKey(Barbero, on_delete=models.CASCADE)
    calificacion = models.ForeignKey(Calificacion, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)    
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_final = models.TimeField()
    
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f"{self.fecha} | {self.hora_inicio} - {self.hora_final} | Estado: {self.estado}"

