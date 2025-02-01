// static/js/script.js

document.getElementById('ubicacionForm').addEventListener('submit', function(event) {
    const nombreUbicacion = document.getElementById('nombre_ubicacion').value;
    const direccion = document.getElementById('direccion').value;
    const ciudad = document.getElementById('ciudad').value;
    const pais = document.getElementById('pais').value;

    // Validación básica (verificar si los campos están vacíos)
    if (!nombreUbicacion || !direccion || !ciudad || !pais) {
        event.preventDefault(); // Prevenir el envío del formulario
        alert('Por favor, complete todos los campos.');
    }
});
