// admin_citas.js – Versión corregida y robusta basada en barbero

const carruselPositions = {};

function mostrarSeccion(seccionId) {
    const secciones = ['citas', 'clientes', 'barberos', 'servicios', 'productos', 'calendario', 'historial'];

    secciones.forEach(id => {
        const section = document.getElementById(id + '-section');
        if (section) {
            section.style.display = 'none';
            section.classList.remove('fadeIn');
        }
    });

    document.querySelectorAll('.menu-item').forEach(item => item.classList.remove('active'));

    const mostrar = document.getElementById(seccionId + '-section');
    if (mostrar) {
        mostrar.style.display = 'block';
        void mostrar.offsetWidth;
        mostrar.classList.add('fadeIn');

        const menu = document.getElementById(`menu-${seccionId}`);
        if (menu) menu.classList.add('active');

        if (seccionId === 'citas') {
            setTimeout(() => {
                inicializarCarrusel('carruselTrackHoy');
                inicializarCarrusel('carruselTrackManana');
                inicializarCarrusel('carruselTrackProximos');
            }, 200);
        }
    }
}

function moverCarrusel(trackId, dir) {
    const track = document.getElementById(trackId);
    if (!track) return;

    const cards = track.querySelectorAll('.carrusel-card');
    const total = cards.length;
    if (typeof carruselPositions[trackId] === 'undefined') carruselPositions[trackId] = 0;

    if (total === 0) {
        track.style.transform = 'translateX(0px)';
        return;
    }

    const cardWidth = cards[0].offsetWidth;
    const gap = 32;
    const container = track.parentElement;
    const paddingLeft = parseFloat(getComputedStyle(container).paddingLeft);
    const paddingRight = parseFloat(getComputedStyle(container).paddingRight);
    const effectiveWidth = container.offsetWidth - paddingLeft - paddingRight;
    const visibleCards = Math.floor((effectiveWidth + gap) / (cardWidth + gap));

    if (dir !== 0) carruselPositions[trackId] += dir;

    if (carruselPositions[trackId] < 0) carruselPositions[trackId] = 0;
    if (total <= visibleCards) carruselPositions[trackId] = 0;
    else if (carruselPositions[trackId] > total - visibleCards)
        carruselPositions[trackId] = total - visibleCards;

    track.style.transform = `translateX(-${carruselPositions[trackId] * (cardWidth + gap)}px)`;
}

function inicializarCarrusel(trackId) {
    moverCarrusel(trackId, 0);
}

document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const seccionDesdeUrl = urlParams.get('seccion');
    mostrarSeccion(seccionDesdeUrl || 'citas');
});

window.addEventListener('resize', () => {
    const citasSection = document.getElementById('citas-section');
    if (citasSection && citasSection.style.display !== 'none') {
        inicializarCarrusel('carruselTrackHoy');
        inicializarCarrusel('carruselTrackManana');
        inicializarCarrusel('carruselTrackProximos');
    }

    const currentActive = document.querySelector('.menu-item.active');
    if (currentActive) {
        const id = currentActive.id.replace('menu-', '');
        mostrarSeccion(id);
    }
});
