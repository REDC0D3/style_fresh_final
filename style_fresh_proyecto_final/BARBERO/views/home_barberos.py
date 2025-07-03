from django.shortcuts import render
from APP_PRINCIPAL.models.usuarios.Barbero import Barbero
from APP_PRINCIPAL.models.Agenda import Agenda
from APP_PRINCIPAL.models.Calificacion import Calificacion
from APP_PRINCIPAL.models.calendario.Evento import Evento
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Import Paginator

from collections import defaultdict
import locale
from datetime import datetime, date, timedelta

locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')

def home_barbero(request):
    barbero = Barbero.objects.get(username=request.user.username)
    
    now = datetime.now() 
    today = date.today() 

    # --- Lógica para Citas Futuras (los 3 Carruseles: Hoy, Mañana, Próximos Días) ---
    eventos_futuros = Evento.objects.filter(
        barbero=barbero,
        inicio__gte=now
    ).order_by('inicio') 
    
    eventos_por_fecha_futuros = defaultdict(list)
    fechas_unicas_futuras = sorted(list(set([e.inicio.date() for e in eventos_futuros])))
    fechas_ordenadas_futuras_str = []

    for f_obj in fechas_unicas_futuras:
        if f_obj == today:
            fechas_ordenadas_futuras_str.append("Hoy")
        elif f_obj == today + timedelta(days=1):
            fechas_ordenadas_futuras_str.append("Mañana")
        else:
            fechas_ordenadas_futuras_str.append(f_obj.strftime('%A %d de %B').capitalize())

    for evento in eventos_futuros:
        if evento.inicio.date() == today:
            clave_fecha = "Hoy"
        elif evento.inicio.date() == today + timedelta(days=1):
            clave_fecha = "Mañana"
        else:
            clave_fecha = evento.inicio.strftime('%A %d de %B').capitalize()
        eventos_por_fecha_futuros[clave_fecha].append(evento)
    # --- END Future Appointments Logic ---


    # --- Lógica para Historial de Cortes (Solo Eventos Pasados) ---
    historial_cortes_list = Evento.objects.filter( # Renamed to _list for pagination
        barbero=barbero,
        fin__lt=now
    )

    buscar_historial_query = request.GET.get('buscar_historial', '').strip()
    if buscar_historial_query:
        historial_cortes_list = historial_cortes_list.filter(
            titulo__icontains=buscar_historial_query
        ) | historial_cortes_list.filter(
            persona__persona_ptr__nombre__icontains=buscar_historial_query 
        ) | historial_cortes_list.filter(
            persona__persona_ptr__apellido__icontains=buscar_historial_query
        ) | historial_cortes_list.filter(
            persona__persona_ptr__telefono__icontains=buscar_historial_query
        )

    orden_actual_historial = request.GET.get('ordenar_historial', '-inicio')
    if orden_actual_historial == 'inicio':
        historial_cortes_list = historial_cortes_list.order_by('inicio') 
    elif orden_actual_historial == '-inicio':
        historial_cortes_list = historial_cortes_list.order_by('-inicio')

    # Pagination for Historial Cortes
    historial_page = request.GET.get('historial_page', 1)
    paginator_historial = Paginator(historial_cortes_list, 10) # 10 items per page
    try:
        historial_cortes = paginator_historial.get_page(historial_page)
    except PageNotAnInteger:
        historial_cortes = paginator_historial.get_page(1)
    except EmptyPage:
        historial_cortes = paginator_historial.get_page(paginator_historial.num_pages)
    # --- END Haircut History Logic ---

    # --- Lógica para Calificaciones del Barbero ---
    calificaciones_barbero_list = Calificacion.objects.filter( # Renamed to _list for pagination
        evento__barbero=barbero
    ).select_related(
        'cliente__persona_ptr',
        'evento__barbero__persona_ptr'
    ).order_by('-evento__inicio')

    # Pagination for Calificaciones Barbero
    calificaciones_page = request.GET.get('calificaciones_page', 1)
    paginator_calificaciones = Paginator(calificaciones_barbero_list, 5) # 5 items per page
    try:
        calificaciones_barbero = paginator_calificaciones.get_page(calificaciones_page)
    except PageNotAnInteger:
        calificaciones_barbero = paginator_calificaciones.get_page(1)
    except EmptyPage:
        calificaciones_barbero = paginator_calificaciones.get_page(paginator_calificaciones.num_pages)
    # --- END Barber Ratings Logic ---

    # --- Determine the initial active section ---
    seccion_activa = 'citas'

    if 'seccion' in request.GET:
        seccion_activa = request.GET.get('seccion')
    elif 'buscar_historial' in request.GET or 'ordenar_historial' in request.GET or 'historial_page' in request.GET: # Added historial_page
        seccion_activa = 'historial'
    elif 'calificaciones_page' in request.GET: # Added calificaciones_page
        seccion_activa = 'calificaciones'
    # --- END Determine active section ---


    return render(request, 'home_barbero.html', {
        'barbero': barbero,
        'eventos_por_fecha': eventos_por_fecha_futuros,
        'fechas_ordenadas': fechas_ordenadas_futuras_str,
        'historial_cortes': historial_cortes, # This is now a Page object
        'orden_actual_historial': orden_actual_historial,
        'buscar_historial_query': buscar_historial_query,
        'calificaciones_barbero': calificaciones_barbero, # This is now a Page object
        'seccion_activa': seccion_activa,
    })