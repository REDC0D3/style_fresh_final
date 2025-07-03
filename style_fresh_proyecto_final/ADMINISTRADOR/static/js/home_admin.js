// static/js/home_admin.js (Este archivo debe contener TODA la lógica JavaScript para home_admin)

// La variable 'django_urls' se asume definida en el HTML antes de cargar este script.

// Función para obtener parámetros de la URL
function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

// Función para mostrar/ocultar secciones y activar el menú
function mostrarSeccion(seccionId) {
    const seccionesAdmin = [
        'clientes', 'barberos', 'admins', 'productos', 'servicios',
        'citas', 'historial', 'configuracion', 'horario', 'calificaciones'
    ];

    seccionesAdmin.forEach(function(id) {
        const sectionElement = document.getElementById(id + '-section');
        if (sectionElement) {
            sectionElement.style.display = 'none';
            sectionElement.classList.remove('fadeIn');
        }
    });

    document.querySelectorAll('nav ul li[onclick]').forEach(item => {
        item.classList.remove('active');
        item.style.backgroundColor = '';
        item.style.color = '';
    });

    const seccionAMostrar = document.getElementById(seccionId + '-section');
    if (seccionAMostrar) {
        seccionAMostrar.style.display = 'block';
        void seccionAMostrar.offsetWidth; // Trigger reflow para reiniciar la animación CSS
        seccionAMostrar.classList.add('fadeIn');

        const menuItemActivo = document.querySelector(`li[onclick="mostrarSeccion('${seccionId}')"]`);
        if (menuItemActivo) {
            menuItemActivo.classList.add('active');
        }

        if (seccionId === 'citas') {
            setTimeout(() => {
                // Las funciones inicializarCarrusel y moverCarrusel deben estar en citas.js
                // Asegúrate de que citas.js se carga ANTES de home_admin.js en tu HTML.
                if (typeof inicializarCarrusel !== 'undefined') {
                    inicializarCarrusel('carruselTrackHoy');
                    inicializarCarrusel('carruselTrackManana');
                    inicializarCarrusel('carruselTrackProximos');
                } else {
                    console.warn("inicializarCarrusel no está definida. Asegúrate de que citas.js se carga correctamente.");
                }
            }, 200);
        }
    }
}


document.addEventListener('DOMContentLoaded', function() {
    // --- LÓGICA PARA MANEJO DE MODALES GENERAL ---
    const createItemModal = document.getElementById('createItemModal');
    const updateItemModal = document.getElementById('updateItemModal');
    const eliminarItemModal = document.getElementById('eliminarItemModal'); // Para el modal de eliminación

    const closeButtons = document.querySelectorAll('.close-button'); // Botones 'X' en todos los modales
    const cancelButtons = document.querySelectorAll('.cancel-btn'); // Botones 'Cancelar' en todos los modales
    const crearButtons = document.querySelectorAll('.boton-crear'); // Botones "+ Crear X" en la página principal

    const createModalTitle = document.getElementById('createModalTitle');
    const createModalFormContainer = document.getElementById('createModalFormContainer');
    const updateModalTitle = document.getElementById('updateModalTitle');
    const updateModalFormContainer = document.getElementById('updateModalFormContainer');

    let currentOpenModal = null; // Variable para rastrear qué modal está abierto

    // Función para abrir un modal de forma general
    function openModal(modalElement) {
        if (currentOpenModal) {
            closeModal(currentOpenModal); // Cierra cualquier modal ya abierto antes de abrir uno nuevo
        }
        modalElement.classList.add('modal-active'); // Añade la clase que lo hace visible
        currentOpenModal = modalElement; // Almacena la referencia al modal abierto
    }

    // Función para cerrar un modal de forma general
    function closeModal(modalElement) {
        modalElement.classList.remove('modal-active'); // Elimina la clase que lo hace visible
        currentOpenModal = null; // Limpia la referencia
        
        // Limpiar mensajes anteriores y resetear formularios al cerrar cualquier modal
        const messageContainers = modalElement.querySelectorAll('.modal-messages');
        messageContainers.forEach(container => container.innerHTML = ''); // Limpia los divs de mensajes

        const allFormsInModal = modalElement.querySelectorAll('form');
        allFormsInModal.forEach(form => {
            if (form.id !== 'form-eliminar-item') { // No resetear el formulario de eliminación
                form.style.display = 'none'; // Ocultar el formulario
                form.reset(); // Restablecer los campos del formulario a sus valores iniciales
                // Asegurarse de limpiar contraseñas específicamente si no se resetean
                const passwordInputs = form.querySelectorAll('input[type="password"]');
                passwordInputs.forEach(input => input.value = '');
            }
        });
        document.body.style.overflow = ''; // Habilitar el scroll del body si se deshabilitó
    }

    // Event listeners para cerrar modales
    // Cierra el modal cuando se hace clic en el botón 'X' (close-button)
    closeButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            closeModal(btn.closest('.modal')); // Encuentra el modal padre y lo cierra
        });
    });

    // Cierra el modal cuando se hace clic en el botón 'Cancelar' (cancel-btn)
    cancelButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            closeModal(btn.closest('.modal')); // Encuentra el modal padre y lo cierra
        });
    });

    // Cierra el modal cuando se hace clic fuera del contenido del modal (en el overlay oscuro)
    window.addEventListener('click', function(event) {
        if (event.target.classList.contains('modal-active')) {
            closeModal(event.target);
        }
    });

    // --- Función genérica para abrir y configurar modal de Creación ---
    // Esta función maneja la visualización del formulario, título y pre-rellenado de datos (para errores)
    function openCreateModalWithForm(formType, initialData = {}) {
        // Ocultar y limpiar todos los formularios en el contenedor de creación
        createModalFormContainer.querySelectorAll('form').forEach(form => {
            form.style.display = 'none';
            form.reset(); // Restablece los campos del formulario
            const msgContainer = form.querySelector('.modal-messages');
            if (msgContainer) msgContainer.innerHTML = ''; // Limpia cualquier mensaje anterior
        });

        const targetForm = document.getElementById(`form-${formType}`);
        if (!targetForm) {
            console.error(`Formulario de creación para ${formType} no encontrado.`);
            return;
        }

        targetForm.style.display = 'block'; // Muestra el formulario deseado

        let modalTitleText = `Crear Nuevo ${formType.charAt(0).toUpperCase() + formType.slice(1)}`;
        if (formType === 'administrador') modalTitleText = 'Crear Nuevo Administrador';
        createModalTitle.textContent = modalTitleText; // Actualiza el título del modal

        // Establecer la URL de acción del formulario (para el POST)
        let formActionUrl;
        let seccionReturn; // Para la sección de retorno en la URL
        switch (formType) {
            case 'cliente': formActionUrl = django_urls.crear_cliente_url; seccionReturn = 'clientes'; break;
            case 'barbero': formActionUrl = django_urls.crear_barbero_url; seccionReturn = 'barberos'; break;
            case 'administrador': formActionUrl = django_urls.crear_administrador_url; seccionReturn = 'admins'; break;
            case 'producto': formActionUrl = django_urls.crear_producto_url; seccionReturn = 'productos'; break;
            case 'servicio': formActionUrl = django_urls.crear_servicio_url; seccionReturn = 'servicios'; break;
            default: 
                console.error('Tipo de formulario de creación desconocido:', formType);
                return; // Salir si el tipo no es reconocido
        }
        targetForm.action = formActionUrl + '?seccion=' + seccionReturn; // Establece la URL de acción del formulario

        // Rellenar campos del formulario con los datos iniciales (útil cuando se reabre por un error)
        for (const key in initialData) {
            const inputElement = targetForm.querySelector(`[name="${key}"]`);
            if (inputElement) {
                // Evitar rellenar campos de contraseña o archivo por seguridad
                if (inputElement.type !== 'password' && inputElement.type !== 'file') {
                    inputElement.value = initialData[key];
                }
            }
        }
        openModal(createItemModal); // Finalmente, abre el modal de creación
    }

    // --- Event listeners para los botones "+ Crear X" en la página principal ---
    crearButtons.forEach(button => {
        button.addEventListener('click', function() {
            const formType = this.dataset.formType; // Obtiene el tipo de formulario ('cliente', 'barbero', etc.)
            openCreateModalWithForm(formType); // Llama a la función genérica para abrir el modal (sin datos iniciales)
        });
    });

    // --- Lógica para los modales de ACTUALIZACIÓN ---
    const updateItemBtns = document.querySelectorAll('.editar-item-btn'); // Botones "Editar" en las tablas
    const updateModal = document.getElementById('updateItemModal'); // El modal general de actualización

    updateItemBtns.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            const itemType = this.dataset.itemTipo; // 'cliente', 'barbero', etc.
            const itemSeccion = this.dataset.itemSeccion; // 'clientes', 'barberos', etc.

            // Ocultar todos los formularios de actualización y resetearlos
            updateModalFormContainer.querySelectorAll('form').forEach(form => {
                form.style.display = 'none';
                form.reset(); 
                const msgContainer = form.querySelector('.modal-messages');
                if (msgContainer) msgContainer.innerHTML = '';
            });

            const updateForm = document.getElementById(`form-update-${itemType}`);
            if (!updateForm) {
                console.error(`Formulario de actualización para ${itemType} no encontrado.`);
                return;
            }

            // Establecer la URL de acción del formulario (para el POST)
            let updateUrlBase = django_urls[`actualizar_${itemType}_url_base`];
            let fetchUrl = updateUrlBase.replace('0', itemId); // URL para obtener datos
            updateForm.action = `${updateUrlBase.replace('0', itemId)}?seccion=${itemSeccion}`; // URL para el POST

            updateModalTitle.textContent = `Actualizar ${itemType.charAt(0).toUpperCase() + itemType.slice(1)}`;

            // Realizar la petición AJAX para obtener los datos del elemento
            fetch(fetchUrl, { // Se hace un GET a la URL del API para obtener los datos del elemento a editar
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Indica que es una petición AJAX
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Poblar el formulario con los datos recibidos
                if (updateForm.querySelector(`#update_${itemType}_id`)) updateForm.querySelector(`#update_${itemType}_id`).value = data.id;
                if (data.nombre) updateForm.querySelector(`#update_${itemType}_nombre`).value = data.nombre;
                if (data.apellido) updateForm.querySelector(`#update_${itemType}_apellido`).value = data.apellido;
                if (data.username) updateForm.querySelector(`#update_${itemType}_username`).value = data.username;
                if (data.email) updateForm.querySelector(`#update_${itemType}_email`).value = data.email;
                if (data.telefono) updateForm.querySelector(`#update_${itemType}_telefono`).value = data.telefono;

                // Campos específicos (Barbero, Producto, Servicio)
                if (data.fecha_nacimiento) updateForm.querySelector(`#update_${itemType}_fecha_nacimiento`).value = data.fecha_nacimiento;
                if (data.especialidad) updateForm.querySelector(`#update_${itemType}_especialidad`).value = data.especialidad;
                if (data.stock) updateForm.querySelector(`#update_${itemType}_stock`).value = data.stock;
                if (data.precio) updateForm.querySelector(`#update_${itemType}_precio`).value = data.precio;
                if (data.descripcion) updateForm.querySelector(`#update_${itemType}_descripcion`).value = data.descripcion;
                if (data.duracion) { // Manejo especial para duración (ej. minutos a formato HH:MM si es input type="time")
                    const totalMinutes = parseInt(data.duracion, 10);
                    if (!isNaN(totalMinutes)) {
                        const hours = Math.floor(totalMinutes / 60).toString().padStart(2, '0');
                        const minutes = (totalMinutes % 60).toString().padStart(2, '0');
                        const durationTime = `${hours}:${minutes}`;
                        const durationInput = updateForm.querySelector(`#update_${itemType}_duracion`);
                        if (durationInput && durationInput.type === 'time') {
                            durationInput.value = durationTime;
                        } else if (durationInput) { // Si no es type="time", solo el número de minutos
                            durationInput.value = totalMinutes;
                        }
                    }
                }
                if (data.tipo) updateForm.querySelector(`#update_${itemType}_tipo`).value = data.tipo; // Asegurarse de que el 'select' de tipo se rellene
                
                // Manejo de la foto de perfil/imagen actual
                const currentPhotoElem = updateForm.querySelector(`#update_${itemType}_current_photo`);
                if (currentPhotoElem && (data.foto_perfil_url || data.imagen_url)) {
                    currentPhotoElem.src = data.foto_perfil_url || data.imagen_url;
                    currentPhotoElem.style.display = 'block';
                } else if (currentPhotoElem) {
                    currentPhotoElem.style.display = 'none';
                    currentPhotoElem.src = ''; // Limpiar src si no hay imagen
                }

                // Limpiar campos de contraseña por seguridad al abrir el modal de actualización
                const oldPasswordInput = updateForm.querySelector(`#update_${itemType}_old_password`);
                const newPasswordInput = updateForm.querySelector(`#update_${itemType}_new_password`);
                const newPassword2Input = updateForm.querySelector(`#update_${itemType}_new_password2`);
                if (oldPasswordInput) oldPasswordInput.value = '';
                if (newPasswordInput) newPasswordInput.value = '';
                if (newPassword2Input) newPassword2Input.value = '';

                updateForm.style.display = 'block'; // Asegura que el formulario esté visible
                openModal(updateModal); // Abre el modal de actualización
            })
            .catch(error => {
                console.error('Error al cargar los datos del elemento para actualización:', error);
                alert('No se pudieron cargar los datos para editar. Por favor, inténtalo de nuevo.');
            });
        });
    });
    
    // --- Lógica para el modal de ELIMINACIÓN ---
    const eliminarItemBtns = document.querySelectorAll('.eliminar-item-btn'); // Botones "Eliminar" en las tablas
    const eliminarModal = document.getElementById('eliminarItemModal'); // El modal de eliminación
    const itemNombreSpan = document.getElementById('item-nombre-a-eliminar'); // Span para el nombre del ítem
    const itemTipoSpan = document.getElementById('item-tipo-a-eliminar');     // Span para el tipo del ítem
    const formEliminar = document.getElementById('form-eliminar-item');       // Formulario de confirmación de eliminación

    // Mapeo de URLs de eliminación desde django_urls (definido en el HTML)
    const urlMapEliminar = { 
        'cliente': django_urls.eliminar_cliente_url,
        'barbero': django_urls.eliminar_barbero_url,
        'administrador': django_urls.eliminar_administrador_url,
        'producto': django_urls.eliminar_producto_url,
        'servicio': django_urls.eliminar_servicio_url,
    };

    eliminarItemBtns.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Evita que el enlace elimine directamente o recargue

            const itemId = this.dataset.itemId;
            const itemNombre = this.dataset.itemNombre;
            const itemTipo = this.dataset.itemTipo;

            itemNombreSpan.textContent = itemNombre; // Actualiza el nombre en el modal
            // Ajusta el texto "el" o "al" según el tipo de ítem para mejor gramática
            if (itemTipo === 'producto' || itemTipo === 'servicio') {
                itemTipoSpan.textContent = 'el ' + itemTipo;
            } else {
                itemTipoSpan.textContent = 'al ' + itemTipo;
            }

            let targetUrlTemplate = urlMapEliminar[itemTipo];
            if (targetUrlTemplate) {
                let finalUrl = targetUrlTemplate.replace('0', itemId);
                let seccionParam; // Parámetro de sección para redirigir después de eliminar
                if (itemTipo === 'administrador') {
                    seccionParam = 'admins';
                } else {
                    seccionParam = itemTipo + 's'; // Añade 's' para obtener 'clientes', 'barberos', etc.
                }
                formEliminar.action = finalUrl + '?seccion=' + seccionParam; // Establece la URL de acción para el formulario de eliminación
            } else {
                console.error('Tipo de ítem no reconocido para eliminación:', itemTipo);
                return;
            }
            openModal(eliminarModal); // Abre el modal de eliminación
        });
    });

    // --- LÓGICA PARA ALTERNAR VISIBILIDAD DE CONTRASEÑA ---
    document.querySelectorAll('.toggle-password').forEach(icon => {
        icon.addEventListener('click', function() {
            const targetId = this.dataset.target;
            const passwordInput = document.getElementById(targetId);
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            }
        });
    });

    // --- LÓGICA PARA ORDENAR HISTORIAL DE CORTES ---
    document.querySelectorAll('.ordenar-historial-btn').forEach(button => {
        button.addEventListener('click', function() {
            const orden = this.dataset.orden;
            const currentUrl = new URL(window.location.href);
            currentUrl.searchParams.set('ordenar_historial', orden);
            currentUrl.searchParams.set('seccion', 'historial'); 
            currentUrl.searchParams.delete('buscar_historial'); 
            window.location.href = currentUrl.toString(); // Recarga la página con los nuevos parámetros
        });
    });

    // --- LÓGICA PARA MOSTRAR MENSAJES DE DJANGO EN MODALES Y LIMPIAR URL ---
    // Variables para capturar parámetros de la URL (DECLARADAS UNA SOLA VEZ AQUÍ)
    const urlParams = new URLSearchParams(window.location.search);
    const modalCreateType = urlParams.get('modal_create_type');   // Tipo de modal de creación a reabrir
    const modalUpdateType = urlParams.get('modal_update_type');   // Tipo de modal de actualización a reabrir
    const modalSuccessType = urlParams.get('modal_success_type'); // Tipo de modal de éxito
    const itemIdToUpdate = urlParams.get('item_id');              // ID del ítem para actualización
    let seccionFromUrl = urlParams.get('seccion');                // SEGUNDA DECLARACIÓN: Usar 'let' para reasignación

    // Si la página se carga con un parámetro 'seccion' en la URL (ej. después de una redirección de una vista)
    // Se muestra la sección correspondiente. Si no hay, se muestra 'clientes' por defecto.
    // Esta lógica se mueve al inicio del DOMContentLoaded para que la sección activa sea siempre correcta.
    if (seccionFromUrl) {
        mostrarSeccion(seccionFromUrl);
    } else {
        mostrarSeccion('clientes'); 
    }

    // Función para mostrar mensajes dentro de un contenedor específico del modal
    function showModalMessage(messageContainer, message, type) {
        messageContainer.innerHTML = ''; // Limpiar mensajes anteriores
        const p = document.createElement('p');
        p.textContent = message;
        p.classList.add('modal-message', type); // Añadir clases para estilo (success/error)
        messageContainer.appendChild(p);
    }

    // Procesar mensajes al cargar la página (solo si hay parámetros de modal o éxito en la URL)
    if (modalCreateType || modalUpdateType || modalSuccessType) {
        const messagesDiv = document.querySelector('.messages'); // Busca el <ul> de Django messages en la página principal
        let djangoMessage = '';
        let messageType = '';

        if (messagesDiv) {
            const messageItem = messagesDiv.querySelector('li'); // Busca el <li> dentro del <ul>
            if (messageItem) {
                djangoMessage = messageItem.textContent; // Obtiene el texto del mensaje
                messageType = messageItem.classList.contains('error') ? 'error' : 'success'; // Determina el tipo de mensaje
                messagesDiv.style.display = 'none'; // Ocultar los mensajes de la página principal para evitar duplicidad
            }
        }

        // Si hay un mensaje de Django para mostrar
        if (djangoMessage) {
            // Lógica para reabrir modal de Creación (si es un error)
            if (modalCreateType && messageType === 'error') {
                const initialData = {};
                // Definir los campos que esperamos para cada tipo de formulario de creación
                const fieldsForType = { 
                    'cliente': ['nombre', 'apellido', 'telefono', 'username', 'email'],
                    'barbero': ['nombre', 'apellido', 'username', 'telefono', 'email', 'fecha_nacimiento', 'especialidad'],
                    'administrador': ['nombre', 'apellido', 'username', 'email'],
                    'producto': ['nombre', 'stock', 'precio', 'descripcion', 'tipo'], // <-- Agregado 'tipo'
                    'servicio': ['nombre', 'descripcion', 'duracion', 'precio', 'tipo'] // <-- Agregado 'tipo'
                };
                
                // Recopilar datos de la URL para pre-rellenar el formulario
                if (fieldsForType[modalCreateType]) {
                    fieldsForType[modalCreateType].forEach(field => {
                        const value = urlParams.get(field);
                        if (value !== null) {
                            initialData[field] = value;
                        }
                    });
                }
                
                // Abrir el modal de creación y rellenar el formulario con los datos recopilados
                openCreateModalWithForm(modalCreateType, initialData);
                
                // Obtener el formulario ya visible para mostrar el mensaje dentro de él
                const targetForm = document.getElementById(`form-${modalCreateType}`);
                if (targetForm) {
                    const messageContainer = targetForm.querySelector('.modal-messages');
                    if (messageContainer) {
                        showModalMessage(messageContainer, djangoMessage, messageType);
                    }
                }

            } 
            // Lógica para reabrir modal de Actualización (si es un error)
            else if (modalUpdateType && messageType === 'error') {
                const updateForm = document.getElementById(`form-update-${modalUpdateType}`);
                if (updateForm && itemIdToUpdate) {
                    const itemSeccionUpdate = urlParams.get('seccion');
                    const updateUrl = django_urls[`actualizar_${modalUpdateType}_url_base`].replace('0', itemIdToUpdate);
                    
                    fetch(`${updateUrl}`, { // Se hace un GET a la URL del API para obtener los datos del elemento a editar
                        headers: { 'X-Requested-With': 'XMLHttpRequest' }
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Poblar el formulario con los datos recibidos
                        if (updateForm.querySelector(`#update_${modalUpdateType}_id`)) updateForm.querySelector(`#update_${modalUpdateType}_id`).value = data.id;
                        if (data.nombre) updateForm.querySelector(`#update_${modalUpdateType}_nombre`).value = data.nombre;
                        if (data.apellido) updateForm.querySelector(`#update_${modalUpdateType}_apellido`).value = data.apellido;
                        if (data.username) updateForm.querySelector(`#update_${modalUpdateType}_username`).value = data.username;
                        if (data.email) updateForm.querySelector(`#update_${modalUpdateType}_email`).value = data.email;
                        if (data.telefono) updateForm.querySelector(`#update_${modalUpdateType}_telefono`).value = data.telefono;
                        
                        if (data.fecha_nacimiento && updateForm.querySelector(`#update_${modalUpdateType}_fecha_nacimiento`)) updateForm.querySelector(`#update_${modalUpdateType}_fecha_nacimiento`).value = data.fecha_nacimiento;
                        if (data.especialidad && updateForm.querySelector(`#update_${modalUpdateType}_especialidad`)) updateForm.querySelector(`#update_${modalUpdateType}_especialidad`).value = data.especialidad;
                        if (data.stock && updateForm.querySelector(`#update_${modalUpdateType}_stock`)) updateForm.querySelector(`#update_${modalUpdateType}_stock`).value = data.stock;
                        if (data.precio && updateForm.querySelector(`#update_${modalUpdateType}_precio`)) updateForm.querySelector(`#update_${modalUpdateType}_precio`).value = data.precio;
                        if (data.descripcion && updateForm.querySelector(`#update_${modalUpdateType}_descripcion`)) updateForm.querySelector(`#update_${modalUpdateType}_descripcion`).value = data.descripcion;
                        if (data.duracion) { 
                            const totalMinutes = parseInt(data.duracion, 10);
                            if (!isNaN(totalMinutes)) {
                                const hours = Math.floor(totalMinutes / 60).toString().padStart(2, '0');
                                const minutes = (totalMinutes % 60).toString().padStart(2, '0');
                                const durationTime = `${hours}:${minutes}`;
                                const durationInput = updateForm.querySelector(`#update_${modalUpdateType}_duracion`);
                                if (durationInput && durationInput.type === 'time') {
                                    durationInput.value = durationTime;
                                } else if (durationInput) {
                                    durationInput.value = totalMinutes;
                                }
                            }
                        }
                        if (data.tipo && updateForm.querySelector(`#update_${modalUpdateType}_tipo`)) updateForm.querySelector(`#update_${modalUpdateType}_tipo`).value = data.tipo; // Rellenar 'tipo' para actualización
                        
                        const currentPhotoElem = updateForm.querySelector(`#update_${modalUpdateType}_current_photo`);
                        if (currentPhotoElem && (data.foto_perfil_url || data.imagen_url)) {
                            currentPhotoElem.src = data.foto_perfil_url || data.imagen_url;
                            currentPhotoElem.style.display = 'block';
                        } else if (currentPhotoElem) {
                            currentPhotoElem.style.display = 'none';
                            currentPhotoElem.src = '';
                        }
                        const messageContainer = updateForm.querySelector('.modal-messages');
                        if (messageContainer) {
                            showModalMessage(messageContainer, djangoMessage, messageType);
                        }
                        updateForm.style.display = 'block'; // Asegura que el formulario esté visible
                        openModal(updateModal); // Abre el modal de actualización
                    })
                    .catch(error => {
                        console.error('Error al rellenar formulario de actualización tras error de Django:', error);
                        alert('No se pudieron cargar los datos del elemento para rellenar el formulario de actualización.');
                    });
                    return; // Salir después de iniciar el fetch
                } else {
                    console.error("No se pudo abrir el modal de actualización. itemId o formulario no encontrado.");
                }
            } 
            // Mensajes de éxito: No reabrimos el modal de formulario, solo ocultamos el mensaje principal
            else if (modalSuccessType) {
                console.log(`¡Éxito para ${modalSuccessType}! Mensaje: ${djangoMessage}`);
            }
        }
        
        // --- LIMPIAR LOS PARÁMETROS DE LA URL DESPUÉS DE PROCESARLOS ---
        // Esta línea es la clave para que la URL se quede limpia.
        // Construye una URL base con solo el protocolo, host y path, eliminando todos los parámetros de búsqueda.
        const cleanUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
        window.history.replaceState({}, document.title, cleanUrl); // Cambia la URL sin recargar la página.
    }

    // Lógica de inicialización al cargar la página (DOMContentLoaded)
    // Usamos la variable 'seccionFromUrl' ya declarada arriba.
    if (seccionFromUrl) {
        mostrarSeccion(seccionFromUrl);
    } else {
        mostrarSeccion('clientes'); 
    }

    // JavaScript para el dropdown del horario (si existe)
    const diaSelect = document.getElementById('dia-select');
    if (diaSelect) {
        diaSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            document.getElementById('hora_apertura').value = selectedOption.dataset.apertura;
            document.getElementById('hora_cierre').value = selectedOption.dataset.cierre;
        });
        diaSelect.dispatchEvent(new Event('change')); 
    }
});

// Ajuste del carrusel y menú al cambiar el tamaño de la ventana
// Ajustes al redimensionar la ventana (re-calcula carruseles y mantiene la sección visible)
window.addEventListener('resize', () => {
  /* ────────── Carruseles ────────── */
  const citasSection = document.getElementById('citas-section');
  if (citasSection && citasSection.style.display !== 'none') {
    ['carruselTrackHoy', 'carruselTrackManana', 'carruselTrackProximos']
      .forEach(inicializarCarrusel);   // vuelve a calcular posición/ancho
  }

  /* ────────── Sección activa ────────── */
  const currentActive = document.querySelector('.menu-item.active'); // ej.  <li id="menu-citas" …>
  if (currentActive) {
    const seccionId = currentActive.id.replace('menu-', ''); // "menu-citas" → "citas"
    mostrarSeccion(seccionId);                               // reaplica animación si hace falta
  }
});

