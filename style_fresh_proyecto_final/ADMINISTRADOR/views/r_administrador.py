from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from APP_PRINCIPAL.models.usuarios.Administrador import Administrador
import re

def validar_password(password):
    """
    Valida que la contraseña tenga al menos:
    - 8 caracteres
    - Una mayúscula
    - Un número
    """
    if not password:
        return False
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True



def registrar_administrador(request):
    """
    Vista para registrar un nuevo administrador.
    - Si es GET, muestra el formulario de registro.
    - Si es POST, valida los datos y crea el administrador si todo es correcto.
    """
    if request.method == 'POST':
        # Obtiene los datos del formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        foto_perfil = request.FILES.get('foto_perfil')

        # Validaciones
        if Administrador.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso")
        elif Administrador.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está en uso")
        elif password != password2:
            messages.error(request, "Las contraseñas no coinciden")
        elif not validar_password(password):
            messages.error(request, "La contraseña debe tener al menos 8 caracteres, una mayúscula y un número")
        else:
            # Crea el nuevo administrador y guarda en la base de datos
            admin = Administrador(
                nombre=nombre,
                apellido=apellido,
                username=username,
                email=email,
                foto_perfil=foto_perfil if foto_perfil else None
            )
            admin.set_password(password)  # Encripta la contraseña
            admin.save()
            messages.success(request, "Administrador registrado correctamente")
            return redirect('admin_home')
    return render(request, 'R_administrador.html')

def actualizar_administrador(request, administrador_id):
    admin = get_object_or_404(Administrador, id=administrador_id)
    if request.method == 'POST':
        admin.nombre = request.POST.get('nombre')
        admin.apellido = request.POST.get('apellido')
        admin.username = request.POST.get('username')
        admin.email = request.POST.get('email')
        # Manejo de cambio de contraseña
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')
        if old_password or new_password or new_password2:
            if not (old_password and new_password and new_password2):
                messages.error(request, "Debes completar todos los campos de contraseña.")
                return render(request, 'R_administrador.html', {"admin": admin})
            if not admin.check_password(old_password):
                messages.error(request, "La contraseña actual es incorrecta.")
                return render(request, 'R_administrador.html', {"admin": admin})
            if new_password != new_password2:
                messages.error(request, "Las nuevas contraseñas no coinciden.")
                return render(request, 'R_administrador.html', {"admin": admin})
            if not validar_password(new_password):
                messages.error(request, "La nueva contraseña debe tener al menos 8 caracteres, una mayúscula y un número")
                return render(request, 'R_administrador.html', {"admin": admin})
            admin.set_password(new_password)
        if request.FILES.get('foto_perfil'):
            admin.foto_perfil = request.FILES.get('foto_perfil')
        admin.save()
        messages.success(request, "Administrador actualizado correctamente")
        return redirect('admin_home')
    return render(request, 'R_administrador.html', {"admin": admin})