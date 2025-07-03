# APP_PRINCIPAL/views/citas_admin_view.py
from collections import defaultdict
from datetime import date, datetime, timedelta
import locale

from django.shortcuts import render
from django.utils import timezone  # Para zonas horarias seguras
from APP_PRINCIPAL.models.calendario.Evento import Evento

# ------------ Configura la localización en castellano ------------
try:
    # Windows suele necesitar el sufijo .1252
    locale.setlocale(locale.LC_TIME, "Spanish_Spain.1252")
except locale.Error:
    # Linux / Mac
    locale.setlocale(locale.LC_TIME, "es_ES.utf8")

# -----------------------------------------------------------------
def citas_admin_view(request):
    """Panel de administración – sección Citas (carruseles + tabla completa)."""
    now = timezone.localtime()       # Respeta zona horaria de Django
    today = date.today()

    # --------------------------------------------------------------
    # 1) Carruseles → SOLO futuras (Hoy, Mañana, Próximos)
    # --------------------------------------------------------------
    eventos_futuros = (
        Evento.objects
        .filter(inicio__date__gte=today)   # >= hoy
        .select_related("persona")
        .order_by("inicio")
    )

    eventos_por_fecha = defaultdict(list)
    fechas_ordenadas = []  # Mantendrá ["Hoy", "Mañana", "Martes 02 de Julio", …]

    # Creamos un set ordenado de fechas únicas futuras
    fechas_unicas = sorted({e.inicio.date() for e in eventos_futuros})

    # Etiquetamos cada fecha
    for f in fechas_unicas:
        if f == today:
            label = "Hoy"
        elif f == today + timedelta(days=1):
            label = "Mañana"
        else:
            # Ej.: "Martes 02 de Julio"
            label = f.strftime("%A %d de %B").capitalize()
        fechas_ordenadas.append(label)

    # Agrupamos eventos bajo esa misma etiqueta
    for evento in eventos_futuros:
        if evento.inicio.date() == today:
            clave = "Hoy"
        elif evento.inicio.date() == today + timedelta(days=1):
            clave = "Mañana"
        else:
            clave = evento.inicio.strftime("%A %d de %B").capitalize()
        eventos_por_fecha[clave].append(evento)

    # --------------------------------------------------------------
    # 2) Tabla completa → TODAS las citas (pasadas + futuras)
    # --------------------------------------------------------------
    eventos_citas_tabla = (
        Evento.objects
        .all()
        .select_related("persona")
        .order_by("-inicio")  # Más reciente primero
    )

    # Búsqueda libre en la tabla (opcional)
    buscar_cita_query = request.GET.get("buscar_cita", "").strip()
    if buscar_cita_query:
        eventos_citas_tabla = (
            eventos_citas_tabla
            .filter(titulo__icontains=buscar_cita_query)
            .select_related("persona")
        )

    # --------------------------------------------------------------
    # 3) Renderizamos el panel
    # --------------------------------------------------------------
    return render(
        request,
        "home_admin.html",
        {
            # Para los carruseles
            "eventos_por_fecha": eventos_por_fecha,
            "fechas_ordenadas":  fechas_ordenadas,

            # Para la tabla completa
            "eventos_citas_tabla": eventos_citas_tabla,
            "buscar_cita_query":   buscar_cita_query,
        },
    )
