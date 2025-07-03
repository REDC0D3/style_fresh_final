from django.shortcuts import render, redirect, get_object_or_404
from APP_PRINCIPAL.models.Servicio import Servicio
from datetime import timedelta

def registrar_servicio(request):
    """
    Vista para registrar un nuevo servicio.
    - Si es GET, muestra el formulario de registro.
    - Si es POST, valida los datos y crea el servicio si todo es correcto.
    """
    mensaje = ""
    if request.method == "POST":
        # Obtiene los datos del formulario
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        duracion = request.POST.get("duracion")
        precio = request.POST.get("precio")
        tipo = request.POST.get("tipo")
        imagen = request.FILES.get("imagen")

        # Validación de campos obligatorios
        if not (nombre and descripcion and duracion and precio and tipo):
            mensaje = "Todos los campos son obligatorios."
        else:
            try:
                minutos = int(duracion)
                duracion_td = timedelta(minutes=minutos)
            except (ValueError, TypeError):
                mensaje = "Duración inválida. Debes ingresar un número entero de minutos."
                return render(request, "R_servicio.html", {"mensaje": mensaje})
            # Crea el nuevo servicio y guarda en la base de datos
            servicio = Servicio(
                nombre=nombre,
                descripcion=descripcion,
                duracion=duracion_td,  
                precio=precio,
                tipo=tipo
            )
            # Si se subió una imagen, la asigna
            if hasattr(servicio, 'imagen') and imagen:
                servicio.imagen = imagen
            servicio.save()
            mensaje = "¡Servicio registrado exitosamente!"
            return redirect('admin_home') 
            # Renderiza el formulario con el mensaje (si hay)
    return render(request, "R_servicio.html", {"mensaje": mensaje})

def actualizar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    mensaje = ""
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        duracion = request.POST.get("duracion")
        precio = request.POST.get("precio")
        tipo = request.POST.get("tipo")
        imagen = request.FILES.get("imagen")

        if not (nombre and descripcion and duracion and precio and tipo):
            mensaje = "Todos los campos son obligatorios."
        else:
            try:
                minutos = int(duracion)
                duracion_td = timedelta(minutes=minutos)
            except (ValueError, TypeError):
                mensaje = "Duración inválida. Debes ingresar un número entero de minutos."
                return render(request, "R_servicio.html", {"servicio": servicio, "mensaje": mensaje})

            servicio.nombre = nombre
            servicio.descripcion = descripcion
            servicio.duracion = duracion_td
            servicio.precio = precio
            servicio.tipo = tipo
            if imagen:
                servicio.imagen = imagen
            servicio.save()
            return redirect('admin_home')
    # Para mostrar los minutos en el campo de duración
    minutos = int(servicio.duracion.total_seconds() // 60) if servicio.duracion else ""
    return render(request, "R_servicio.html", {"servicio": servicio, "minutos": minutos, "mensaje": mensaje})