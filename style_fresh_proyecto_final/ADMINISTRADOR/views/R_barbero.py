from django.shortcuts import render, redirect, get_object_or_404
from APP_PRINCIPAL.models.usuarios.Barbero import Barbero
from APP_PRINCIPAL.models.usuarios.usuario import Usuario  # O el modelo base de usuario

def registro_barbero(request):
    """
    Vista para registrar un nuevo barbero.
    - Si es GET, muestra el formulario de registro.
    - Si es POST, valida los datos y crea el barbero si todo es correcto.
    """
    mensaje = ""
    if request.method == "POST":
        # Obtiene los datos del formulario
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        username = request.POST.get("username")
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        fecha_nacimiento = request.POST.get("fecha_nacimiento")
        especialidad = request.POST.get("especialidad")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        
        # Validaciones
        if Usuario.objects.filter(username=username).exists():
            mensaje = "El nombre de usuario ya está en uso. Por favor, elige otro."
            return render(request, 'R_barbero.html', {"mensaje": mensaje})
        elif Usuario.objects.filter(email=email).exists():
            mensaje = "El correo electrónico ya está en uso. Por favor, usa otro."
            return render(request, 'R_barbero.html', {"mensaje": mensaje})
        elif password != password2:
            mensaje = "Las contraseñas no coinciden." 
        else:
            # Crea el nuevo barbero y guarda en la base de datos
            barbero = Barbero(
                nombre=nombre,
                apellido=apellido,
                username=username,
                telefono=telefono,
                email=email,
                fecha_nacimiento=fecha_nacimiento,
                especialidad=especialidad
            )
            barbero.set_password(password)  # Encripta la contraseña
            barbero.save()
            return redirect('admin_home')

    # Renderiza el formulario con el mensaje (si hay)
    return render(request, "R_barbero.html", {"mensaje": mensaje})

def actualizar_barbero(request, barbero_id):
    """
    Vista para actualizar los datos de un barbero existente.
    """
    barbero = get_object_or_404(Barbero, id=barbero_id)
    mensaje = ""
    if request.method == 'POST':
        barbero.nombre = request.POST.get('nombre')
        barbero.apellido = request.POST.get('apellido')
        barbero.telefono = request.POST.get('telefono')
        barbero.username = request.POST.get('username')
        barbero.email = request.POST.get('email')
        barbero.especialidad = request.POST.get('especialidad')
        barbero.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password or password2:
            if password != password2:
                mensaje = "Las contraseñas no coinciden"
                return render(request, 'R_barbero.html', {"barbero": barbero, "mensaje": mensaje})
            barbero.set_password(password)
        if request.FILES.get('foto_perfil'):
            barbero.foto_perfil = request.FILES.get('foto_perfil')
        barbero.save()
        return redirect('admin_home')
    return render(request, 'R_barbero.html', {"barbero": barbero})
