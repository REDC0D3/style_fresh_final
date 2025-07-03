from django.shortcuts import render
from django.http import JsonResponse
from APP_PRINCIPAL.models.calendario.Evento import Evento
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.dateparse import parse_datetime
from django.db.models.functions import TruncHour
from APP_PRINCIPAL.models.usuarios import Cliente, Barbero, Persona
from django.templatetags.static import static

def calendario_view(request):
    user_data = {}
    if request.user.is_authenticated:
        if request.user.tipo == 'cliente':
            try:
                cliente_instance = Cliente.objects.get(pk=request.user.pk)
                user_data['nombre_cliente'] = cliente_instance.nombre
                user_data['telefono_cliente'] = cliente_instance.telefono
            except Cliente.DoesNotExist:
                user_data['nombre_cliente'] = request.user.username
                user_data['telefono_cliente'] = ''
        elif request.user.tipo == 'barbero':
            try:
                barbero_instance = Barbero.objects.get(pk=request.user.pk)
                user_data['nombre_cliente'] = barbero_instance.nombre
                user_data['telefono_cliente'] = barbero_instance.telefono
            except Barbero.DoesNotExist:
                user_data['nombre_cliente'] = request.user.username
                user_data['telefono_cliente'] = ''
        else:
            try:
                persona_instance = Persona.objects.get(pk=request.user.pk)
                user_data['nombre_cliente'] = persona_instance.nombre
                user_data['telefono_cliente'] = persona_instance.telefono
            except Persona.DoesNotExist:
                user_data['nombre_cliente'] = request.user.username
                user_data['telefono_cliente'] = ''

    # Obtener lista de barberos con imagen
    barberos_queryset = Barbero.objects.all()
    barberos_list = []
    for barbero in barberos_queryset:
        barberos_list.append({
            'id': barbero.id,
            'nombre': barbero.nombre,
            'apellido': barbero.apellido,
            'foto': barbero.foto_perfil.url if barbero.foto_perfil else static('img/default-barbero.jpg')
        })

    context = {
        'user_data': json.dumps(user_data),
        'barberos': json.dumps(barberos_list)
    }
    return render(request, 'calendario.html', context)

def eventos_json(request):
    eventos = Evento.objects.all()
    data = []

    for evento in eventos:
        barbero_nombre = evento.barbero.nombre if evento.barbero else "No asignado"
        data.append({
            "id": evento.id,
            "title": f"{evento.titulo} ({barbero_nombre})",
            "start": evento.inicio.isoformat(),
            "end": evento.fin.isoformat(),
            "description": evento.descripcion,
            "nombre_cliente": evento.persona.nombre if evento.persona else "Desconocido",
            "barbero_id": evento.barbero.id if evento.barbero else None,
            "barbero_nombre": barbero_nombre,
        })

    return JsonResponse(data, safe=False)

@csrf_exempt
def crear_evento(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)

            inicio = parse_datetime(data['inicio'])
            fin = parse_datetime(data['fin'])
            barbero_id = data.get('barbero_id')

            if barbero_id:
                barbero_seleccionado = Barbero.objects.get(id=barbero_id)
                existe_cita_barbero = Evento.objects.filter(
                    barbero=barbero_seleccionado,
                    inicio__lt=fin,
                    fin__gt=inicio
                ).exists()
                if existe_cita_barbero:
                    return JsonResponse({'mensaje': 'El barbero ya tiene una cita en ese horario. Por favor, elige otra hora o barbero.'}, status=400)

            existe = Evento.objects.annotate(
                hora=TruncHour('inicio')
            ).filter(
                hora=inicio.replace(minute=0, second=0, microsecond=0)
            ).exists()

            if existe:
                return JsonResponse({'mensaje': 'Ya existe una cita en esa hora. Por favor, elige otra.'}, status=400)

            persona_instance = None
            if request.user.is_authenticated:
                telefono_enviado = data.get('telefono', '')
                if request.user.tipo == 'cliente':
                    try:
                        persona_instance = Cliente.objects.get(pk=request.user.pk)
                        if telefono_enviado and persona_instance.telefono != telefono_enviado:
                            persona_instance.telefono = telefono_enviado
                            persona_instance.save()
                    except Cliente.DoesNotExist:
                        pass
                elif request.user.tipo == 'barbero':
                    try:
                        persona_instance = Barbero.objects.get(pk=request.user.pk)
                        if telefono_enviado and persona_instance.telefono != telefono_enviado:
                            persona_instance.telefono = telefono_enviado
                            persona_instance.save()
                    except Barbero.DoesNotExist:
                        pass
                else:
                    try:
                        persona_instance = Persona.objects.get(pk=request.user.pk)
                        if telefono_enviado and persona_instance.telefono != telefono_enviado:
                            persona_instance.telefono = telefono_enviado
                            persona_instance.save()
                    except Persona.DoesNotExist:
                        pass

            barbero_instance = None
            if barbero_id:
                try:
                    barbero_instance = Barbero.objects.get(id=barbero_id)
                except Barbero.DoesNotExist:
                    return JsonResponse({'mensaje': 'Barbero seleccionado no válido.'}, status=400)

            # 1. Crear el evento con un título temporal
            evento = Evento.objects.create(
                titulo="Reserva temporal",
                inicio=inicio,
                fin=fin,
                descripcion=data.get('descripcion', ''),
                persona=persona_instance,
                barbero=barbero_instance
            )

            # 2. Actualizar el título con el ID
            evento.titulo = f"Reserva número {evento.id}"
            evento.save()

            return JsonResponse({'mensaje': 'Evento creado exitosamente'}, status=201)
        except json.JSONDecodeError as e:
            return JsonResponse({'mensaje': f'Error al decodificar JSON: {str(e)}'}, status=400)
        except KeyError as e:
            return JsonResponse({'mensaje': f'Faltan datos obligatorios en la solicitud: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'mensaje': f'Error inesperado al crear evento: {str(e)}'}, status=400)

    return JsonResponse({'mensaje': 'Método no permitido'}, status=405)
