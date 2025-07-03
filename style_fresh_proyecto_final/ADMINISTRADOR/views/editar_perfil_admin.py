from django.contrib import messages, auth        # ← import logout vía auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from APP_PRINCIPAL.models.usuarios.Administrador import Administrador


@login_required
def editar_perfil_admin(request):
    """
    - Actualiza datos básicos desde el modal.
    - Si el admin cambia su contraseña → cierra sesión y redirige a login.
    - Si solo edita datos → guarda y vuelve a admin_home.
    """
    admin = Administrador.objects.get(id=request.user.id)

    if request.method == "POST":
        data = request.POST

        # 1️⃣ Actualizar campos de perfil
        admin.nombre   = data.get("nombre",   admin.nombre)
        admin.apellido = data.get("apellido", admin.apellido)
        admin.telefono = data.get("telefono", admin.telefono)
        admin.username = data.get("username", admin.username)
        admin.email    = data.get("email",    admin.email)

        if "foto_perfil" in request.FILES:
            admin.foto_perfil = request.FILES["foto_perfil"]

        # 2️⃣ Validar / cambiar contraseña
        old_pass  = data.get("old_password")
        new_pass  = data.get("new_password")
        new_pass2 = data.get("new_password2")

        if any([old_pass, new_pass, new_pass2]):             # si tocó algún campo de clave
            if not all([old_pass, new_pass, new_pass2]):
                messages.error(request, "Para cambiar la contraseña completa los 3 campos.")
                return _recarga_con_modal(request, admin, data)

            if not admin.check_password(old_pass):
                messages.error(request, "La contraseña actual es incorrecta.")
                return _recarga_con_modal(request, admin, data)

            if new_pass != new_pass2:
                messages.error(request, "Las nuevas contraseñas no coinciden.")
                return _recarga_con_modal(request, admin, data)

            # Cambiar contraseña y guardar
            admin.set_password(new_pass)
            admin.save(update_fields=["password"])           # guarda solo la clave
            messages.success(request, "Contraseña actualizada con éxito. Inicia sesión de nuevo.")

            # 🔒 Cerrar sesión y mandar al login
            auth.logout(request)
            return redirect("login")                        # nombre de tu URL de login

        # 3️⃣ Guardar cambios generales (sin cambio de clave)
        admin.save()
        messages.success(request, "Perfil actualizado correctamente.")
        return redirect("admin_home")                       # ruta normal

    # GET → mostrar página con modal cerrado
    return render(request, "home_admin.html", {"admin": admin})


# -----------------------------------------------------------------
# Helper: recargar página con los datos que el usuario intentó enviar
# -----------------------------------------------------------------
def _recarga_con_modal(request, admin, form_data):
    return render(
        request,
        "home_admin.html",
        {
            "admin": admin,
            "form_data": form_data,   # conserva inputs para el modal
        },
    )
