/*  ver_descripcion.js
    ————————————————————————
    Muestra la descripción de la cita en un modal
*/

/* —— mini‑Markdown: negritas, viñetas, saltos —— */
function miniMarkdown(str){
  return str
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>') // **negritas**
    .replace(/^\s*[-*]\s+/gm, '• ')                   // • viñeta
    .replace(/\n/g, '<br>');                          // <br>
}

/* —— abrir modal —— */
document.addEventListener('click', e => {
  if (e.target.classList.contains('btn-ver-desc')) {
    const raw     = e.target.dataset.descripcion;      // texto escapado
    const decoded = JSON.parse('"' + raw + '"');       // unescape \uXXXX
    const html    = miniMarkdown(decoded);

    document.getElementById('textoDescripcion').innerHTML = html;
    document.getElementById('modalDescripcion').style.display = 'flex';
  }
});

/* —— cerrar modal —— */
document.addEventListener('DOMContentLoaded', () => {
  const modal      = document.getElementById('modalDescripcion');
  const cerrarBtn  = document.getElementById('cerrarModalDesc');

  cerrarBtn.onclick = () => modal.style.display = 'none';

  window.onclick = e => {
    if (e.target === modal) modal.style.display = 'none';
  };
});
