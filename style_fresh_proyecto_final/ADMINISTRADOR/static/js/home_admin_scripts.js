document.addEventListener('DOMContentLoaded', function() {
    // ... (otras variables y listeners) ...

    eliminarItemBtns.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // <-- Crucial: prevents the link from navigating immediately

            // ... (obtención de datos de item) ...

            // Construye la URL de acción del formulario dinámicamente
            let targetUrl = urlMap[itemTipo];
            if (targetUrl) {
                formEliminar.action = targetUrl.replace('{id}', itemId);
            } else {
                console.error('Tipo de ítem no reconocido para eliminación:', itemTipo);
                return;
            }
            
            modal.style.display = 'flex'; // <-- Esto es lo que muestra el modal. ¡CORREGIDO A 'flex'!
        });
    });

    // Evento para cerrar el modal al hacer clic en 'Cancelar'
    cancelarBtn.addEventListener('click', function() {
        modal.style.display = 'none'; // <-- Esto es lo que oculta el modal
    });

    // Evento para cerrar el modal al hacer clic en el botón 'X'
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none'; // <-- Esto es lo que oculta el modal
    });

    // Evento para cerrar el modal si se hace clic fuera del contenido
    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = 'none'; // <-- Esto es lo que oculta el modal
        }
    });
});