from django.shortcuts import render, redirect
from django.urls import reverse
from APP_PRINCIPAL.models.Configuracion import Configuracion_barberia

def configurar_barberia(request):
    configuracion, created = Configuracion_barberia.objects.get_or_create(pk=1)

    if request.method == "POST":
        if 'submit_horario' in request.POST:
            configuracion.horario = request.POST.get('horario', configuracion.horario)
        elif 'submit_ubicacion' in request.POST:
            configuracion.ubicacion = request.POST.get('ubicacion', configuracion.ubicacion)
        elif 'submit_telefono' in request.POST:
            configuracion.telefono = request.POST.get('telefono', configuracion.telefono)
        elif 'submit_email' in request.POST:
            configuracion.email = request.POST.get('email', configuracion.email)
        elif 'submit_redes_sociales' in request.POST:
            configuracion.redes_sociales = request.POST.get('redes_sociales', configuracion.redes_sociales)
        configuracion.save()

        return redirect(reverse('admin_home') + '?seccion=configuracion')
    
    return render(request, 'home_admin.html', {'configuracion': configuracion})