# ADMINISTRADOR/views/update.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse 

# --- TODAS LAS IMPORTACIONES DE MODELOS APUNTAN A APP_PRINCIPAL.MODELS ---
from APP_PRINCIPAL.models.usuarios.Administrador import Administrador
from APP_PRINCIPAL.models.usuarios.Barbero import Barbero
from APP_PRINCIPAL.models.usuarios.Cliente import Cliente
from APP_PRINCIPAL.models.Productos import Producto
from APP_PRINCIPAL.models.Servicio import Servicio
from APP_PRINCIPAL.models.usuarios.usuario import Usuario 

import re
from datetime import timedelta

# Función de validación de contraseña (para reutilizar)
def validar_password(password):
    if not password: return False
    if len(password) < 8: return False
    if not re.search(r'[A-Z]', password): return False
    if not re.search(r'\d', password): return False
    return True


def actualizar_administrador(request, administrador_id):
    admin = get_object_or_404(Administrador, id=administrador_id)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'id': admin.id,
            'nombre': admin.nombre,
            'apellido': admin.apellido,
            'username': admin.username,
            'email': admin.email,
            'foto_perfil_url': admin.foto_perfil.url if admin.foto_perfil else '',
        }
        return JsonResponse(data)

    if request.method == 'POST':
        seccion_return = request.GET.get('seccion', 'admins')
        modal_param = f"&modal_update_type=administrador&item_id={admin.id}" # Añadir item_id para rellenar

        admin.nombre = request.POST.get('nombre')
        admin.apellido = request.POST.get('apellido')
        
        new_username = request.POST.get('username')
        if new_username != admin.username and Usuario.objects.filter(username=new_username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}') # Redirige con parámetros
        admin.username = new_username

        new_email = request.POST.get('email')
        if new_email != admin.email and Usuario.objects.filter(email=new_email).exists():
            messages.error(request, "El correo electrónico ya está en uso.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}') # Redirige con parámetros
        admin.email = new_email

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')

        if new_password or new_password2:
            if not (old_password and new_password and new_password2):
                messages.error(request, "Debes completar todos los campos de contraseña para cambiarla.")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}')
            if not admin.check_password(old_password):
                messages.error(request, "La contraseña actual es incorrecta.")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}')
            if new_password != new_password2:
                messages.error(request, "Las nuevas contraseñas no coinciden.")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}')
            if not validar_password(new_password):
                messages.error(request, "La nueva contraseña debe tener al menos 8 caracteres, una mayúscula y un número.")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}')
            admin.set_password(new_password)
        
        if request.FILES.get('foto_perfil'):
            admin.foto_perfil = request.FILES.get('foto_perfil')
        
        admin.save()
        messages.success(request, "Administrador actualizado correctamente.")
        return redirect(f'/adminstrador/home/?seccion={seccion_return}&modal_success_type=administrador')
    
    return redirect('/adminstrador/home/')


def actualizar_barbero(request, barbero_id):
    barbero = get_object_or_404(Barbero, id=barbero_id)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'id': barbero.id,
            'nombre': barbero.nombre,
            'apellido': barbero.apellido,
            'username': barbero.username,
            'telefono': barbero.telefono,
            'email': barbero.email,
            'fecha_nacimiento': barbero.fecha_nacimiento.isoformat() if barbero.fecha_nacimiento else '',
            'especialidad': barbero.especialidad,
            'foto_perfil_url': barbero.foto_perfil.url if barbero.foto_perfil else '',
        }
        return JsonResponse(data)

    if request.method == 'POST':
        seccion_return = request.GET.get('seccion', 'barberos')
        modal_param = f"&modal_update_type=barbero&item_id={barbero.id}"

        barbero.nombre = request.POST.get('nombre')
        barbero.apellido = request.POST.get('apellido')
        barbero.telefono = request.POST.get('telefono')
        
        new_username = request.POST.get('username')
        if new_username != barbero.username and Usuario.objects.filter(username=new_username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}')
        barbero.username = new_username

        new_email = request.POST.get('email')
        if new_email != barbero.email and Usuario.objects.filter(email=new_email).exists():
            messages.error(request, "El correo electrónico ya está en uso.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}')
        barbero.email = new_email

        barbero.especialidad = request.POST.get('especialidad')
        barbero.fecha_nacimiento = request.POST.get('fecha_nacimiento')

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')

        if new_password or new_password2:
            if not (old_password and new_password and new_password2):
                messages.error(request, "Debes completar todos los campos de contraseña para cambiarla.")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}')
            if not barbero.check_password(old_password):
                messages.error(request, "La contraseña actual es incorrecta.")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}')
            if new_password != new_password2:
                messages.error(request, "Las nuevas contraseñas no coinciden.")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}')
            if not validar_password(new_password):
                messages.error(request, "La nueva contraseña debe tener al menos 8 caracteres, una mayúscula y un número.")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}')
            barbero.set_password(new_password)

        if request.FILES.get('foto_perfil'):
            barbero.foto_perfil = request.FILES.get('foto_perfil')

        barbero.save()
        messages.success(request, "Barbero actualizado correctamente.")
        return redirect(f'/adminstrador/home/?seccion={seccion_return}&modal_success_type=barbero')
    
    return redirect('/adminstrador/home/')


def actualizar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'id': cliente.id,
            'nombre': cliente.nombre,
            'apellido': cliente.apellido,
            'username': cliente.username,
            'telefono': cliente.telefono,
            'email': cliente.email,
            'foto_perfil_url': cliente.foto_perfil.url if cliente.foto_perfil else '',
        }
        return JsonResponse(data)

    if request.method == 'POST':
        seccion_return = request.GET.get('seccion', 'clientes')
        modal_param = f"&modal_update_type=cliente&item_id={cliente.id}"

        cliente.nombre = request.POST.get('nombre')
        cliente.apellido = request.POST.get('apellido')
        cliente.telefono = request.POST.get('telefono')

        new_username = request.POST.get('username')
        if new_username != cliente.username and Usuario.objects.filter(username=new_username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}')
        cliente.username = new_username

        new_email = request.POST.get('email')
        if new_email != cliente.email and Usuario.objects.filter(email=new_email).exists():
            messages.error(request, "El correo electrónico ya está en uso.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}')
        cliente.email = new_email

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')

        if new_password or new_password2:
            if not (old_password and new_password and new_password2):
                messages.error(request, "Debes completar todos los campos de contraseña para cambiarla.")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}')
            if not cliente.check_password(old_password):
                messages.error(request, "La contraseña actual es incorrecta.")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}')
            if new_password != new_password2:
                messages.error(request, "Las nuevas contraseñas no coinciden.")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}')
            if not validar_password(new_password):
                messages.error(request, "La nueva contraseña debe tener al menos 8 caracteres, una mayúscula y un número.")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}')
            cliente.set_password(new_password)

        if request.FILES.get('foto_perfil'):
            cliente.foto_perfil = request.FILES.get('foto_perfil')
        
        cliente.save()
        messages.success(request, "Cliente actualizado correctamente.")
        return redirect(f'/adminstrador/home/?seccion={seccion_return}&modal_success_type=cliente')
    
    return redirect('/adminstrador/home/')


def actualizar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'id': producto.id,
            'nombre': producto.nombre,
            'stock': producto.stock,
            'precio': str(producto.precio),
            'descripcion': producto.descripcion,
            'tipo': producto.tipo,
            'imagen_url': producto.imagen.url if producto.imagen else '',
        }
        return JsonResponse(data)

    if request.method == "POST":
        seccion_return = request.GET.get('seccion', 'productos')
        modal_param = f"&modal_update_type=producto&item_id={producto.id}"

        producto.nombre = request.POST.get("nombre")
        producto.descripcion = request.POST.get("descripcion")
        producto.precio = request.POST.get("precio")
        producto.stock = request.POST.get("stock")
        producto.tipo = request.POST.get("tipo")
        if request.FILES.get("imagen"):
            producto.imagen = request.FILES.get("imagen")
        producto.save()
        messages.success(request, "Producto actualizado correctamente.")
        return redirect(f'/adminstrador/home/?seccion={seccion_return}&modal_success_type=producto')
    
    return redirect('/adminstrador/home/')


def actualizar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'id': servicio.id,
            'nombre': servicio.nombre,
            'descripcion': servicio.descripcion,
            'duracion': int(servicio.duracion.total_seconds() // 60),
            'precio': str(servicio.precio),
            'tipo': servicio.tipo,
            'imagen_url': servicio.imagen.url if servicio.imagen else '',
        }
        return JsonResponse(data)

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        duracion_str = request.POST.get("duracion")
        precio = request.POST.get("precio")
        tipo = request.POST.get("tipo")
        imagen = request.FILES.get("imagen")

        seccion_return = request.GET.get('seccion', 'servicios')
        modal_param = f"&modal_update_type=servicio&item_id={servicio.id}"

        if not (nombre and descripcion and duracion_str and precio and tipo):
            messages.error(request, "Todos los campos del servicio son obligatorios.")
        else:
            try:
                minutos = int(duracion_str)
                duracion_td = timedelta(minutes=minutos)
            except (ValueError, TypeError):
                messages.error(request, "Duración inválida. Debes ingresar un número entero de minutos.")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_param}')

            servicio.nombre = nombre
            servicio.descripcion = descripcion
            servicio.duracion = duracion_td
            servicio.precio = precio
            servicio.tipo = tipo
            if imagen:
                servicio.imagen = imagen
            servicio.save()
            messages.success(request, "Servicio actualizado correctamente.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}&modal_success_type=servicio')
    
    return redirect('/adminstrador/home/')