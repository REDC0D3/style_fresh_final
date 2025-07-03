// citas.js - Contiene solo la lógica de los carruseles de citas.

/**
 * Almacena la posición actual de cada carrusel por su ID de track.
 * Esto permite que cada carrusel tenga su propio estado de desplazamiento.
 */
const carruselPositions = {};

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
 * Esta función será llamada desde el script incrustado en home_admin.html.
 * @param {string} trackId El ID del carrusel-track a inicializar.
 */
function inicializarCarrusel(trackId) {
    moverCarrusel(trackId, 0);
}

// **NOTA:** Este archivo NO contiene DOMContentLoaded o window.onload directos.
// La inicialización de los carruseles se manejará desde el script incrustado en home_admin.html
// a través de llamadas a `inicializarCarrusel()` cuando la sección de citas sea visible.
// La lógica de `window.addEventListener('resize')` también se maneja desde el script incrustado.