from django.http import JsonResponse
from django.utils import timezone
from APP_PRINCIPAL.models.calendario.Evento import Evento
from APP_PRINCIPAL.models.Calificacion import Calificacion
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from APP_PRINCIPAL.models.usuarios.Cliente import Cliente


def ultima_cita_pendiente_calificar(request):
    usuario = request.user
    try:
        cliente = Cliente.objects.get(username=usuario.username)
        print("Cliente encontrado:", cliente, cliente.persona.id)
    except Cliente.DoesNotExist:
        print("No es cliente")
        return JsonResponse({'cita': None})

    ahora = timezone.now()
    print("Fecha/hora actual del servidor:", ahora)

    eventos = Evento.objects.filter(persona=cliente.persona, fin__lt=ahora).order_by('-fin')
    evento_sin_calificar = None

    for evento in eventos:
        try:
            calificacion = Calificacion.objects.get(evento=evento, cliente=cliente)
            if calificacion.no_molestar or calificacion.puntuacion:
                continue  # Ya calificado o no molestar, sigue buscando
        except Calificacion.DoesNotExist:
            calificacion = None

        # Si no hay calificación, o no tiene puntuación/no molestar, este es el evento pendiente
        evento_sin_calificar = evento
        break

    if not evento_sin_calificar:
        print("No hay evento pasado sin calificar")
        return JsonResponse({'cita': None})

    evento = evento_sin_calificar
    print("Evento seleccionado:", evento)

    if not evento:
        print("No hay evento pasado")
        return JsonResponse({'cita': None})

    try:
        calificacion = Calificacion.objects.get(evento=evento, cliente=cliente)
        print("Calificacion encontrada:", calificacion)
    except Calificacion.DoesNotExist:
        calificacion = None
        print("No hay calificacion para este evento")

    if calificacion:
        print("Puntuacion:", calificacion.puntuacion, "No molestar:", calificacion.no_molestar)
        if calificacion.no_molestar or calificacion.puntuacion:
            print("Ya calificado o no molestar")
            return JsonResponse({'cita': None})

    cita_data = {
        'id': evento.id,
        'titulo': evento.titulo,
        'barbero': str(evento.barbero) if evento.barbero else '',
        'inicio': evento.inicio.strftime('%Y-%m-%d %H:%M'),
        'fin': evento.fin.strftime('%Y-%m-%d %H:%M'),
        'descripcion': evento.descripcion or ''
    }
    print("Cita pendiente encontrada:", cita_data)
    return JsonResponse({'cita': cita_data})


@csrf_exempt
@require_POST
def guardar_calificacion(request):
    try:
        data = json.loads(request.body)
        evento_id = data.get('evento_id')
        puntuacion = int(data.get('puntuacion'))
        comentario = data.get('comentario', '')

        if not (1 <= puntuacion <= 5):
            return JsonResponse({'ok': False, 'mensaje': 'Puntuación inválida'}, status=400)

        evento = Evento.objects.get(id=evento_id)
        cliente = evento.persona.cliente
        calificacion, _ = Calificacion.objects.get_or_create(evento=evento, cliente=cliente)
        calificacion.puntuacion = puntuacion
        calificacion.comentario = comentario
        calificacion.save()

        return JsonResponse({'ok': True, 'mensaje': '¡Calificación guardada!'})
    except Exception as e:
        return JsonResponse({'ok': False, 'mensaje': str(e)}, status=400)


@csrf_exempt
@require_POST
def marcar_no_molestar(request):
    try:
        data = json.loads(request.body)
        evento_id = data.get('evento_id')

        evento = Evento.objects.get(id=evento_id)
        cliente = evento.persona.cliente
        calificacion, _ = Calificacion.objects.get_or_create(evento=evento, cliente=cliente)
        calificacion.no_molestar = True
        calificacion.save()

        return JsonResponse({'ok': True, 'mensaje': 'No molestar guardado'})
    except Exception as e:
        return JsonResponse({'ok': False, 'mensaje': str(e)}, status=400)