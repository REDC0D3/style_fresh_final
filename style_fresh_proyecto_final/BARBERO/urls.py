from django.urls import path
from .views.home_barberos import home_barbero
from .views.editar_perfil_barbero import editar_perfil_barbero  # 👈 NUEVO

urlpatterns = [
    path('home_berbero/', home_barbero, name='home_barbero'),
    path('editar-perfil-barbero/', editar_perfil_barbero, name='editar_perfil_barbero'),  # 👈 NUEVO
]
