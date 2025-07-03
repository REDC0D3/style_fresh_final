# ADMINISTRADOR/views/create.py

from django.shortcuts import render, redirect
from django.contrib import messages
from urllib.parse import quote_plus # Importar para codificar parámetros URL

# --- TODAS LAS IMPORTACIONES DE MODELOS APUNTAN A APP_PRINCIPAL.MODELS ---
from APP_PRINCIPAL.models.usuarios.Administrador import Administrador 
from APP_PRINCIPAL.models.usuarios.Barbero import Barbero 
from APP_PRINCIPAL.models.usuarios.Cliente import Cliente 
from APP_PRINCIPAL.models.Productos import Producto 
from APP_PRINCIPAL.models.Servicio import Servicio
from APP_PRINCIPAL.models.usuarios.usuario import Usuario 

import re
from datetime import timedelta

def validar_password(password):
    """
    Valida que la contraseña tenga al menos:
    - 8 caracteres
    - Una mayúscula
    - Un número
    """
    if not password: return False
    if len(password) < 8: return False
    if not re.search(r'[A-Z]', password): return False
    if not re.search(r'\d', password): return False
    return True

def create_cliente(request):
    """
    Vista para crear un nuevo cliente desde el panel de administración (modal).
    Procesa el envío del formulario POST.
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        foto_perfil = request.FILES.get('foto_perfil')

        seccion_return = request.GET.get('seccion', 'clientes')
        # Parámetros para reabrir el modal de creación de cliente en caso de error
        # Importante: Usar quote_plus para codificar los valores de los campos
        modal_error_params = (
            f"&modal_create_type=cliente"
            f"&nombre={quote_plus(nombre or '')}&apellido={quote_plus(apellido or '')}"
            f"&telefono={quote_plus(telefono or '')}&username={quote_plus(username or '')}"
            f"&email={quote_plus(email or '')}"
        )

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso. Por favor, elige otro.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')
        elif Usuario.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está en uso. Por favor, usa otro.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')
        elif password != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')
        elif not validar_password(password):
            messages.error(request, "La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')
        else:
            try:
                cliente = Cliente(
                    nombre=nombre,
                    apellido=apellido,
                    telefono=telefono,
                    username=username,
                    email=email,
                    foto_perfil=foto_perfil # Acceder directamente a foto_perfil
                )
                cliente.set_password(password)
                cliente.save()
                messages.success(request, "Cliente registrado correctamente.")
                # Si es éxito, redirección simple con el tipo de éxito
                return redirect(f'/adminstrador/home/?seccion={seccion_return}&modal_success_type=cliente')
            except Exception as e:
                messages.error(request, f"Ocurrió un error inesperado al registrar el cliente: {e}")
                # En caso de excepción inesperada al guardar, también redirigir con params
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')
        
    return redirect('/adminstrador/home/') # Fallback si no es POST o si se llega aquí inesperadamente


def create_barbero(request):
    """
    Vista para crear un nuevo barbero desde el panel de administración (modal).
    Procesa el envío del formulario POST.
    """
    if request.method == 'POST':
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        username = request.POST.get("username")
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        fecha_nacimiento = request.POST.get("fecha_nacimiento")
        especialidad = request.POST.get("especialidad")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        
        from urllib.parse import quote_plus
        seccion_return = request.GET.get('seccion', 'barberos')
        modal_error_params = (
            f"&modal_create_type=barbero"
            f"&nombre={quote_plus(nombre or '')}&apellido={quote_plus(apellido or '')}"
            f"&username={quote_plus(username or '')}&telefono={quote_plus(telefono or '')}"
            f"&email={quote_plus(email or '')}&fecha_nacimiento={quote_plus(fecha_nacimiento or '')}"
            f"&especialidad={quote_plus(especialidad or '')}"
        )

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso. Por favor, elige otro.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')
        elif Usuario.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está en uso. Por favor, usa otro.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')
        elif password != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')
        elif not validar_password(password):
            messages.error(request, "La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')
        else:
            try:
                barbero = Barbero(
                    nombre=nombre,
                    apellido=apellido,
                    username=username,
                    telefono=telefono,
                    email=email,
                    fecha_nacimiento=fecha_nacimiento,
                    especialidad=especialidad,
                    foto_perfil=request.FILES.get('foto_perfil')
                )
                barbero.set_password(password)
                barbero.save()
                messages.success(request, "Barbero registrado correctamente.")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}&modal_success_type=barbero')
            except Exception as e:
                messages.error(request, f"Ocurrió un error inesperado al registrar el barbero: {e}")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')

    return redirect('/adminstrador/home/')

def create_administrador(request):
    """
    Vista para crear un nuevo administrador desde el panel de administración (modal).
    Procesa el envío del formulario POST.
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        from urllib.parse import quote_plus
        seccion_return = request.GET.get('seccion', 'admins')
        modal_error_params = (
            f"&modal_create_type=administrador"
            f"&nombre={quote_plus(nombre or '')}&apellido={quote_plus(apellido or '')}"
            f"&username={quote_plus(username or '')}&email={quote_plus(email or '')}"
        )

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')
        elif Usuario.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está en uso.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')
        elif password != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')
        elif not validar_password(password):
            messages.error(request, "La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')
        else:
            try:
                admin = Administrador(
                    nombre=nombre,
                    apellido=apellido,
                    username=username,
                    email=email,
                    foto_perfil=request.FILES.get('foto_perfil')
                )
                admin.set_password(password)
                admin.save()
                messages.success(request, "Administrador registrado correctamente.")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}&modal_success_type=administrador')
            except Exception as e:
                messages.error(request, f"Ocurrió un error inesperado al registrar el administrador: {e}")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')
        
    return redirect('/adminstrador/home/')

def create_producto(request):
    """
    Vista para crear un nuevo producto desde el panel de administración (modal).
    Procesa el envío del formulario POST.
    """
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        stock = request.POST.get("stock")
        precio = request.POST.get("precio")
        descripcion = request.POST.get("descripcion")
        tipo = request.POST.get("tipo")
        
        from urllib.parse import quote_plus
        seccion_return = request.GET.get('seccion', 'productos')
        modal_error_params = (
            f"&modal_create_type=producto"
            f"&nombre={quote_plus(nombre or '')}&stock={quote_plus(stock or '')}"
            f"&precio={quote_plus(precio or '')}&descripcion={quote_plus(descripcion or '')}"
            f"&tipo={quote_plus(tipo or '')}"
        )

        if not nombre or not stock or not precio or not descripcion or not tipo:
            messages.error(request, "Todos los campos del producto son obligatorios.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')
        else:
            try:
                producto = Producto(
                    nombre=nombre,
                    stock=stock,
                    precio=precio,
                    descripcion=descripcion,
                    tipo=tipo
                )
                if request.FILES.get("imagen"):
                    producto.imagen = request.FILES.get("imagen")
                producto.save()
                messages.success(request, "¡Producto registrado exitosamente!")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}&modal_success_type=producto')
            except Exception as e:
                messages.error(request, f"Ocurrió un error inesperado al registrar el producto: {e}")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')
        
    return redirect('/adminstrador/home/')


def create_servicio(request):
    """
    Vista para crear un nuevo servicio desde el panel de administración (modal).
    Procesa el envío del formulario POST.
    """
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        duracion = request.POST.get("duracion")
        precio = request.POST.get("precio")
        tipo = request.POST.get("tipo")
        
        from urllib.parse import quote_plus
        seccion_return = request.GET.get('seccion', 'servicios')
        modal_error_params = (
            f"&modal_create_type=servicio"
            f"&nombre={quote_plus(nombre or '')}&descripcion={quote_plus(descripcion or '')}"
            f"&duracion={quote_plus(duracion or '')}&precio={quote_plus(precio or '')}"
            f"&tipo={quote_plus(tipo or '')}"
        )

        if not (nombre and descripcion and duracion and precio and tipo):
            messages.error(request, "Todos los campos del servicio son obligatorios.")
            return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')
        else:
            try:
                minutos = int(duracion)
                duracion_td = timedelta(minutes=minutos)
            except (ValueError, TypeError):
                messages.error(request, "Duración inválida. Debes ingresar un número entero de minutos.")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')

            try:
                servicio = Servicio(
                    nombre=nombre,
                    descripcion=descripcion,
                    duracion=duracion_td,  
                    precio=precio,
                    tipo=tipo
                )
                if request.FILES.get("imagen"):
                    servicio.imagen = request.FILES.get("imagen")
                servicio.save()
                messages.success(request, "¡Servicio registrado exitosamente!")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}&modal_success_type=servicio')
            except Exception as e:
                messages.error(request, f"Ocurrió un error inesperado al registrar el servicio: {e}")
                return redirect(f'/adminstrador/home/?seccion={seccion_return}{modal_error_params}')
        
    return redirect('/adminstrador/home/')