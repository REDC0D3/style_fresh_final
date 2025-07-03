/*  Calendario de reservas – Fresh Style
    --------------------------------------------------------------
    – Lee una recomendación guardada en localStorage
    – La pre‑carga en el modal de cita
    – Limpia la clave al confirmar                  */
document.addEventListener('DOMContentLoaded', function () {

  /* ---------------- Referencias DOM ---------------- */
  const calendarEl               = document.getElementById('calendar');
  let   fechaSeleccionada        = null;

  const modal                    = document.getElementById('reservaModal');
  const cerrarModal              = document.getElementById('cerrarModal');
  const formReserva              = document.getElementById('formReserva');

  const mensajeModal             = document.getElementById('mensajeConfirmacion');
  const cerrarMensaje            = document.getElementById('cerrarMensaje');
  const textoConfirmacion        = document.getElementById('textoConfirmacion');

  const nombreDisplay            = document.getElementById('nombre_display');
  const telefonoInput            = document.getElementById('telefono');
  const telefonoGroup            = document.getElementById('telefono_group');

  const btnAbrirModalBarberos    = document.getElementById('abrirModalBarberos');
  const modalBarberos            = document.getElementById('modalBarberos');
  const cerrarModalBarberos      = document.getElementById('cerrarModalBarberos');
  const contenedorBarberos       = document.getElementById('contenedorBarberos');
  const barberoSeleccionadoInput = document.getElementById('barberoSeleccionado');
  const barberoSeleccionadoTexto = document.getElementById('barberoSeleccionadoTexto');

  /* --- 1. Recomendación traída desde recomendar_corte.html --- */
  let recomendacionCorte = localStorage.getItem('recomendacionCorte') || null;

  /* ---------------- Datos de usuario / barberos ---------------- */
  const userDataMeta = document.querySelector('meta[name="user-data"]');
  let userData = {};
  try {
    if (userDataMeta && userDataMeta.content) {
      userData = JSON.parse(userDataMeta.content);
    }
  } catch (e) { console.error("Error al interpretar los datos del usuario:", e); }

  const barberosDataMeta = document.querySelector('meta[name="barberos-data"]');
  let barberos = [];
  try {
    if (barberosDataMeta && barberosDataMeta.content) {
      barberos = JSON.parse(barberosDataMeta.content);
    }
  } catch (e) { console.error("Error al interpretar los datos de barberos:", e); }

  /* ---------------- Renderizado de tarjetas de barbero ---------------- */
  barberos.forEach(barbero => {
    const tarjeta = document.createElement('div');
    tarjeta.className = 'tarjeta-barbero';
    tarjeta.style.cssText = 'border:1px solid #ccc;border-radius:10px;padding:10px;cursor:pointer;width:150px;text-align:center;';

    const img = document.createElement('img');
    img.src   = barbero.foto || '/static/img/default_barbero.png';
    img.alt   = barbero.nombre;
    img.style.cssText = 'width:100%;border-radius:10px;';

    const nombre = document.createElement('p');
    nombre.textContent = `${barbero.nombre} ${barbero.apellido}`;

    tarjeta.append(img, nombre);

    tarjeta.onclick = () => {
      barberoSeleccionadoInput.value = barbero.id;
      barberoSeleccionadoTexto.textContent = `Barbero seleccionado: ${barbero.nombre} ${barbero.apellido}`;
      modalBarberos.style.display = 'none';
    };

    contenedorBarberos.appendChild(tarjeta);
  });

  /* ---------------- Pre‑rellenar datos de usuario ---------------- */
  if (userData.nombre_cliente) nombreDisplay.value = userData.nombre_cliente;
  if (userData.telefono_cliente) {
    telefonoInput.value = userData.telefono_cliente;
    telefonoInput.removeAttribute('required');
    telefonoGroup.style.display = 'none';
  }

  /* ---------------- Manejo de modales ---------------- */
  cerrarModal.onclick         = () => modal.style.display = 'none';
  cerrarMensaje.onclick       = () => mensajeModal.style.display = 'none';
  btnAbrirModalBarberos.onclick = () => modalBarberos.style.display = 'flex';
  cerrarModalBarberos.onclick = () => modalBarberos.style.display = 'none';

  window.onclick = (e) => {
    if (e.target === modal)          modal.style.display = 'none';
    if (e.target === mensajeModal)   mensajeModal.style.display = 'none';
    if (e.target === modalBarberos)  modalBarberos.style.display = 'none';
  };

  /* ---------------- FullCalendar ---------------- */
  const hoy = new Date().toISOString().split('T')[0];

  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView : 'dayGridMonth',
    locale      : 'es',
    events      : '/cliente/eventos/',
    selectable  : true,
    validRange  : { start: hoy },
    selectAllow : (info) => info.startStr >= hoy,

    /* ----- 2. Selección de una fecha ----- */
    select(info) {
      if (info.startStr < hoy) {
        alert('No puedes agendar en días pasados.');
        calendar.unselect();
        return;
      }

      fechaSeleccionada = info.startStr;
      modal.style.display = 'flex';

      const descripcionInput = document.getElementById('descripcion');

      /* >>> Precargar recomendación si existe <<< */
      if (descripcionInput) {
        descripcionInput.value = recomendacionCorte ? recomendacionCorte : '';
      }

      /* Mantener lógica previa de teléfono y barbero */
      if (userData.telefono_cliente) {
        telefonoInput.value = userData.telefono_cliente;
        telefonoInput.removeAttribute('required');
        telefonoGroup.style.display = 'none';
      } else {
        telefonoInput.value = '';
        telefonoInput.setAttribute('required', 'required');
        telefonoGroup.style.display = 'block';
      }

      barberoSeleccionadoInput.value = '';
      barberoSeleccionadoTexto.textContent = '';
    }
  });

  /* ----- 3. Envío del formulario de reserva ----- */
  formReserva.onsubmit = function (e) {
    e.preventDefault();

    /* Limpia localStorage para no re‑utilizar la recomendación */
    localStorage.removeItem('recomendacionCorte');
    recomendacionCorte = null;

    const telefono     = telefonoInput.value;
    const horaInicio   = document.getElementById('horaInicio').value;
    const descripcion  = document.getElementById('descripcion').value;
    const barberoId    = barberoSeleccionadoInput.value;

    if (telefonoInput.hasAttribute('required') && !telefono.trim()) {
      alert('Por favor, ingresa tu número de teléfono.');
      return;
    }
    if (!barberoId) { alert('Por favor, selecciona un barbero.'); return; }
    if (!horaInicio) { alert('Por favor, selecciona una hora de inicio.'); return; }

    /* Calcular hora de fin (1 h) */
    const [h, m]   = horaInicio.split(':');
    const finHour  = String(Number(h) + 1).padStart(2, '0');
    const finLocal = `${fechaSeleccionada}T${finHour}:${m}`;

    const dataToSend = {
      inicio     : `${fechaSeleccionada}T${horaInicio}`,
      fin        : finLocal,
      telefono,
      descripcion,
      barbero_id : barberoId
    };

    fetch('/cliente/crear/', {
      method  : 'POST',
      headers : {
        'Content-Type': 'application/json',
        'X-CSRFToken' : document.querySelector('[name=csrf-token]').content
      },
      body: JSON.stringify(dataToSend)
    })
    .then(res => res.json().then(d => { if (!res.ok) throw new Error(d.mensaje || 'Error'); return d; }))
    .then(() => {
      modal.style.display = 'none';
      formReserva.reset();
      const nombre = userData.nombre_cliente || 'cliente';
      textoConfirmacion.textContent = `¡Gracias ${nombre}! Tu cita ha sido asignada.`;
      mensajeModal.style.display = 'flex';
      calendar.refetchEvents();
    })
    .catch(err => {
      console.error('Error al crear el evento:', err);
      textoConfirmacion.textContent = err.message || 'Error al reservar la cita.';
      mensajeModal.style.display = 'flex';
    });
  };

  calendar.render();
});
