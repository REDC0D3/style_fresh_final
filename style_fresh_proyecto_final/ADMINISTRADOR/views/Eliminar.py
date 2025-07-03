from django.shortcuts import get_object_or_404, redirect
from APP_PRINCIPAL.models.usuarios.Cliente import Cliente
from APP_PRINCIPAL.models.Productos import Producto
from APP_PRINCIPAL.models.usuarios.Administrador import Administrador
from APP_PRINCIPAL.models.usuarios.Barbero import Barbero
from APP_PRINCIPAL.models.Servicio import Servicio
from APP_PRINCIPAL.models.Calificacion import Calificacion # Importamos Calificacion

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == "POST":
        cliente.delete()
        return redirect('admin_home')
    return redirect('admin_home')

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":
        producto.delete()
        return redirect('admin_home')
    return redirect('admin_home')

def eliminar_administrador(request, administrador_id):
    administrador = get_object_or_404(Administrador, id=administrador_id)
    if request.method == "POST":
        administrador.delete()
        return redirect('admin_home')
    return redirect('admin_home')

def eliminar_barbero(request, barbero_id):
    barbero = get_object_or_404(Barbero, id=barbero_id)
    if request.method == "POST":
        barbero.delete()
        return redirect('admin_home')
    return redirect('admin_home')

def eliminar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    if request.method == "POST":
        servicio.delete()
        return redirect('admin_home')
    return redirect('admin_home')

def eliminar_calificacion(request, calificacion_id): # ¡Nueva vista!
    calificacion = get_object_or_404(Calificacion, id=calificacion_id)
    if request.method == "POST":
        calificacion.delete()
        return redirect('admin_home') # O a la sección de calificaciones si la creas
    return redirect('admin_home') # En caso de que no sea POST, redirige igualmente