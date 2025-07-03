function confirmarEliminacion(clienteId, clienteNombre) {
    document.getElementById('modal-nombre').innerText = clienteNombre;
    document.getElementById('form-eliminar').action = '/adminstrador/eliminar_cliente/' + clienteId + '/';
    document.getElementById('modal-eliminar').classList.add('active');
}
function cerrarModal() {
    document.getElementById('modal-eliminar').classList.remove('active');
}