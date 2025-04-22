document.addEventListener('DOMContentLoaded', function() {
    // Variables globales
    let ordenes = [];
    let ordenesFiltered = [];
    const itemsPorPagina = 10;
    let paginaActual = 1;

    // Elementos del DOM
    const searchInput = document.getElementById('searchInput');
    const estadoFilter = document.getElementById('estadoFilter');
    const fechaDesde = document.getElementById('fechaDesde');
    const fechaHasta = document.getElementById('fechaHasta');
    const btnAplicarFiltros = document.getElementById('aplicarFiltros');
    const btnLimpiarFiltros = document.getElementById('limpiarFiltros');
    const btnPrevPage = document.getElementById('prevPage');
    const btnNextPage = document.getElementById('nextPage');
    const spanPaginaActual = document.getElementById('paginaActual');

    // Elementos de estadísticas
    const totalOrdenesElement = document.getElementById('totalOrdenes');
    const ordenesPendientesElement = document.getElementById('ordenesPendientes');
    const ordenesEnRevisionElement = document.getElementById('ordenesEnRevision');
    const ordenesReparadasElement = document.getElementById('ordenesReparadas');
    const ordenesNoReparadasElement = document.getElementById('ordenesNoReparadas');

    // Event Listeners
    searchInput.addEventListener('input', aplicarFiltros);
    estadoFilter.addEventListener('change', aplicarFiltros);
    fechaDesde.addEventListener('change', aplicarFiltros);
    fechaHasta.addEventListener('change', aplicarFiltros);
    btnAplicarFiltros.addEventListener('click', aplicarFiltros);
    btnLimpiarFiltros.addEventListener('click', limpiarFiltros);
    btnPrevPage.addEventListener('click', () => cambiarPagina(paginaActual - 1));
    btnNextPage.addEventListener('click', () => cambiarPagina(paginaActual + 1));

    // Cargar datos iniciales
    cargarOrdenes();

    function cargarOrdenes() {
        fetch('/api/ordenes_servicio')
            .then(response => response.json())
            .then(data => {
                ordenes = data;
                ordenesFiltered = [...ordenes];
                actualizarEstadisticas(ordenes);
                aplicarFiltros();
            })
            .catch(error => {
                console.error('Error al obtener los datos:', error);
                mostrarError('Error al cargar los datos: ' + error.message);
            });
    }

    function actualizarEstadisticas(ordenes) {
        const stats = {
            total: ordenes.length,
            pendientes: 0,
            enRevision: 0,
            reparadas: 0,
            noReparadas: 0
        };

        ordenes.forEach(orden => {
            switch(orden.estado) {
                case 'Pendiente por revision':
                    stats.pendientes++;
                    break;
                case 'En Revision':
                    stats.enRevision++;
                    break;
                case 'REPARADO':
                    stats.reparadas++;
                    break;
                case 'NO REPARADO':
                    stats.noReparadas++;
                    break;
            }
        });

        // Actualizar elementos del DOM
        totalOrdenesElement.textContent = stats.total;
        ordenesPendientesElement.textContent = stats.pendientes;
        ordenesEnRevisionElement.textContent = stats.enRevision;
        ordenesReparadasElement.textContent = stats.reparadas;
        ordenesNoReparadasElement.textContent = stats.noReparadas;

        // Animar los números
        animarContador(totalOrdenesElement);
        animarContador(ordenesPendientesElement);
        animarContador(ordenesEnRevisionElement);
        animarContador(ordenesReparadasElement);
        animarContador(ordenesNoReparadasElement);
    }

    function animarContador(elemento) {
        const valor = parseInt(elemento.textContent);
        let actual = 0;
        const duracion = 1000; // 1 segundo
        const pasos = 20;
        const incremento = valor / pasos;
        const intervalo = duracion / pasos;

        const animacion = setInterval(() => {
            actual += incremento;
            if (actual >= valor) {
                elemento.textContent = valor;
                clearInterval(animacion);
            } else {
                elemento.textContent = Math.floor(actual);
            }
        }, intervalo);
    }

    function aplicarFiltros() {
        const searchTerm = searchInput.value.toLowerCase();
        const estadoSeleccionado = estadoFilter.value;
        const fechaDesdeVal = fechaDesde.value ? new Date(fechaDesde.value) : null;
        const fechaHastaVal = fechaHasta.value ? new Date(fechaHasta.value + 'T23:59:59') : null;

        ordenesFiltered = ordenes.filter(orden => {
            // Búsqueda por texto
            const cumpleBusqueda = !searchTerm || 
                Object.values(orden).some(value => 
                    String(value).toLowerCase().includes(searchTerm)
                );

            // Filtro por estado
            const cumpleEstado = !estadoSeleccionado || 
                orden.estado === estadoSeleccionado;

            // Filtro por fecha
            const fechaOrden = new Date(orden.fecha_entrada);
            const cumpleFechaDesde = !fechaDesdeVal || fechaOrden >= fechaDesdeVal;
            const cumpleFechaHasta = !fechaHastaVal || fechaOrden <= fechaHastaVal;

            return cumpleBusqueda && cumpleEstado && cumpleFechaDesde && cumpleFechaHasta;
        });

        paginaActual = 1;
        actualizarTabla();
        actualizarEstadisticas(ordenesFiltered);
    }

    function limpiarFiltros() {
        searchInput.value = '';
        estadoFilter.value = '';
        fechaDesde.value = '';
        fechaHasta.value = '';
        ordenesFiltered = [...ordenes];
        paginaActual = 1;
        actualizarTabla();
        actualizarEstadisticas(ordenes);
    }

    function actualizarTabla() {
        const inicio = (paginaActual - 1) * itemsPorPagina;
        const fin = inicio + itemsPorPagina;
        const ordenesActuales = ordenesFiltered.slice(inicio, fin);

        const tbody = document.querySelector('#ordenesServicioTable tbody');
        
        if (ordenesActuales.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="11" class="text-center">No se encontraron órdenes que coincidan con los filtros</td>
                </tr>
            `;
        } else {
            tbody.innerHTML = ordenesActuales.map(orden => `
                <tr>
                    <td>${orden.idordenes_servicio}</td>
                    <td>${orden.id_cliente}</td>
                    <td>${formatearFecha(orden.fecha_entrada)}</td>
                    <td>${formatearFecha(orden.inicio_trabajo)}</td>
                    <td>${formatearFecha(orden.fin_trabajo)}</td>
                    <td class="tiempo">${formatearTiempo(orden.tiempo_trabajo)}</td>
                    <td>${formatearEstado(orden.estado)}</td>
                    <td>${orden.diag_final || '-'}</td>
                    <td>${orden.marca || '-'}</td>
                    <td>${orden.modelo || '-'}</td>
                    <td>${orden.serial || '-'}</td>
                </tr>
            `).join('');
        }

        actualizarPaginacion();
    }

    function actualizarPaginacion() {
        const totalPaginas = Math.ceil(ordenesFiltered.length / itemsPorPagina);
        btnPrevPage.disabled = paginaActual <= 1;
        btnNextPage.disabled = paginaActual >= totalPaginas;
        spanPaginaActual.textContent = `Página ${paginaActual} de ${totalPaginas}`;
    }

    function cambiarPagina(nuevaPagina) {
        const totalPaginas = Math.ceil(ordenesFiltered.length / itemsPorPagina);
        if (nuevaPagina >= 1 && nuevaPagina <= totalPaginas) {
            paginaActual = nuevaPagina;
            actualizarTabla();
        }
    }

    function formatearFecha(fecha) {
        if (!fecha) return '-';
        return new Date(fecha).toLocaleString('es-CO', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    function formatearTiempo(minutos) {
        if (!minutos || minutos === 0) return '-';
        const horas = Math.floor(minutos / 60);
        const mins = minutos % 60;
        return `${horas}h ${mins}m`;
    }

    function formatearEstado(estado) {
        if (!estado) return '-';
        
        const claseEstado = {
            'Pendiente por revision': 'estado-pendiente',
            'En Revision': 'estado-revision',
            'REPARADO': 'estado-reparado',
            'NO REPARADO': 'estado-no-reparado'
        }[estado] || '';

        return `<span class="estado ${claseEstado}">${estado}</span>`;
    }

    function mostrarError(mensaje) {
        document.querySelector('#ordenesServicioTable tbody').innerHTML = `
            <tr>
                <td colspan="11" class="text-center">${mensaje}</td>
            </tr>
        `;
    }
});
