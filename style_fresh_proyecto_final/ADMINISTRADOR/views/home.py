# APP_PRINCIPAL/views/home_admin.py
from collections import defaultdict
from datetime import date, timedelta
import locale

from django.shortcuts import render
from django.utils import timezone

from APP_PRINCIPAL.models.usuarios.Cliente        import Cliente
from APP_PRINCIPAL.models.usuarios.Barbero        import Barbero
from APP_PRINCIPAL.models.usuarios.Administrador  import Administrador
from APP_PRINCIPAL.models.Productos               import Producto
from APP_PRINCIPAL.models.Servicio                import Servicio
from APP_PRINCIPAL.models.Horario                 import Horario
from APP_PRINCIPAL.models.calendario.Evento       import Evento
from APP_PRINCIPAL.models.Calificacion            import Calificacion
from django.db import models                       # para annotate si lo usas

# -------- Localización castellano ----------
try:
    locale.setlocale(locale.LC_TIME, "Spanish_Spain.1252")   # Windows
except locale.Error:
    locale.setlocale(locale.LC_TIME, "es_ES.utf8")           # Linux / Mac
# -------------------------------------------


def home_admin(request):
    """Panel principal del administrador (citas + tablas varias)."""

    # ─────────── Datos básicos del admin logueado ───────────
    admin = Administrador.objects.filter(id=request.user.id).first()

    # ─────────── Colecciones generales (clientes, etc.) ─────
    clientes   = Cliente.objects.all()
    barberos   = Barbero.objects.all()
    admins     = Administrador.objects.all()
    productos  = Producto.objects.all()
    servicios  = Servicio.objects.all()
    horarios   = Horario.objects.all().order_by("id")
    califs     = Calificacion.objects.all()

    # ════════════════════════════════════════════════════════
    # 1) CARRUSELES –- solo citas FUTURAS (Hoy / Mañana / Próximos)
    # ════════════════════════════════════════════════════════
    today = date.today()

    eventos_futuros = (
        Evento.objects
        .filter(inicio__date__gte=today)
        .select_related("persona")
        .order_by("inicio")
    )

    eventos_por_fecha = defaultdict(list)   # {"Hoy": [e1, e2], "Mañana": [...], "Martes 02 de Julio": [...]}
    fechas_ordenadas  = []                  # ["Hoy", "Mañana", "Martes 02 de Julio", …]

    for ev in eventos_futuros:
        # etiqueta human-friendly que usa el template
        if ev.inicio.date() == today:
            label = "Hoy"
        elif ev.inicio.date() == today + timedelta(days=1):
            label = "Mañana"
        else:
            label = ev.inicio.strftime("%A %d de %B").capitalize()

        # Guardamos sin duplicados y agrupamos
        if label not in fechas_ordenadas:
            fechas_ordenadas.append(label)

        eventos_por_fecha[label].append(ev)

    # ════════════════════════════════════════════════════════
    # 2) HISTORIAL DE CORTES (tabla completa, opcional búsqueda/orden)
    # ════════════════════════════════════════════════════════
    historial = Evento.objects.filter(inicio__date__lt=today)

    buscar_hist = request.GET.get("buscar_historial", "").strip()
    if buscar_hist:
        historial = (
            historial.filter(titulo__icontains=buscar_hist) |
            historial.filter(persona__persona_ptr__nombre__icontains=buscar_hist) |
            historial.filter(persona__persona_ptr__apellido__icontains=buscar_hist) |
            historial.filter(persona__persona_ptr__telefono__icontains=buscar_hist)
        )

    orden_hist = request.GET.get("ordenar_historial", "-inicio")
    if orden_hist == "inicio":
        historial = historial.order_by("inicio")
    elif orden_hist == "-inicio":
        historial = historial.order_by("-inicio")
    elif orden_hist == "puntuacion_desc":
        historial = historial.annotate(p=models.F("calificacion__puntuacion")).order_by("-p", "-inicio")
    elif orden_hist == "puntuacion_asc":
        historial = historial.annotate(p=models.F("calificacion__puntuacion")).order_by("p", "inicio")

    # ════════════════════════════════════════════════════════
    # 3) Determinar qué sección lateral se marca como activa
    # ════════════════════════════════════════════════════════
    seccion = "citas"  # por defecto

    if any(param in request.GET for param in ("buscar_cliente", "crear_cliente")):
        seccion = "clientes"
    elif any(param in request.GET for param in ("buscar_barbero",)):
        seccion = "barberos"
    elif any(param in request.GET for param in ("buscar_admin",)):
        seccion = "admins"
    elif any(param in request.GET for param in ("buscar_producto",)):
        seccion = "productos"
    elif any(param in request.GET for param in ("buscar_servicio",)):
        seccion = "servicios"
    elif buscar_hist or "ordenar_historial" in request.GET:
        seccion = "historial"
    elif "seccion_calificaciones" in request.GET:
        seccion = "calificaciones"

    # ════════════════════════════════════════════════════════
    # 4) Render
    # ════════════════════════════════════════════════════════
    return render(
        request,
        "home_admin.html",
        {
            "admin": admin,

            # Tablas básicas
            "clientes":   clientes,
            "barberos":   barberos,
            "admins":     admins,
            "productos":  productos,
            "servicios":  servicios,
            "horarios":   horarios,
            "calificaciones": califs,

            # Carruseles
            "eventos_por_fecha": eventos_por_fecha,
            "fechas_ordenadas":  fechas_ordenadas,

            # Historial de cortes
            "historial_cortes":       historial,
            "orden_actual_historial": orden_hist,
            "buscar_historial_query": buscar_hist,

            # Menú lateral
            "seccion_activa": seccion,
        },
    )
