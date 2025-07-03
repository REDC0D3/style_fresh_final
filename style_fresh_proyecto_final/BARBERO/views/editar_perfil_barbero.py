from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from APP_PRINCIPAL.models.usuarios.Barbero import Barbero   # ajusta la ruta

@login_required
def editar_perfil_barbero(request):
    """
    Igual que admin/cliente:
    - Si cambia contraseña → cerrar sesión y mandar a login.
    - Si solo edita datos → guardar y volver a home_barbero.
    """
    barbero = Barbero.objects.get(id=request.user.id)

    if request.method == "POST":
        d = request.POST

        # Datos básicos
        barbero.nombre   = d.get("nombre",   barbero.nombre)
        barbero.apellido = d.get("apellido", barbero.apellido)
        barbero.telefono = d.get("telefono", barbero.telefono)
        barbero.username = d.get("username", barbero.username)
        barbero.email    = d.get("email",    barbero.email)

        if "foto_perfil" in request.FILES:
            barbero.foto_perfil = request.FILES["foto_perfil"]

        # Contraseña
        old, new1, new2 = d.get("old_password"), d.get("new_password"), d.get("new_password2")
        if any([old, new1, new2]):
            if not all([old, new1, new2]):
                messages.error(request, "Completa los 3 campos de contraseña.")
                return _recarga(request, barbero, d)

            if not request.user.check_password(old):
                messages.error(request, "La contraseña actual es incorrecta.")
                return _recarga(request, barbero, d)

            if new1 != new2:
                messages.error(request, "Las nuevas contraseñas no coinciden.")
                return _recarga(request, barbero, d)

            request.user.set_password(new1)
            request.user.save(update_fields=["password"])
            messages.success(request, "Contraseña cambiada. Inicia sesión de nuevo.")
            auth.logout(request)
            return redirect("login")

        # Guardar resto de datos
        barbero.save()
        messages.success(request, "Perfil actualizado correctamente.")
        return redirect("home_barbero")

    return render(request, "home_barbero.html", {"barbero": barbero})

def _recarga(request, barbero, form_data):
    return render(request, "home_barbero.html",
                  {"barbero": barbero, "form_data": form_data})
