from django.shortcuts import render
from APP_PRINCIPAL.models.Horario import Horario # Import the Horario model class directly

def horario_barberia(request):
    horarios = Horario.objects.all().order_by('id') # Access objects on the Horario model class
    return render(request, 'horario.html', {'horarios': horarios})