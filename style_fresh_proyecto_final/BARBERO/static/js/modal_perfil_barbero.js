// ========= Modal Editar Perfil – BARBERO =========

// Abrir
function abrirEditarPerfilBarberoModal() {
  const m = document.getElementById('editarPerfilBarberoModal');
  if (m) m.classList.add('show');
}

document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('editarPerfilBarberoModal');
  if (!modal) return;

  // Cerrar
  document.getElementById('closeEditarPerfilBarberoModal')?.addEventListener('click', () => modal.classList.remove('show'));
  document.getElementById('cancelarEditarPerfilBarberoBtn')?.addEventListener('click', () => modal.classList.remove('show'));
  modal.addEventListener('click', e => { if (e.target === modal) modal.classList.remove('show'); });
  modal.querySelector('.modal-content-perfil')?.addEventListener('click', e => e.stopPropagation());
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && modal.classList.contains('show')) modal.classList.remove('show'); });

  // Toggle contraseña
  document.querySelectorAll('.toggle-password').forEach(icon => {
    icon.addEventListener('click', () => {
      const input = document.getElementById(icon.dataset.target);
      if (!input) return;
      const hidden = input.type === 'password';
      input.type = hidden ? 'text' : 'password';
      icon.classList.toggle('fa-eye-slash', hidden);
      icon.classList.toggle('fa-eye', !hidden);
    });
  });

  // Nombre del archivo
  const fileInput = document.getElementById('editar_barbero_foto_perfil');
  const fileName  = document.querySelector('.file-name-display');
  if (fileInput && fileName) {
    const updateName = () => {
      fileName.textContent = fileInput.files.length ? fileInput.files[0].name : 'Sin archivos seleccionados';
    };
    fileInput.addEventListener('change', updateName);
    updateName();
  }

  // Ocultar mensajes vacíos
  const msgDiv  = document.getElementById('form-messages-barbero');
  const msgList = document.getElementById('form-messages-list-barbero');
  if (msgDiv && (!msgList || msgList.children.length === 0)) msgDiv.style.display = 'none';
});

