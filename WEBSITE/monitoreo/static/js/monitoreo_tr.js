document.addEventListener("DOMContentLoaded", function() {
    asignarEventosBotones();
    configurarFiltrosDesplegables();
    function toggleFiltro(id) {
        let filtro = document.getElementById(id);
        filtro.style.display = (filtro.style.display === "none" || filtro.style.display === "") ? "block" : "none";
    }
});

/* 🔹 Mostrar/Ocultar filtros desplegables */
function configurarFiltrosDesplegables() {
    document.querySelectorAll(".toggle-btn").forEach(button => {
        button.addEventListener("click", function() {
            let contenido = this.nextElementSibling;
            contenido.style.display = contenido.style.display === "none" || contenido.style.display === "" ? "block" : "none";
            this.innerText = contenido.style.display === "block" ? "🔼 Ocultar Filtros" : "🔽 Mostrar Filtros";
        });
    });
}

/* 🔹 Cargar inventario basado en filtros seleccionados */
function cargarInventario() {
    // Obtener los valores seleccionados para cada filtro
    let ubicaciones = [...document.querySelectorAll("input[name='ubicacion']:checked")].map(input => input.value);
    let tipos = [...document.querySelectorAll("input[name='tipo']:checked")].map(input => input.value);
    let marcas = [...document.querySelectorAll("input[name='marca']:checked")].map(input => input.value);
    let sistemas = [...document.querySelectorAll("input[name='sistema']:checked")].map(input => input.value);

    // Construir la URL con los filtros seleccionados
    let url = "/monitoreo/inventario/?";
    
    // Añadir cada filtro a la URL si tiene elementos seleccionados
    if (ubicaciones.length) url += `ubicacion[]=${ubicaciones.join("&ubicacion[]=")}&`;
    if (tipos.length) url += `tipo[]=${tipos.join("&tipo[]=")}&`;
    if (marcas.length) url += `marca[]=${marcas.join("&marca[]=")}&`;
    if (sistemas.length) url += `sistema[]=${sistemas.join("&sistema[]=")}&`;

    // Eliminar el último '&' si existe
    if (url.endsWith('&')) {
        url = url.slice(0, -1);
    }

    console.log("🔍 URL generada:", url);  // Verifica en la consola del navegador

    // Hacer la petición con los filtros aplicados
    fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(response => response.json())
        .then(data => actualizarTabla(data))  // Pasar los datos a la función que actualiza la tabla
        .catch(error => console.error("⚠ Error al cargar inventario:", error));
}


function buscarPorIP() {
    // Obtener los valores de los campos de la IP
    let ip1 = document.getElementById('ip1').value;
    let ip2 = document.getElementById('ip2').value;
    let ip3 = document.getElementById('ip3').value;
    let ip4 = document.getElementById('ip4').value;

    // Verifica si los campos están vacíos
    if (!ip1 || !ip2 || !ip3 || !ip4) {
        alert("⚠ Todos los campos de IP deben ser completados.");
        return;
    }

    // Generar la IP concatenando los valores
    let ip = `${ip1}.${ip2}.${ip3}.${ip4}`;
    
    console.log("IP generada:", ip);  // Verifica si la IP se genera correctamente

    // Validar la IP
    if (!validarIPv4(ip)) {
        alert("⚠ IP inválida. Verifique los valores ingresados.");
        return;
    }

    // Crear la URL para la solicitud con la IP
    let url = `/monitoreo/inventario/?ip=${encodeURIComponent(ip)}`;
    
    console.log("🔍 URL generada:", url);  // Verifica que la URL es correcta

    // Realizar la solicitud
    fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(response => response.json())
        .then(data => actualizarTabla(data))
        .catch(error => console.error("⚠ Error al buscar IP:", error));
}

// 🔹 Función para validar IP
function validarIPv4(ip) {
    let partes = ip.split('.');
    return partes.length === 4 && partes.every(num => num !== "" && !isNaN(num) && parseInt(num) >= 0 && parseInt(num) <= 255);
}

/* 🔹 Actualizar la tabla con nuevos datos */
function actualizarTabla(data) {
    console.log(data); // Verifica cómo están llegando los datos

    let tabla = document.getElementById("inventario-body");
    if (!tabla) {
        console.error("⚠ Error: No se encontró el elemento #inventario-body en el DOM.");
        return;
    }

    tabla.innerHTML = ""; // Limpiar la tabla antes de actualizar

    if (data.length === 0) {
        tabla.innerHTML = `<tr><td colspan="6">No hay elementos en el inventario.</td></tr>`;
        return;
    }

    data.forEach(item => {
        console.log(item); // Verifica cómo está estructurado cada 'item'

        let fila = document.createElement("tr");

        fila.innerHTML = `
            <td>${item.ubicacion || "No disponible"}</td>
            <td>${item.ip || "No disponible"}</td>
            <td>${item.tipo_elemento || "No especificado"}</td>
            <td id="estado-${item.id_inventario}">⏳ Esperando...</td>
            <td><button class="btn-ping" data-ip="${item.ip}" data-id="${item.id_inventario}">Verificar Estado</button></td>
            <td><button class="btn-detalles"
                data-id="${item.id_inventario}"
                data-nombre="${item.nombre || 'No disponible'}"
                data-ubicacion="${item.ubicacion || 'No disponible'}"
                data-ip="${item.ip || 'No disponible'}"
                data-tipo="${item.tipo_elemento || 'No especificado'}"
                data-estado="${item.estado || 'Desconocido'}"
                data-fecha="${item.fecha_adquisicion || 'No disponible'}">
                Ver Detalles
            </button></td>
        `;

        tabla.appendChild(fila);
    });

    asignarEventosBotones(
        document.querySelectorAll(".btn-detalles").forEach(button => {
            button.addEventListener("click", function () {
                const id = this.dataset.id;
                if (id) {
                    window.location.href = `/monitoreo/detalle_dispositivo/${id}/`;
                } else {
                    alert("⚠ No se encontró el ID del dispositivo.");
                }
            });
        })
    ); // Asegúrate de volver a asignar los eventos después de actualizar la tabla
}

/* 🔹 Asignar eventos a los botones después de actualizar la tabla */
function asignarEventosBotones() {
    document.querySelectorAll(".btn-ping").forEach(button => {
        button.addEventListener("click", function() {
            verificarEstado(this.dataset.ip, this.dataset.id);
        });
    });

    document.querySelectorAll(".btn-detalles").forEach(button => {
        button.addEventListener("click", function() {
            mostrarDetalles(
                this.dataset.id,
                this.dataset.nombre,
                this.dataset.ubicacion,
                this.dataset.ip,
                this.dataset.tipo,
                this.dataset.marca,
                this.dataset.sistema,
                this.dataset.estado,
                this.dataset.fecha
            );
        });
    });
}

/* 🔹 Verificar el estado de todos los dispositivos con IP */
function verificarTodos() {
    let botones = document.querySelectorAll(".btn-ping");
    if (botones.length === 0) {
        alert("No hay dispositivos para verificar.");
        return;
    }

    botones.forEach(button => {
        let ip = button.dataset.ip;
        let id = button.dataset.id;
        if (ip && id) {
            verificarEstado(ip, id);
        }
    });
}

/* 🔹 Verificar el estado de un solo dispositivo */
function verificarEstado(ip, id) {
    if (!ip) {
        document.getElementById(`estado-${id}`).innerText = "⚠ IP no válida";
        return;
    }

    fetch(`/monitoreo/verificar_estado/?ip=${encodeURIComponent(ip)}`)
        .then(response => response.json())
        .then(data => {
            let estado = document.getElementById(`estado-${id}`);
            estado.innerText = data.estado === "exito" ? `✅ Activo (${data.tiempo})` : `❌ Inactivo (No responde)`;
        })
        .catch(error => {
            console.error("Error al hacer ping:", error);
            document.getElementById(`estado-${id}`).innerText = "⚠ Error en la consulta";
        });
}

/* 🔹 Mostrar detalles del dispositivo en un modal */
function mostrarDetalles(id, nombre, ubicacion, ip, tipo, marca, sistema, estado, fecha) {
    let detalles = `
        <p><strong>ID:</strong> ${id}</p>
        <p><strong>Nombre:</strong> ${nombre}</p>
        <p><strong>Ubicación:</strong> ${ubicacion}</p>
        <p><strong>IP:</strong> ${ip || 'No disponible'}</p>
        <p><strong>Tipo:</strong> ${tipo}</p>
        <p><strong>Marca:</strong> ${marca}</p>
        <p><strong>Sistema Operativo:</strong> ${sistema}</p>
        <p><strong>Estado:</strong> ${estado}</p>
        <p><strong>Fecha de Adquisición:</strong> ${fecha || 'No disponible'}</p>
    `;
    document.getElementById("detalles-dispositivo").innerHTML = detalles;
    document.getElementById("modal").style.display = "block";
}

/* 🔹 Cerrar modal */
function cerrarModal() {
    document.getElementById("modal").style.display = "none";
}

/* 🔹 Eliminar filtros sin recargar */
function eliminarFiltros() {
    document.querySelectorAll("input, select").forEach(input => {
        if (input.type === "checkbox") input.checked = false;
        else input.value = "";
    });
}

// 🔹 Mueve automáticamente el cursor al siguiente campo al escribir 3 dígitos
function moverCursor(input, siguiente) {
    if (input.value.length === 3) {
        document.getElementById(siguiente).focus();
    }
}

// 🔹 Solo permite números del 0 al 9 en los campos de la IP
function soloNumeros(event) {
    let char = String.fromCharCode(event.which);
    if (!/^[0-9]$/.test(char)) {
        event.preventDefault();
    }
}

// 🔹 Valida si la IP ingresada es correcta (cada número entre 0 y 255)
function validarIPv4(ip) {
    let partes = ip.split('.');
    return partes.length === 4 && partes.every(num => num !== "" && !isNaN(num) && parseInt(num) >= 0 && parseInt(num) <= 255);
}

// ✅ Función para mostrar/ocultar las tarjetas desplegables
function toggleFiltro(id) {
    let contenido = document.getElementById(id);
    contenido.classList.toggle('mostrar');
}

function toggleDropdown(id) {
    document.getElementById(id).classList.toggle("show");
}

window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        let dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
            let openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

function moverCursor(input, nextInputId) {
    if (input.value.length === input.maxLength) {
        document.getElementById(nextInputId).focus();
    }
}

function soloNumeros(event) {
    let char = String.fromCharCode(event.which);
    if (!/[0-9]/.test(char)) {
        event.preventDefault();
    }
}



window.toggleFiltro = toggleFiltro;
window.moverCursor = moverCursor;
window.soloNumeros = soloNumeros;
window.buscarPorIP = buscarPorIP;
window.verificarTodos = verificarTodos;
window.eliminarFiltros = eliminarFiltros;
