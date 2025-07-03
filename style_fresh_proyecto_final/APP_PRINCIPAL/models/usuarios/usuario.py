from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que hereda de AbstractUser.
    """
    tipos = [
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
        ('barbero', 'Barbero'),
    ]
    tipo = models.CharField(max_length=10, choices=tipos)

    def __str__(self):
        return self.username