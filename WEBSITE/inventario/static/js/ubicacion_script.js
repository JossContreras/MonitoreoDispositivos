// Llamar a la API mediante su puerta de enlace
fetch('http://127.0.0.1:8000/api/ubicaciones/')
    .then(response => response.json())
    .then(data => {
        // Obtener el contenedor de la lista
        const listContainer = document.getElementById('ubicaciones-list');
        
        // Si no hay datos, mostrar un mensaje
        if (data.length === 0) {
            listContainer.innerHTML = '<li class="item">No hay ubicaciones disponibles.</li>';
        } else {
            // Mostrar cada ubicación en la lista definiendo los datos a mostrar
            data.forEach(ubicacion => {
                const listItem = document.createElement('li');
                listItem.className = 'item';
                listItem.textContent = `${ubicacion.nombre_ubicacion} - ${ubicacion.ciudad}, ${ubicacion.pais}`;
                listContainer.appendChild(listItem);
            });
        }
    })
    .catch(error => {
        console.error('Error al obtener las ubicaciones:', error);
    });
