document.addEventListener('DOMContentLoaded', function() {
    // Variables globales
    let ordenes = [];
    let ordenesFiltered = [];
    const itemsPorPagina = 10;
    let paginaActual = 1;
    let ordenesPorPagina = 10;
    let filtros = {
        estado: '',
        fechaDesde: '',
        fechaHasta: '',
        busqueda: ''
    };

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
    const logoutLink = document.querySelector('a[href*="logout"]');

    // Manejar el logout
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = this.href;
        });
    }

    // Elementos de estadísticas
    const totalOrdenesElement = document.getElementById('totalOrdenes');
    const ordenesPendientesElement = document.getElementById('ordenesPendientes');
    const ordenesEnRevisionElement = document.getElementById('ordenesEnRevision');
    const ordenesReparadasElement = document.getElementById('ordenesReparadas');
    const ordenesNoReparadasElement = document.getElementById('ordenesNoReparadas');

    // Elementos del modal de tickets
    const ticketsModal = $('#ticketsModal');
    const ticketsList = document.getElementById('ticketsList');
    const nuevoTicketBtn = document.getElementById('nuevoTicketBtn');
    const nuevoTicketForm = document.getElementById('nuevoTicketForm');
    const ticketForm = document.getElementById('ticketForm');
    const cancelarTicketBtn = document.getElementById('cancelarTicketBtn');
    const departamentoSelect = document.getElementById('departamento');

    // Event Listeners
    searchInput.addEventListener('input', (e) => {
        filtros.busqueda = e.target.value;
        paginaActual = 1;
        cargarOrdenes();
    });
    estadoFilter.addEventListener('change', (e) => {
        filtros.estado = e.target.value;
        paginaActual = 1;
        cargarOrdenes();
    });
    fechaDesde.addEventListener('change', (e) => {
        filtros.fechaDesde = e.target.value;
        paginaActual = 1;
        cargarOrdenes();
    });
    fechaHasta.addEventListener('change', (e) => {
        filtros.fechaHasta = e.target.value;
        paginaActual = 1;
        cargarOrdenes();
    });
    btnAplicarFiltros.addEventListener('click', () => {
        paginaActual = 1;
        cargarOrdenes();
    });
    btnLimpiarFiltros.addEventListener('click', () => {
        searchInput.value = '';
        estadoFilter.value = '';
        fechaDesde.value = '';
        fechaHasta.value = '';
        filtros = {
            estado: '',
            fechaDesde: '',
            fechaHasta: '',
            busqueda: ''
        };
        paginaActual = 1;
        cargarOrdenes();
    });
    btnPrevPage.addEventListener('click', () => {
        if (paginaActual > 1) {
            paginaActual--;
            cargarOrdenes();
        }
    });
    btnNextPage.addEventListener('click', () => {
        paginaActual++;
        cargarOrdenes();
    });

    // Eventos del modal de tickets
    nuevoTicketBtn.addEventListener('click', () => {
        nuevoTicketForm.style.display = 'block';
        ticketsList.style.display = 'none';
    });
    cancelarTicketBtn.addEventListener('click', () => {
        nuevoTicketForm.style.display = 'none';
        ticketsList.style.display = 'block';
        ticketForm.reset();
    });
    ticketForm.addEventListener('submit', (e) => {
        e.preventDefault();
        crearTicket();
    });

    // Cargar datos iniciales
    cargarOrdenes();
    cargarDepartamentos();

    function cargarOrdenes() {
        fetch('/api/ordenes_servicio', {
            credentials: 'include'  // Incluir cookies en la petición
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la respuesta del servidor');
                }
                return response.json();
            })
            .then(data => {
                console.log('Datos recibidos:', data); // Debug
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
        console.log('Actualizando estadísticas con:', ordenes.length, 'órdenes'); // Debug
        const stats = {
            total: ordenes.length,
            pendientes: 0,
            enRevision: 0,
            reparadas: 0,
            noReparadas: 0
        };

        ordenes.forEach(orden => {
            const estado = orden.estado ? orden.estado.toUpperCase() : '';
            console.log('Procesando orden con estado:', estado); // Debug
            
            if (estado === 'PENDIENTE') {
                stats.pendientes++;
            } else if (estado === 'EN REVISION') {
                stats.enRevision++;
            } else if (estado === 'REPARADO') {
                stats.reparadas++;
            } else if (estado === 'NO REPARADO') {
                stats.noReparadas++;
            }
        });

        console.log('Estadísticas calculadas:', stats); // Debug

        // Actualizar elementos del DOM
        totalOrdenesElement.textContent = stats.total;
        ordenesPendientesElement.textContent = stats.pendientes;
        ordenesEnRevisionElement.textContent = stats.enRevision;
        ordenesReparadasElement.textContent = stats.reparadas;
        ordenesNoReparadasElement.textContent = stats.noReparadas;
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
                (orden.estado && orden.estado.toUpperCase() === estadoSeleccionado.toUpperCase());

            // Filtro por fecha
            const fechaOrden = orden.fecha_entrada ? new Date(orden.fecha_entrada) : null;
            const cumpleFechaDesde = !fechaDesdeVal || (fechaOrden && fechaOrden >= fechaDesdeVal);
            const cumpleFechaHasta = !fechaHastaVal || (fechaOrden && fechaOrden <= fechaHastaVal);

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
                    <td>${orden.idordenes_servicio || '-'}</td>
                    <td>${orden.id_cliente || '-'}</td>
                    <td>${formatearFecha(orden.fecha_entrada)}</td>
                    <td>${formatearFecha(orden.inicio_trabajo)}</td>
                    <td>${formatearFecha(orden.fin_trabajo)}</td>
                    <td class="tiempo">${formatearTiempo(orden.tiempo_trabajo)}</td>
                    <td>${formatearEstado(orden.estado)}</td>
                    <td>${orden.diag_final || '-'}</td>
                    <td>${orden.marca || '-'}</td>
                    <td>${orden.modelo || '-'}</td>
                    <td>${orden.serial || '-'}</td>
                    <td>
                        <button class="btn btn-sm btn-info" onclick="mostrarTickets(${orden.idordenes_servicio})">
                            <i class="fas fa-ticket-alt"></i> Tickets
                        </button>
                    </td>
                    <td>
                        <button class="btn btn-sm btn-primary" onclick="editarOrden(${orden.idordenes_servicio})">
                            <i class="fas fa-edit"></i>
                        </button>
                    </td>
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
        estado = estado.toUpperCase();
        
        let claseEstado = '';
        if (estado === 'PENDIENTE') {
            claseEstado = 'estado-pendiente';
        } else if (estado === 'EN REVISION') {
            claseEstado = 'estado-revision';
        } else if (estado === 'REPARADO') {
            claseEstado = 'estado-reparado';
        } else if (estado === 'NO REPARADO') {
            claseEstado = 'estado-no-reparado';
        }

        return `<span class="estado ${claseEstado}">${estado}</span>`;
    }

    function mostrarError(mensaje) {
        document.querySelector('#ordenesServicioTable tbody').innerHTML = `
            <tr>
                <td colspan="11" class="text-center text-danger">${mensaje}</td>
            </tr>
        `;
    }

    // Funciones de tickets
    async function mostrarTickets(ordenId) {
        try {
            document.getElementById('ordenId').value = ordenId;
            const response = await fetch(`/api/ordenes/${ordenId}/tickets`);
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            ticketsList.innerHTML = '';
            if (data.tickets.length === 0) {
                ticketsList.innerHTML = '<p class="text-center">No hay tickets asociados a esta orden</p>';
            } else {
                data.tickets.forEach(ticket => {
                    const ticketDiv = document.createElement('div');
                    ticketDiv.className = 'ticket-item mb-3 p-3 border rounded';
                    ticketDiv.innerHTML = `
                        <div class="d-flex justify-content-between align-items-center">
                            <h6 class="mb-0">${ticket.titulo}</h6>
                            <span class="badge badge-${getEstadoBadgeClass(ticket.estado)}">${ticket.estado}</span>
                        </div>
                        <p class="mb-1">${ticket.descripcion}</p>
                        <div class="d-flex justify-content-between">
                            <small class="text-muted">Departamento: ${ticket.departamento_nombre}</small>
                            <small class="text-muted">Creado: ${formatearFecha(ticket.fecha_creacion)}</small>
                        </div>
                    `;
                    ticketsList.appendChild(ticketDiv);
                });
            }
            
            ticketsModal.modal('show');
        } catch (error) {
            console.error('Error al cargar tickets:', error);
            mostrarError('Error al cargar los tickets de la orden');
        }
    }

    async function cargarDepartamentos() {
        try {
            const response = await fetch('/api/departamentos');
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            departamentoSelect.innerHTML = '<option value="">Seleccionar departamento</option>';
            data.departamentos.forEach(depto => {
                const option = document.createElement('option');
                option.value = depto.departamento_id;
                option.textContent = depto.nombre;
                departamentoSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error al cargar departamentos:', error);
            mostrarError('Error al cargar los departamentos');
        }
    }

    async function crearTicket() {
        try {
            const formData = new FormData(ticketForm);
            const data = {
                titulo: formData.get('titulo'),
                descripcion: formData.get('descripcion'),
                departamento_id: formData.get('departamento_id'),
                prioridad: formData.get('prioridad'),
                orden_id: formData.get('orden_id')
            };
            
            const response = await fetch('/api/tickets', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.error) {
                throw new Error(result.error);
            }
            
            mostrarExito('Ticket creado exitosamente');
            ticketForm.reset();
            nuevoTicketForm.style.display = 'none';
            ticketsList.style.display = 'block';
            mostrarTickets(data.orden_id);
        } catch (error) {
            console.error('Error al crear ticket:', error);
            mostrarError('Error al crear el ticket');
        }
    }

    function getEstadoBadgeClass(estado) {
        switch (estado) {
            case 'abierto':
                return 'primary';
            case 'cerrado':
                return 'success';
            case 'en_progreso':
                return 'warning';
            case 'pendiente':
                return 'info';
            default:
                return 'secondary';
        }
    }

    function mostrarExito(mensaje) {
        // Implementar lógica para mostrar mensajes de éxito
        alert(mensaje);
    }
});
