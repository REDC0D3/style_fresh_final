from django.core.paginator import Paginator
from django.shortcuts import render
from APP_PRINCIPAL.models.Calificacion import Calificacion
from APP_PRINCIPAL.models.usuarios.Cliente import Cliente

def historial_calificaciones_cliente(request):
    cliente = Cliente.objects.get(username=request.user.username)
    calificaciones_list = Calificacion.objects.filter(cliente=cliente).select_related('evento', 'evento__barbero').order_by('-evento__inicio')
    paginator = Paginator(calificaciones_list, 5)  # 5 por página

    page_number = request.GET.get('page')
    calificaciones = paginator.get_page(page_number)
    return render(request, 'historial_cali.html', {'calificaciones': calificaciones})