from django.urls import path
from .views.home_cliente import home_cliente
from .views.calendario import calendario_view, eventos_json, crear_evento
from .views.historial_c import historial_cliente
from .views.historial_cali import historial_calificaciones_cliente
from .views.calificar import (
    ultima_cita_pendiente_calificar,
    guardar_calificacion,
    marcar_no_molestar,
)
from .views.cerrar_sision import cerrar_sesion_personalizado
from .views.editar_calificacion import editar_calificacion
from .views.editar_cliente import editar_perfil_cliente
from .views.recomendar_corte import formulario_recomendacion, recomendar_corte_con_gemini  # ← este sí completo
from .views.Avatar import crear_avatar, guardar_avatar_png

urlpatterns = [
    path('', home_cliente, name='home_cliente'),
    path('calendario/', calendario_view, name='calendario'),
    path('eventos/', eventos_json, name='eventos_json'),
    path('crear/', crear_evento, name='crear_evento'),
    path('historial/', historial_cliente, name='historial_cliente'),
    path('historial_calificaciones/', historial_calificaciones_cliente, name='historial_calificaciones'),

    # Calificaciones
    path('ultima_cita_pendiente_calificar/', ultima_cita_pendiente_calificar, name='ultima_cita_pendiente_calificar'),
    path('guardar_calificacion/', guardar_calificacion, name='guardar_calificacion'),
    path('marcar_no_molestar/', marcar_no_molestar, name='marcar_no_molestar'),
    path('editar_calificacion/', editar_calificacion, name='editar_calificacion'),

    # Perfil
    path('cliente/editar-perfil/', editar_perfil_cliente, name='editar_perfil_cliente'),
    path('logout/', cerrar_sesion_personalizado, name='logout'),

    # Recomendación de corte (GET y POST separados)
    path('diseño-corte/', formulario_recomendacion, name='formulario_recomendacion'),  # Muestra el formulario
    path('diseño-corte/obtener/', recomendar_corte_con_gemini, name='recomendacion_corte'),  # Procesa la IA (POST)

    #avatar
    path('avatar/', crear_avatar, name='avatar'),
    path('avatar/guardar_foto/', guardar_avatar_png, name='guardar_avatar_png'),
]
