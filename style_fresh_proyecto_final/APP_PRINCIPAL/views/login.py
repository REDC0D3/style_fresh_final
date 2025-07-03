# login.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_1(request):
    """
    Vista para iniciar sesión de usuarios.
    - Si es GET, muestra el formulario de login.
    - Si es POST, valida las credenciales y redirige según el tipo de usuario.
    """
    username = ""
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Hola, {user.first_name or user.username}! Has iniciado sesión correctamente.')
            if hasattr(user, 'tipo'):
                if user.tipo == 'admin':
                    return redirect('admin_home')
                elif user.tipo == 'barbero':
                    return redirect('home_barbero')
                elif user.tipo == 'cliente':
                    return redirect('home_cliente')
            return redirect('pagina_principal')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
            return render(request, 'inicio.html', {'username': username})
    return render(request, 'inicio.html', {'username': username})