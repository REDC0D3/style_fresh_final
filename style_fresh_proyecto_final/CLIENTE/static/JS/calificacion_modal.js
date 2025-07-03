document.addEventListener('DOMContentLoaded', function () {
  let citaPendiente = null;
  let puntuacionSeleccionada = 0;

  // Elementos del modal
  const modal = document.getElementById('modalCalificacion');
  const estrellas = document.getElementById('estrellas');
  const comentario = document.getElementById('comentarioCalificacion');
  const btnGuardar = document.getElementById('btnGuardarCalificacion');
  const btnNoMolestar = document.getElementById('btnNoMolestar');

  // Consultar cita pendiente
  fetch('/cliente/ultima_cita_pendiente_calificar/')
    .then(response => response.json())
    .then(data => {
      if (data.cita) {
        citaPendiente = data.cita;
        mostrarModal();
      }
    })
    .catch(error => {
      console.error('Error consultando cita pendiente:', error);
    });

  // Mostrar el modal
  function mostrarModal() {
    modal.style.display = 'flex';
    resetModal();
  }

  // Resetear el modal
  function resetModal() {
    puntuacionSeleccionada = 0;
    actualizarEstrellas();
    comentario.value = '';
  }

  estrellas.querySelectorAll('.estrella').forEach((star, idx) => {
    star.addEventListener('mouseenter', function () {
      actualizarEstrellas(idx + 1);
    });
    star.addEventListener('mouseleave', function () {
      actualizarEstrellas();
    });
    star.addEventListener('click', function () {
      puntuacionSeleccionada = idx + 1;
      actualizarEstrellas();
    });
  });

  function actualizarEstrellas(hoverValor = 0) {
    estrellas.querySelectorAll('.estrella').forEach((star, idx) => {
      if ((hoverValor && idx < hoverValor) || (!hoverValor && idx < puntuacionSeleccionada)) {
        star.innerHTML = '&#9733;'; // estrella llena
        star.classList.add('selected');
      } else {
        star.innerHTML = '&#9734;'; // estrella vacía
        star.classList.remove('selected');
      }
    });
  }

  // Guardar calificación
  btnGuardar.addEventListener('click', function () {
    if (!puntuacionSeleccionada) {
      alert('Por favor selecciona una puntuación.');
      return;
    }
    fetch('/cliente/guardar_calificacion/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        evento_id: citaPendiente.id,
        puntuacion: puntuacionSeleccionada,
        comentario: comentario.value
      })
    })
      .then(response => response.json())
      .then(data => {
        // alert(data.mensaje || '¡Calificación guardada!');
        modal.style.display = 'none';
      })
      .catch(error => {
        alert('Error al guardar la calificación');
        console.error(error);
      });
  });

  // Marcar no molestar
  btnNoMolestar.addEventListener('click', function () {
    fetch('/cliente/marcar_no_molestar/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ evento_id: citaPendiente.id })
    })
      .then(response => response.json())
      .then(data => {
        // alert(data.mensaje || 'Guardado');
        modal.style.display = 'none';
      })
      .catch(error => {
        alert('Error al guardar la preferencia');
        console.error(error);
      });
  });
});