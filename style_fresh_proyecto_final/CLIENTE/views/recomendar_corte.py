from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from PIL import Image
import google.generativeai as genai
from APP_PRINCIPAL.models.diseño_corte import HaircutRecommendation

# Configura la API Key de Gemini
genai.configure(api_key="AIzaSyDD7SQE6tOKc9wrMTLMWL6SarO8a23aEe0") #AIzaSyDD7SQE6tOKc9wrMTLMWL6SarO8a23aEe0

@login_required
def formulario_recomendacion(request):
    if request.user.tipo != 'cliente':
        return JsonResponse({"error": "Solo los clientes pueden acceder a esta página."}, status=403)
    return render(request, 'recomendar_corte.html')

@csrf_exempt
def recomendar_corte_con_gemini(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Método no permitido"}, status=405)

    if not request.user.is_authenticated or request.user.tipo != 'cliente':
        return JsonResponse({"error": "Acceso no autorizado."}, status=403)

    fotos = {
        "frente": request.FILES.get('frente'),
        "lado_izq": request.FILES.get('lado_izq'),
        "lado_der": request.FILES.get('lado_der'),
        "atras": request.FILES.get('atras'),
    }

    if not all(fotos.values()):
        return JsonResponse({"error": "Faltan una o más fotos."}, status=400)

    try:
        # Abrir imágenes como PIL.Image y convertir a RGB
        imagenes_pil = [Image.open(foto).convert("RGB") for foto in fotos.values()]

        # Prompt optimizado
        prompt = (
            "Eres un barbero profesional. Basado en las fotos del rostro del cliente "
            "(frente, lados y atrás), sugiere un corte de cabello moderno, breve y claro, un poco corto, y sin poner los ** lo texto "
            "Incluye el nombre del corte, por qué le queda bien y cómo lo puede peinar."
        )

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        # Enviar texto + imágenes
        respuesta = model.generate_content(
            contents=[prompt] + imagenes_pil,
            generation_config={"temperature": 0.7}
        )

        recomendacion = respuesta.text

        # Guardar recomendación
        HaircutRecommendation.objects.create(
            cliente=request.user,
            frente=fotos["frente"],
            lado_izq=fotos["lado_izq"],
            lado_der=fotos["lado_der"],
            atras=fotos["atras"],
            recomendacion=recomendacion
        )

        return JsonResponse({"recomendacion": recomendacion})

    except Exception as e:
        return JsonResponse({"error": f"Error con Gemini: {str(e)}"}, status=500)
