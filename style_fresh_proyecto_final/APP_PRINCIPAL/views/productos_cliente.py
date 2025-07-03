from django.shortcuts import render
from APP_PRINCIPAL.models.Productos import Producto

def productos_cliente(request):
    productos_barberia = Producto.objects.filter(tipo='belleza')
    productos_bebidas = Producto.objects.filter(tipo='bebida')
    productos_empaquetados = Producto.objects.filter(tipo='comestible')
    productos_merch = Producto.objects.filter(tipo='merch')
    return render(request, 'productos_clientes.html', {
        'productos_barberia': productos_barberia,
        'productos_bebidas': productos_bebidas,
        'productos_empaquetados': productos_empaquetados,
        'productos_merch': productos_merch,
    })