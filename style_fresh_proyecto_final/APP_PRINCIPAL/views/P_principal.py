from django.shortcuts import render, redirect

def pagina_principal(request):
    """
    Vista para mostrar la página principal del sistema.
    """
    return render(request, 'Pagina_principal.html')