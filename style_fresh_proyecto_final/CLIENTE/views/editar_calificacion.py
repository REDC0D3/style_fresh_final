from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from APP_PRINCIPAL.models.Calificacion import Calificacion

@csrf_exempt
def editar_calificacion(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        calificacion_id = data.get('calificacion_id')
        puntuacion = data.get('puntuacion')
        comentario = data.get('comentario')
        try:
            calificacion = Calificacion.objects.get(id=calificacion_id)
            calificacion.puntuacion = puntuacion
            calificacion.comentario = comentario
            calificacion.save()
            return JsonResponse({'ok': True})
        except Calificacion.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'No existe la calificación'})
    return JsonResponse({'ok': False, 'error': 'Método no permitido'})