from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from APP_PRINCIPAL.models.Horario import Horario

def modificar_horario(request):
    if request.method == "POST":
        dia_modificar = request.POST.get("dia")  # Recuperamos desde el formulario
        apertura = request.POST.get("hora_apertura")
        cierre = request.POST.get("hora_cierre")

        if not apertura or not cierre or not dia_modificar:
            messages.error(request, "Todos los campos son obligatorios.")
        elif apertura >= cierre:
            messages.error(request, "La hora de cierre debe ser posterior a la de apertura.")
        else:
            horario = get_object_or_404(Horario, dia=dia_modificar)
            horario.apertura = apertura
            horario.cierre = cierre
            horario.save()
            messages.success(request, f"Horario de {dia_modificar.capitalize()} actualizado correctamente.")

        return redirect('admin_home')
