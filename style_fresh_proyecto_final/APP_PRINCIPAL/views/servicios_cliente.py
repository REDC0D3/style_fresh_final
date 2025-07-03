from django.shortcuts import render
from APP_PRINCIPAL.models.Servicio import Servicio

def servicios_cliente(request):
    servicios_normal = Servicio.objects.filter(tipo='normal')
    servicios_vip = Servicio.objects.filter(tipo='vip')
    servicios_otro = Servicio.objects.filter(tipo='otro')
    return render(request, "servicios_cliente.html", {
        "servicios_normal": servicios_normal,
        "servicios_vip": servicios_vip,
        "servicios_otro": servicios_otro,
    })

