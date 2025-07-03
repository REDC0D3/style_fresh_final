# ADMINISTRADOR/urls.py

from django.urls import path

# Importa home_admin desde el archivo 'home.py' dentro de ADMINISTRADOR/views/
from .views.home import home_admin

# Importa las vistas de creación desde el archivo 'create.py'
from .views import create

# Importa las vistas de actualización desde el archivo 'update.py' (en minúsculas)
from .views import update 

# Importa las vistas de configuración y horario
from .views.configuraciones import configurar_barberia
from .views.horarios import modificar_horario

# --- ¡CORREGIDO! Importa el módulo completo 'Eliminar' ---
from .views import Eliminar 

# editar perfil
from .views.editar_perfil_admin import editar_perfil_admin


urlpatterns = [
    # Ruta principal del panel de administración
    path('home/', home_admin, name='admin_home'),

    # Rutas para los modales de creación (apuntando a create.py)
    path('crear_cliente/', create.create_cliente, name='crear_cliente'),
    path('crear_barbero/', create.create_barbero, name='crear_barbero'),
    path('crear_administrador/', create.create_administrador, name='crear_administrador'),
    path('crear_producto/', create.create_producto, name='crear_producto'),
    path('crear_servicio/', create.create_servicio, name='crear_servicio'),

    # Rutas para actualizar (apuntando a update.py)
    path('actualizar_cliente/<int:cliente_id>/', update.actualizar_cliente, name='actualizar_cliente'),
    path('actualizar_barbero/<int:barbero_id>/', update.actualizar_barbero, name='actualizar_barbero'),
    path('actualizar_administrador/<int:administrador_id>/', update.actualizar_administrador, name='actualizar_administrador'),
    path('actualizar_producto/<int:producto_id>/', update.actualizar_producto, name='actualizar_producto'),
    path('actualizar_servicio/<int:servicio_id>/', update.actualizar_servicio, name='actualizar_servicio'),
    
    # --- ¡CORREGIDO! Rutas para eliminar, usando el prefijo del módulo 'Eliminar' ---
    path('eliminar_cliente/<int:cliente_id>/', Eliminar.eliminar_cliente, name='eliminar_cliente'),
    path('eliminar_producto/<int:producto_id>/', Eliminar.eliminar_producto, name='eliminar_producto'),
    path('eliminar_admin/<int:administrador_id>/', Eliminar.eliminar_administrador, name='eliminar_administrador'),
    path('eliminar_barbero/<int:barbero_id>/', Eliminar.eliminar_barbero, name='eliminar_barbero'),
    path('eliminar_servicio/<int:servicio_id>/', Eliminar.eliminar_servicio, name='eliminar_servicio'),

    # Rutas de configuración y horario
    path('configurar_barberia/', configurar_barberia, name='configurar_barberia'),
    path('modificar_horario/', modificar_horario, name='modificar_horario'),

    # editar perfil
    path("editar-perfil/", editar_perfil_admin, name="editar_perfil_admin"),
]