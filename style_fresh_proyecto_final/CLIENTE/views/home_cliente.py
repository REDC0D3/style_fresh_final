from django.shortcuts import render
from APP_PRINCIPAL.models.usuarios.Cliente import Cliente

def home_cliente(request):
    """
    Vista para la página de inicio del cliente.
    Renderiza la plantilla 'home_cliente.html'.
    """
    cliente = Cliente.objects.get(username=request.user.username)
    return render(request, 'home_cliente.html', {'cliente': cliente})
