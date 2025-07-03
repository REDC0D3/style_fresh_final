from django.contrib import admin
from .models.Servicio import Servicio
from .models.Productos import Producto
from .models.facturacion.Detalles_factura import DetalleFactura
from .models.facturacion.Factura import Factura
from .models.metodo_p.Credito import Credito
from .models.metodo_p.Efectivo import Efectivo
from .models.metodo_p.Transferencia import Transferencia
from .models.metodo_p.Pago import Pago
from .models.usuarios.Barbero import Barbero
from .models.usuarios.Administrador import Administrador
from .models.usuarios.usuario import Usuario
from .models.usuarios.Persona import Persona
from .models.usuarios.Cliente import Cliente
from .models.Configuracion import Configuracion_barberia
from .models.calendario.Evento import Evento
from .models.diseño_corte import HaircutRecommendation
 
# Registrar modelos en el admin
admin.site.register(Servicio)
admin.site.register(Producto)
admin.site.register(DetalleFactura)
admin.site.register(Factura)
admin.site.register(Credito)
admin.site.register(Efectivo)
admin.site.register(Transferencia)
admin.site.register(Pago)
admin.site.register(Barbero)
admin.site.register(Administrador)
admin.site.register(Usuario)
admin.site.register(Persona)
admin.site.register(Cliente)
admin.site.register(Configuracion_barberia)
admin.site.register(Evento)
admin.site.register(HaircutRecommendation)
