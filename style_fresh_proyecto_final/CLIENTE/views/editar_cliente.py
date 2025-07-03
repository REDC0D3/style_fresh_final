from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist
from APP_PRINCIPAL.models.usuarios.Cliente import Cliente
from APP_PRINCIPAL.models.usuarios.usuario import Usuario
import re

def validar_password(password):
    if not password: return False
    if len(password) < 8: return False
    if not re.search(r'[A-Z]', password): return False
    if not re.search(r'\d', password): return False
    return True

@login_required
def editar_perfil_cliente(request):
    try:
        cliente = Cliente.objects.get(usuario_ptr_id=request.user.id)
    except ObjectDoesNotExist:
        messages.error(request, "Tu perfil de cliente no fue encontrado.")
        return redirect('home_cliente')

    if request.method == 'POST':
        # Mantén la lógica de validación actual
        cliente.nombre = request.POST.get('nombre')
        cliente.apellido = request.POST.get('apellido')
        cliente.telefono = request.POST.get('telefono')

        nuevo_username = request.POST.get('username')
        nuevo_email = request.POST.get('email')

        # Bandera para saber si hubo errores y si el modal debe abrirse
        has_errors = False

        if nuevo_username != cliente.username and Usuario.objects.filter(username=nuevo_username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            has_errors = True

        if nuevo_email != cliente.email and Usuario.objects.filter(email=nuevo_email).exists():
            messages.error(request, "El correo electrónico ya está en uso.")
            has_errors = True
        
        # Si no hay errores de username/email, actualiza. Si no, mantiene los originales
        if not has_errors:
            cliente.username = nuevo_username
            cliente.email = nuevo_email
        else: # Si hay errores de username/email, no actualizamos estos campos en el objeto cliente para que se muestren los valores originales en el formulario.
              # Aunque los nuevos valores estarán en request.POST. Los mostraremos después.
            pass


        if request.FILES.get('foto_perfil'):
            cliente.foto_perfil = request.FILES.get('foto_perfil')

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')

        password_changed = False
        if new_password or new_password2 or old_password: # Si alguno de los campos de contraseña fue tocado
            password_changed = True
            if not (old_password and new_password and new_password2):
                messages.error(request, "Para cambiar la contraseña, completa los tres campos de contraseña.")
                has_errors = True
            elif not cliente.check_password(old_password):
                messages.error(request, "La contraseña actual es incorrecta.")
                has_errors = True
            elif new_password != new_password2:
                messages.error(request, "Las nuevas contraseñas no coinciden.")
                has_errors = True
            elif not validar_password(new_password):
                messages.error(request, "La nueva contraseña debe tener al menos 8 caracteres, una mayúscula y un número.")
                has_errors = True
            else:
                cliente.set_password(new_password)
                cliente.save() # Guardar el cliente con la nueva contraseña
                update_session_auth_hash(request, cliente) # Mantener la sesión activa
                messages.success(request, "Contraseña actualizada correctamente.")
                # Si solo se cambia la contraseña, redirigimos a login como antes
                # Si hay otros cambios, se manejará al final
                return redirect('login') # Redirigir a login si solo se cambió la contraseña


        # Si no hubo errores en las validaciones, guarda el resto de los datos
        if not has_errors and not password_changed: # Solo guarda si no hay errores y no se intentó cambiar la contraseña o ya se manejó
            cliente.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('home_cliente')
        
        # Si hubo errores, renderiza la plantilla con los errores
        # Usamos request.POST para pre-llenar los campos con los valores que el usuario intentó enviar
        context = {
            'cliente': cliente, # Se mantiene el objeto cliente original para la foto, etc.
            'form_data': request.POST, # Esto contendrá los datos que el usuario envió
            'show_modal': has_errors # Para indicarle al JS que abra el modal
        }
        return render(request, 'home_cliente.html', context)


    # Si es GET request, solo renderiza
    return render(request, 'home_cliente.html', {'cliente': cliente})