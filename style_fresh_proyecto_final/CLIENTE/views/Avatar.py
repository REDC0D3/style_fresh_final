from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.base import ContentFile
from APP_PRINCIPAL.models.usuarios.Cliente import Cliente
import base64, uuid

# === Vista que muestra el editor de avatar ===
@login_required
def crear_avatar(request):
    cliente = Cliente.objects.get(username=request.user.username)
    return render(request, 'Avatar.html', {'cliente': cliente})


# === Vista que guarda el avatar como foto de perfil ===
@csrf_exempt
@login_required
def guardar_avatar_png(request):
    if request.method == 'POST':
        avatar_file = request.FILES.get('avatar_png')
        if not avatar_file:
            return JsonResponse({'success': False, 'error': 'No se recibió la imagen.'}, status=400)

        cliente = Cliente.objects.get(username=request.user.username)
        cliente.foto_perfil.save(f"avatar_{uuid.uuid4()}.png", avatar_file)
        cliente.save()

        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)
