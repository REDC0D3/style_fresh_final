from django.shortcuts import render
from APP_PRINCIPAL.models.Configuracion import Configuracion_barberia

def sobre_nosotros(request):

    info_barberia = Configuracion_barberia.objects.first() 
    
    return render(request, 'sobre_nosotros.html', {'info_barberia': info_barberia})