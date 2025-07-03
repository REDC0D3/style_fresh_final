// =====================
// Menú desplegable perfil (Función compartida con home_cliente.html)
// =====================
function toggleMenuPerfil() {
  const menu = document.getElementById('menuPerfil');
  const btn = document.querySelector('.btn-perfil');
  const expanded = menu && menu.style.display === 'flex';
  if (menu && btn) {
    menu.style.display = expanded ? 'none' : 'flex';
    btn.setAttribute('aria-expanded', !expanded);
  }
}

// Cierra el menú si haces clic fuera
document.addEventListener('click', function (event) {
  const menu = document.getElementById('menuPerfil');
  const btn = document.querySelector('.btn-perfil');
  if (menu && btn && !btn.contains(event.target) && !menu.contains(event.target)) {
    menu.style.display = 'none';
    btn.setAttribute('aria-expanded', false);
  }
});

// =====================
// Modal de editar perfil (Función para abrir el modal)
// =====================
function abrirEditarPerfilClienteModal() {
  const modal = document.getElementById('editarPerfilClienteModal');
  if (modal) {
    modal.classList.add('show');
  }
}

// =====================
// Lógica principal del modal y funcionalidades al cargar el DOM
// =====================
document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('editarPerfilClienteModal');
  const closeBtn = document.getElementById('closeEditarPerfilClienteModal');
  const cancelBtn = document.getElementById('cancelarEditarPerfilClienteBtn');

  if (closeBtn) {
    closeBtn.onclick = () => modal.classList.remove('show');
  }

  if (cancelBtn) {
    cancelBtn.onclick = () => modal.classList.remove('show');
  }

  // Cerrar con tecla Escape
  document.addEventListener('keydown', function (e) {
    if (e.key === "Escape" && modal && modal.classList.contains('show')) {
      modal.classList.remove('show');
    }
  });

  // Cerrar si se hace clic fuera del contenido del modal
  if (modal) {
      modal.addEventListener('click', (event) => {
          // Solo cierra si el clic fue directamente en el fondo del modal, no en su contenido
          if (event.target === modal) {
              modal.classList.remove('show');
          }
      });
  }

  // Evitar cierre si se hace clic dentro del contenido del modal
  modal?.querySelector('.modal-content-perfil')?.addEventListener('click', e => {
    e.stopPropagation();
  });

  // =====================
  // Mostrar/ocultar contraseña (¡Esta es la funcionalidad que quieres!)
  // =====================
  document.querySelectorAll('.toggle-password').forEach(icon => {
    icon.addEventListener('click', () => {
      const input = document.getElementById(icon.dataset.target); 
      if (input) {
        const isHidden = input.type === 'password';
        input.type = isHidden ? 'text' : 'password'; 

        // Alterna las clases de FontAwesome para cambiar el icono
        icon.classList.toggle('fa-eye', !isHidden);
        icon.classList.toggle('fa-eye-slash', isHidden);
        
        icon.setAttribute('aria-label', isHidden ? 'Ocultar contraseña' : 'Mostrar contraseña');
      }
    });
  });

  // =====================
  // Lógica para mostrar el nombre del archivo seleccionado en el campo de "Foto de Perfil"
  // =====================
  const fileInput = document.getElementById('editar_cliente_foto_perfil');
  const fileNameDisplay = document.querySelector('.file-name-display');

  if (fileInput && fileNameDisplay) {
      fileInput.addEventListener('change', function() {
          if (this.files && this.files.length > 0) {
              fileNameDisplay.textContent = this.files[0].name;
          } else {
              fileNameDisplay.textContent = 'Sin archivos seleccionados';
          }
      });
      // Set initial display if a file is already selected (e.g., from Django's initial data)
      if (fileInput.files && fileInput.files.length > 0) {
          fileNameDisplay.textContent = fileInput.files[0].name;
      }
  }

  // =====================
  // Ocultar/mostrar mensajes de Django si están vacíos (al cargar)
  // =====================
  const formMessagesDiv = document.getElementById('form-messages');
  const formMessagesList = document.getElementById('form-messages-list');

  // Asegurarse de que el div de mensajes se muestre solo si tiene elementos <li> dentro
  if (formMessagesDiv && (!formMessagesList || formMessagesList.children.length === 0)) {
      formMessagesDiv.style.display = 'none';
  } else if (formMessagesDiv) {
      formMessagesDiv.style.display = 'block'; 
  }
});