from django.shortcuts import render
from APP_PRINCIPAL.models.calendario.Evento import Evento
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')

def historial_admin_view(request):
    now = datetime.now()

    # Lógica para Historial de Cortes (Solo Eventos Pasados)
    historial_cortes = Evento.objects.filter(
        fin__lt=now # Filtra eventos cuya fecha y hora de FIN son ANTERIORES a la actual
    )

    # Lógica para buscar en el historial de cortes
    buscar_historial_query = request.GET.get('buscar_historial', '').strip()
    if buscar_historial_query:
        historial_cortes = historial_cortes.filter(titulo__icontains=buscar_historial_query) | \
                           historial_cortes.filter(nombre__icontains=buscar_historial_query) | \
                           historial_cortes.filter(telefono__icontains=buscar_historial_query)

    # Lógica para ordenar el historial de cortes
    orden_actual_historial = request.GET.get('ordenar_historial', '-inicio') # Por defecto: más reciente
    if orden_actual_historial == 'inicio': # 'inicio' para más antiguo
        historial_cortes = historial_cortes.order_by('inicio') 
    elif orden_actual_historial == '-inicio': # '-inicio' para más reciente
        historial_cortes = historial_cortes.order_by('-inicio')

    # Esto se pasaría al contexto de home_admin.html
    return {
        'historial_cortes': historial_cortes,
        'orden_actual_historial': orden_actual_historial,
        'buscar_historial_query': buscar_historial_query,
    }