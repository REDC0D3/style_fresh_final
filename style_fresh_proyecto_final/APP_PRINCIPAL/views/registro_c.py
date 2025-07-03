from django.shortcuts import render, redirect, get_object_or_404
from APP_PRINCIPAL.models.usuarios.Cliente import Cliente
import re

def validar_password(password):
    # Al menos 8 caracteres, una mayúscula y un número
    if not password:
        return False
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True

def registrar_cliente(request):
    mensaje = ""
    admin_registra = request.GET.get('admin', False) or request.POST.get('admin_registra', False)
    
    # Initialize form_data with empty strings for initial render or if no POST data
    form_data = {
        'nombre': '',
        'apellido': '',
        'telefono': '',
        'username': '',
        'email': '',
    }

    if request.method == 'POST':
        # Populate form_data with POST data
        form_data = {
            'nombre': request.POST.get('nombre', ''),
            'apellido': request.POST.get('apellido', ''),
            'telefono': request.POST.get('telefono', ''),
            'username': request.POST.get('username', ''),
            'email': request.POST.get('email', ''),
        }

        nombre = form_data['nombre']
        apellido = form_data['apellido']
        telefono = form_data['telefono']
        username = form_data['username']
        email = form_data['email']
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        foto_perfil = request.FILES.get('foto_perfil')

        # Validaciones
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            mensaje = "El correo electrónico no es válido"
        elif not validar_password(password):
            mensaje = "La contraseña debe tener al menos 8 caracteres, una mayúscula y un número"
        elif Cliente.objects.filter(username=username).exists():
            mensaje = "El nombre de usuario ya está en uso"
        elif Cliente.objects.filter(email=email).exists():
            mensaje = "El correo electrónico ya está en uso"
        elif password != password2:
            mensaje = "Las contraseñas no coinciden"
        else:
            cliente = Cliente(
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                username=username,
                email=email,
                foto_perfil=foto_perfil if foto_perfil else None
            )
            cliente.set_password(password)
            cliente.password_visible = password  # Solo para pruebas
            cliente.save()
            if admin_registra:
                return redirect('admin_home')
            else:
                return redirect('login')  # O la página que desees para usuarios normales
                
    # Pass both the message and form data to the template
    return render(request, 'registro_cliente.html', {"mensaje": mensaje, "admin_registra": admin_registra, "form_data": form_data})

def actualizar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    mensaje = ""
    # Initialize form_data with existing client data for initial render
    form_data = {
        'nombre': cliente.nombre,
        'apellido': cliente.apellido,
        'telefono': cliente.telefono,
        'username': cliente.username,
        'email': cliente.email,
    }

    if request.method == 'POST':
        # Update form_data with POST data
        form_data = {
            'nombre': request.POST.get('nombre', cliente.nombre),
            'apellido': request.POST.get('apellido', cliente.apellido),
            'telefono': request.POST.get('telefono', cliente.telefono),
            'username': request.POST.get('username', cliente.username),
            'email': request.POST.get('email', cliente.email),
        }

        cliente.nombre = form_data['nombre']
        cliente.apellido = form_data['apellido']
        cliente.telefono = form_data['telefono']
        # Check if the username being submitted is different from the current one and if it already exists
        if cliente.username != form_data['username'] and Cliente.objects.filter(username=form_data['username']).exclude(id=cliente.id).exists():
            mensaje = "El nombre de usuario ya está en uso por otro cliente."
            return render(request, 'registro_cliente.html', {"cliente": cliente, "mensaje": mensaje, "form_data": form_data})
        cliente.username = form_data['username']
        
        # Check if the email being submitted is different from the current one and if it already exists
        if cliente.email != form_data['email'] and Cliente.objects.filter(email=form_data['email']).exclude(id=cliente.id).exists():
            mensaje = "El correo electrónico ya está en uso por otro cliente."
            return render(request, 'registro_cliente.html', {"cliente": cliente, "mensaje": mensaje, "form_data": form_data})
        cliente.email = form_data['email']


        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password or password2:
            if password != password2:
                mensaje = "Las contraseñas no coinciden"
                return render(request, 'registro_cliente.html', {"cliente": cliente, "mensaje": mensaje, "form_data": form_data})
            if not validar_password(password):
                mensaje = "La contraseña debe tener al menos 8 caracteres, una mayúscula y un número"
                return render(request, 'registro_cliente.html', {"cliente": cliente, "mensaje": mensaje, "form_data": form_data})
            cliente.set_password(password)
            cliente.password_visible = password  # Solo para pruebas
        if request.FILES.get('foto_perfil'):
            cliente.foto_perfil = request.FILES.get('foto_perfil')
        cliente.save()
        return redirect('admin_home')
    # Pass existing client data (or updated form_data if there were errors) to the template
    return render(request, 'registro_cliente.html', {"cliente": cliente, "form_data": form_data})


def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == "POST":
        cliente.delete()
        return redirect('admin_home')
    return redirect('admin_home')