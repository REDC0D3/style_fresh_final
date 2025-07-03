from django.urls import path
from APP_PRINCIPAL.views.login import login_1
from APP_PRINCIPAL.views.P_principal import pagina_principal
from APP_PRINCIPAL.views.registro_c import registrar_cliente
from APP_PRINCIPAL.views.productos_cliente import productos_cliente
from APP_PRINCIPAL.views.servicios_cliente import servicios_cliente
from APP_PRINCIPAL.views.horario_barberia import horario_barberia
from APP_PRINCIPAL.views.sobre_nosotros import sobre_nosotros



urlpatterns = [
    # Página principal del sistema
    path('', pagina_principal, name='pagina_principal'),
    # Registro de administrador
    path('registrarse/', registrar_cliente, name='registrarse'),
    # Login de usuario
    path('login/', login_1, name='login'),
    # Productos para el cliente
    path('productos/', productos_cliente, name='productos_clientes'),
    # Servicios para el cliente
    path('servicios/', servicios_cliente, name='servicios_cliente'),
    path('horario/', horario_barberia, name='horario'),
    path('sobre-nosotros/', sobre_nosotros, name='sobre_nosotros'),

]

