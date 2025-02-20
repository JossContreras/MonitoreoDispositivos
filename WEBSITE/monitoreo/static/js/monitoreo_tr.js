document.addEventListener("DOMContentLoaded", function() {
    asignarEventosBotones(); // ✅ Asigna eventos al cargar la página
});

function cargarInventario() {
    let ubicaciones = [...document.getElementById("ubicacion").selectedOptions].map(opt => opt.value);
    let ipBusqueda = document.getElementById("buscar-ip").value.trim();
    let tipos = [...document.querySelectorAll("input[name='tipo']:checked")].map(input => input.value);
    let marcas = [...document.querySelectorAll("input[name='marca']:checked")].map(input => input.value);
    let sistemas = [...document.querySelectorAll("input[name='sistema']:checked")].map(input => input.value);

    let url = "/monitoreo/inventario/?";
    if (ipBusqueda) url += `ip=${encodeURIComponent(ipBusqueda)}`;
    if (ubicaciones.length) url += `&ubicacion[]=${ubicaciones.join("&ubicacion[]=")}`;
    if (tipos.length) url += `&tipo[]=${tipos.join("&tipo[]=")}`;
    if (marcas.length) url += `&marca[]=${marcas.join("&marca[]=")}`;
    if (sistemas.length) url += `&sistema[]=${sistemas.join("&sistema[]=")}`;

    fetch(url, {
        headers: { "X-Requested-With": "XMLHttpRequest" }
    })
    .then(response => response.json())
    .then(data => actualizarTabla(data))
    .catch(error => console.error("Error al cargar inventario:", error));
}

function actualizarTabla(data) {
    let tabla = document.getElementById("inventario-body");
    tabla.innerHTML = "";
    if (data.length === 0) {
        tabla.innerHTML = `<tr><td colspan="10">No hay elementos en el inventario.</td></tr>`;
        return;
    }

    data.forEach(item => {
        let fila = `<tr>
            <td>${item.id_inventario}</td>
            <td>${item.nombre}</td>
            <td>${item.ubicacion}</td>
            <td>${item.ip}</td>
            <td>${item.tipo_elemento || "No especificado"}</td>
            <td>${item.marca || "No disponible"}</td>
            <td>${item.sistema_operativo || "No disponible"}</td>
            <td id="estado-${item.id_inventario}">⏳ Esperando...</td>
            <td><button class="btn-ping" data-ip="${item.ip}" data-id="${item.id_inventario}">Verificar Estado</button></td>
            <td><button class="btn-detalles"
                data-id="${item.id_inventario}"
                data-nombre="${item.nombre}"
                data-ubicacion="${item.ubicacion}"
                data-ip="${item.ip || 'No disponible'}"
                data-tipo="${item.tipo_elemento || 'No especificado'}"
                data-marca="${item.marca || 'No disponible'}"
                data-sistema="${item.sistema_operativo || 'No disponible'}"
                data-estado="${item.estado || 'Desconocido'}"
                data-fecha="${item.fecha_adquisicion || 'No disponible'}">
                Ver Detalles
            </button></td>
        </tr>`;

        tabla.innerHTML += fila;
    });

    asignarEventosBotones(); // ✅ Asigna eventos después de actualizar la tabla
}

function asignarEventosBotones() {
    // 🟢 Asignar eventos a "Verificar Estado"
    document.querySelectorAll(".btn-ping").forEach(button => {
        button.addEventListener("click", function() {
            verificarEstado(this.dataset.ip, this.dataset.id);
        });
    });

    // 🟢 Asignar eventos a "Ver Detalles"
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

function verificarEstado(ip, id) {
    if (!ip) {
        document.getElementById(`estado-${id}`).innerText = "⚠ Error: IP no válida";
        return;
    }

    fetch(`/monitoreo/verificar_estado/?ip=${encodeURIComponent(ip)}`)
        .then(response => response.json())
        .then(data => {
            let estado = document.getElementById(`estado-${id}`);
            if (data.estado === "exito") {
                estado.innerText = `✅ Activo (${data.tiempo})`;
            } else {
                let mensajeError = data.motivo;

                // 🔹 Acortar mensaje de error
                if (mensajeError.includes("Host de destino inaccesible")) {
                    mensajeError = "Host inaccesible";
                } else if (mensajeError.includes("100% perdidos")) {
                    mensajeError = "100% pérdida";
                } else {
                    mensajeError = "No responde";
                }

                estado.innerText = `❌ Inactivo (${mensajeError})`;
            }
        })
        .catch(error => {
            console.error("Error al hacer ping:", error);
            document.getElementById(`estado-${id}`).innerText = "⚠ Error en la consulta";
        });
}

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

function cerrarModal() {
    document.getElementById("modal").style.display = "none";
}

function eliminarFiltros() {
    // 🔹 Deseleccionar todas las opciones en "Ubicación"
    let ubicacionSelect = document.getElementById("ubicacion");
    for (let option of ubicacionSelect.options) {
        option.selected = false;
    }

    // 🔹 Desmarcar todas las casillas de verificación (tipo, marca, sistema operativo)
    document.querySelectorAll("input[name='tipo']:checked").forEach(input => input.checked = false);
    document.querySelectorAll("input[name='marca']:checked").forEach(input => input.checked = false);
    document.querySelectorAll("input[name='sistema']:checked").forEach(input => input.checked = false);

    // 🔹 Vaciar el campo de búsqueda de IP
    document.getElementById("buscar-ip").value = "";

    // ✅ No llamamos a cargarInventario() automáticamente, solo limpiamos los campos
    console.log("Filtros limpiados. Esperando acción del usuario.");
}
