from django.db import models

class Horario(models.Model):
    dia = models.CharField(max_length=20)
    apertura = models.TimeField()
    cierre = models.TimeField()

    def __str__(self):
        return f"{self.dia}: {self.apertura} - {self.cierre}"