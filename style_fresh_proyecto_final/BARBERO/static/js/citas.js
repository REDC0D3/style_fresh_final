// citas.js - Contiene la lógica del menú de secciones y la funcionalidad de múltiples carruseles para home_barbero.html

/**
 * Almacena la posición actual de cada carrusel por su ID de track.
 * Esto permite que cada carrusel tenga su propio estado de desplazamiento.
 */
const carruselPositions = {};

/**
 * Muestra una sección específica del contenido principal y actualiza el estado del menú.
 * @param {string} seccionId La parte del ID de la sección a mostrar (ej. 'citas', 'historial').
 * El ID completo en el HTML será 'citas-section', 'historial-section'.
 */
function mostrarSeccion(seccionId) {
    // Lista de todos los IDs base de las secciones del barbero.
    const seccionesBarbero = [
        'citas',
        'historial',
        'disenos', 
        'calificaciones' 
    ];

    // 1. Oculta todas las secciones de contenido
    seccionesBarbero.forEach(function(id) {
        const sectionElement = document.getElementById(id + '-section'); // Busca el ID completo
        if (sectionElement) {
            sectionElement.style.display = 'none';
            sectionElement.classList.remove('fadeIn'); 
        }
    });

    // 2. Remueve la clase 'active' de todos los items del menú
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
    });

    // 3. Muestra la sección deseada y añade la animación
    const seccionAMostrar = document.getElementById(seccionId + '-section'); // Busca el ID completo
    if (seccionAMostrar) {
        seccionAMostrar.style.display = 'block';
        void seccionAMostrar.offsetWidth; 
        seccionAMostrar.classList.add('fadeIn'); 

        // 4. Activa el elemento del menú correspondiente
        const menuItemActivo = document.getElementById(`menu-${seccionId}`);
        if (menuItemActivo) {
            menuItemActivo.classList.add('active'); 
        }

        // 5. Si la sección mostrada es 'citas', inicializa todos los carruseles que contiene
        if (seccionId === 'citas') {
            // Un pequeño retraso para asegurar que los elementos estén renderizados y tengan ancho
            setTimeout(() => {
                inicializarCarrusel('carruselTrackHoy');
                inicializarCarrusel('carruselTrackManana');
                inicializarCarrusel('carruselTrackProximos');
            }, 200); 
        }
    }
}

/**
 * Mueve un carrusel específico a la siguiente/anterior posición o recalcula la posición actual.
 * @param {string} trackId El ID del carrusel-track a mover (ej. 'carruselTrackHoy').
 * @param {number} dir La dirección del movimiento (-1 para anterior, 1 para siguiente, 0 para recalcular/inicializar).
 */
function moverCarrusel(trackId, dir) {
    const track = document.getElementById(trackId);
    if (!track) return; // Asegura que el track exista

    const cards = track.querySelectorAll('.carrusel-card');
    const total = cards.length;
    
    // Inicializa la posición si no existe para este carrusel
    if (typeof carruselPositions[trackId] === 'undefined') {
        carruselPositions[trackId] = 0;
    }

    if (total === 0) { // Si no hay tarjetas, asegura transform en 0 y sale.
        track.style.transform = `translateX(0px)`;
        return; 
    }
    
    const cardWidth = cards[0].offsetWidth; 
    const gap = 32; // Debe coincidir con el valor en citas.css

    const container = track.parentElement;
    const containerPaddingLeft = parseFloat(getComputedStyle(container).paddingLeft);
    const containerPaddingRight = parseFloat(getComputedStyle(container).paddingRight);
    const effectiveContainerWidth = container.offsetWidth - containerPaddingLeft - containerPaddingRight;

    const visibleCardsInView = Math.floor((effectiveContainerWidth + gap) / (cardWidth + gap));
    
    // Actualiza la posición si hay dirección
    if (dir !== 0) {
        carruselPositions[trackId] += dir;
    }

    // Limita la posición
    if (carruselPositions[trackId] < 0) {
        carruselPositions[trackId] = 0; 
    }
    
    if (total <= visibleCardsInView) { // Si todas las tarjetas caben, no hay desplazamiento
        carruselPositions[trackId] = 0; 
    } else if (carruselPositions[trackId] > total - visibleCardsInView) {
        carruselPositions[trackId] = total - visibleCardsInView;
    }
    
    // Aplica la transformación
    track.style.transform = `translateX(-${carruselPositions[trackId] * (cardWidth + gap)}px)`;
}

/**
 * Función auxiliar para inicializar un carrusel específico.
 * Llama a moverCarrusel con dir=0 para que recalcule y posicione.
 * @param {string} trackId El ID del carrusel-track a inicializar.
 */
function inicializarCarrusel(trackId) {
    moverCarrusel(trackId, 0);
}

// Inicialización al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const seccionDesdeUrl = urlParams.get('seccion');
    
    // Muestra la sección 'citas' por defecto si no se especifica ninguna en la URL.
    mostrarSeccion(seccionDesdeUrl || 'citas'); 
});

// Ajuste del carrusel y menú al cambiar el tamaño de la ventana
window.addEventListener('resize', () => {
    // Si la sección de citas está visible, reinicializa todos sus carruseles
    const citasSection = document.getElementById('citas-section'); // Busca la sección de citas
    if (citasSection && citasSection.style.display !== 'none') {
        inicializarCarrusel('carruselTrackHoy');
        inicializarCarrusel('carruselTrackManana');
        inicializarCarrusel('carruselTrackProximos');
    }
    // También reajusta la visibilidad de las secciones si se hizo un cambio de tamaño
    const currentActiveSectionId = document.querySelector('.menu-item.active')?.id.replace('menu-', '');
    if (currentActiveSectionId) {
        mostrarSeccion(currentActiveSectionId);
    }
});

// Lógica para los botones de orden en historial de cortes
document.addEventListener('DOMContentLoaded', function() {
    const ordenarHistorialBtns = document.querySelectorAll('.ordenar-historial-btn');
    ordenarHistorialBtns.forEach(button => {
        button.addEventListener('click', function() {
            const orden = this.dataset.orden;
            const currentUrl = new URL(window.location.href);
            currentUrl.searchParams.set('ordenar_historial', orden);
            currentUrl.searchParams.set('seccion', 'historial'); // Asegurar que se muestre la sección de historial
            
            // Mantiene el término de búsqueda si está presente, para que el orden funcione combinado con la búsqueda.
            const buscarHistorialQuery = currentUrl.searchParams.get('buscar_historial');
            if (buscarHistorialQuery) {
                currentUrl.searchParams.set('buscar_historial', buscarHistorialQuery);
            } else {
                currentUrl.searchParams.delete('buscar_historial'); // Si no hay búsqueda, lo elimina.
            }

            window.location.href = currentUrl.toString(); // Redirigir
        });
    });
});