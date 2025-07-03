from django.shortcuts import render
from APP_PRINCIPAL.models.calendario.Evento import Evento

def historial_cliente(request):
    # Filtra por el usuario autenticado
    historial = Evento.objects.filter(persona_id=request.user.id).order_by('-inicio')
    return render(request, 'historial_cliente.html', {'historial': historial})