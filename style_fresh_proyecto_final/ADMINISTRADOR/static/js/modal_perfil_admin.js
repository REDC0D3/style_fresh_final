/* ============================================================
   perfil_admin_modal.js – versión estable (abre / cierra bien)
   ============================================================ */

/*-------------------------------------------------------------
  1.  ABRIR MODAL
-------------------------------------------------------------*/
function abrirEditarPerfilAdminModal (event) {
  if (event) event.preventDefault();          // por si llamas desde <a href="#">
  const modal = document.getElementById('editarPerfilAdminModal');
  if (!modal) return;

  /* Asegúrate de que el <form> NO está oculto si otro script lo dejó así */
  const form = modal.querySelector('form');
  if (form) form.style.display = 'block';

  modal.classList.add('show');
}


/*-------------------------------------------------------------
  2.  LOG-IN DE EVENTOS UNA VEZ CARGADO EL DOM
-------------------------------------------------------------*/
document.addEventListener('DOMContentLoaded', () => {

  /* ---------- Nodos clave ---------- */
  const modal      = document.getElementById('editarPerfilAdminModal');
  if (!modal) return;                         // si no existe, salimos

  const closeBtn   = document.getElementById('closeEditarPerfilAdminModal');
  const cancelBtn  = document.getElementById('cancelarEditarPerfilAdminBtn');
  const form       = modal.querySelector('form');
  const fileInput  = document.getElementById('editar_admin_foto_perfil');
  const fileLabel  = document.querySelector('.file-name-display');
  const msgDiv     = document.getElementById('form-messages-admin');
  const msgList    = document.getElementById('form-messages-list-admin');


  /* ---------- Función cerrar ---------- */
  const cerrarModal = () => {
    modal.classList.remove('show');
  };


  /* ---------- Eventos de cierre ---------- */
  closeBtn ?.addEventListener('click', cerrarModal);
  cancelBtn?.addEventListener('click', cerrarModal);

  // clic fuera del contenido
  modal.addEventListener('click', e => {
    if (e.target === modal) cerrarModal();
  });

  // evitar propagación en el interior
  modal.querySelector('.modal-content-perfil')
       ?.addEventListener('click', e => e.stopPropagation());

  // tecla Escape
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && modal.classList.contains('show')) cerrarModal();
  });


  /* ---------- “Ojitos” contraseña ---------- */
  document.querySelectorAll('.toggle-password').forEach(icon => {
    icon.addEventListener('click', () => {
      const input = document.getElementById(icon.dataset.target);
      if (!input) return;
      const hidden = input.type === 'password';
      input.type = hidden ? 'text' : 'password';
      icon.classList.toggle('fa-eye-slash', hidden);
      icon.classList.toggle('fa-eye',       !hidden);
      icon.setAttribute('aria-label', hidden ? 'Ocultar contraseña'
                                             : 'Mostrar contraseña');
    });
  });


  /* ---------- Nombre del archivo seleccionado ---------- */
  if (fileInput && fileLabel) {
    const actualizarNombre = () => {
      fileLabel.textContent = fileInput.files.length
        ? fileInput.files[0].name
        : 'Sin archivos seleccionados';
    };
    fileInput.addEventListener('change', actualizarNombre);
    actualizarNombre();                       // estado inicial
  }


  /* ---------- Ocultar bloque de mensajes vacío ---------- */
  if (msgDiv && (!msgList || msgList.children.length === 0)) {
    msgDiv.style.display = 'none';
  } else if (msgDiv) {
    msgDiv.style.display = 'block';
  }


  /* ---------- (opcional) Resetear el formulario al cerrar ---------- */
  modal.addEventListener('animationend', e => {
    if (!modal.classList.contains('show') && form) {
      form.reset();                           // limpia inputs tras cerrar
      // Vuelve a poner texto por defecto:
      if (fileLabel) fileLabel.textContent = 'Sin archivos seleccionados';
    }
  });
});
