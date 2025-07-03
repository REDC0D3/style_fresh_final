from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from APP_PRINCIPAL.models.Productos import Producto

def registrar_producto(request):
    """
    Vista para registrar un nuevo producto.
    - Si es GET, muestra el formulario de registro.
    - Si es POST, valida los datos y crea el producto si todo es correcto.
    """
    mensaje = ""
    if request.method == "POST":
        # Obtiene los datos del formulario
        nombre = request.POST.get("nombre")
        stock = request.POST.get("stock")
        precio = request.POST.get("precio")
        descripcion = request.POST.get("descripcion")
        tipo = request.POST.get("tipo")
        imagen = request.FILES.get("imagen")

        # Validación de campos obligatorios
        if not nombre or not stock or not precio or not descripcion or not tipo:
            mensaje = "Todos los campos son obligatorios."
        else:
            # Crea el nuevo producto y guarda en la base de datos
            producto = Producto(
                nombre=nombre,
                stock=stock,
                precio=precio,
                descripcion=descripcion,
                tipo=tipo
            )
            # Si se subió una imagen, la asigna
            if hasattr(producto, 'imagen') and imagen:
                producto.imagen = imagen
            producto.save()
            messages.success(request, "¡Producto registrado exitosamente!")
            return redirect('admin_home')  # Redirige al home del admin

    # Renderiza el formulario con el mensaje (si hay)
    return render(request, "R_productos.html", {"mensaje": mensaje})

def actualizar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":
        producto.nombre = request.POST.get("nombre")
        producto.descripcion = request.POST.get("descripcion")
        producto.precio = request.POST.get("precio")
        producto.stock = request.POST.get("stock")
        producto.tipo = request.POST.get("tipo")
        if request.FILES.get("imagen"):
            producto.imagen = request.FILES.get("imagen")
        producto.save()
        return redirect('admin_home')
    # Solo renderiza el formulario, sin <html>, <body>, etc.
    return render(request, "R_productos.html", {"producto": producto})