from django.shortcuts import render
from APP_PRINCIPAL.models.calendario.Evento import Evento # Asegúrate de importar Evento
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')

def historial_barbero(request):
    # Obtener la fecha y hora actuales
    now = datetime.now()

    # Obtener todos los eventos que YA PASARON (fin es menor que now)
    historial_cortes_pasados = Evento.objects.filter(
        fin__lt=now # Filtra eventos cuya fecha y hora de fin son ANTERIORES a la actual
    )

    # Lógica para buscar en el historial de cortes
    buscar_historial_query = request.GET.get('buscar_historial', '').strip()
    if buscar_historial_query:
        historial_cortes_pasados = historial_cortes_pasados.filter(titulo__icontains=buscar_historial_query) | \
                                   historial_cortes_pasados.filter(nombre__icontains=buscar_historial_query) | \
                                   historial_cortes_pasados.filter(telefono__icontains=buscar_historial_query)

    # Lógica para ordenar el historial de cortes
    orden_actual_historial = request.GET.get('ordenar_historial', '-inicio') # Por defecto: más reciente
    if orden_actual_historial == 'inicio': # 'inicio' para más antiguo
        historial_cortes_pasados = historial_cortes_pasados.order_by('inicio') 
    elif orden_actual_historial == '-inicio': # '-inicio' para más reciente
        historial_cortes_pasados = historial_cortes_pasados.order_by('-inicio')

    return render(request, 'historial_barbero.html', { # Renderiza a una NUEVA plantilla si quieres que sea solo historial
        'historial_cortes': historial_cortes_pasados,
        'orden_actual_historial': orden_actual_historial,
        'buscar_historial_query': buscar_historial_query, # Pasa el término de búsqueda para mantenerlo en el input
        'seccion_activa': 'historial', # Para que el menú sepa qué item activar
    })