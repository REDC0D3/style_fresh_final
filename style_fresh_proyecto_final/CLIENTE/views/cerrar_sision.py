# APP_PRINCIPAL/views.py (o el archivo views.py de tu aplicación principal)

# Importaciones necesarias
from django.shortcuts import render, redirect
from django.contrib.auth import logout # Función de Django para cerrar sesión
from django.contrib import messages # Para usar los mensajes flash de Django


# ... (Tus otras vistas irían aquí, por ejemplo, home_cliente, editar_perfil_cliente, etc.) ...


# Función para cerrar sesión de forma personalizada
def cerrar_sesion_personalizado(request):
    logout(request) # Llama a la función de Django para cerrar la sesión del usuario actual
    messages.success(request, "Has cerrado sesión correctamente. ¡Vuelve pronto!") # Añade un mensaje de éxito
    return redirect('pagina_principal') # Redirige al usuario a la página 'pagina_principal'
                                      # Asegúrate de que 'pagina_principal' sea el nombre de URL correcto
                                      # de tu vista de página principal.