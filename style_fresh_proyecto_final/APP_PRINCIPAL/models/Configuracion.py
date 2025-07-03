from django.db import models

class Configuracion_barberia(models.Model):
    horario = models.CharField(max_length=100, default='Lunes a Viernes: 9:00 - 18:00')
    telefono = models.CharField(max_length=15, default='123-456-7890')
    ubicacion = models.CharField(max_length=255, default='Calle Falsa 123, Ciudad')
    email = models.EmailField(max_length=254)
    redes_sociales = models.CharField(max_length=255, default='https://facebook.com/barberia')
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    
    
    def __str__(self):
        return f"Configuración de Barbería: {self.ubicacion} - {self.telefono}"
    
