document.addEventListener("DOMContentLoaded", function () {
    const tablaBody = document.getElementById("tablaBody");
    const buscador = document.getElementById("buscador");
    const fechaDesde = document.getElementById("fechaDesde");
    const fechaHasta = document.getElementById("fechaHasta");
    const filtroEmpleado = document.getElementById("filtroEmpleado");
    const btnLimpiar = document.getElementById("btnLimpiar");

    let currentSort = 'id';
    let currentOrder = 'desc';
    let debounceTimer;

    function cargarDatosAJAX(urlParams) {
        urlParams.set('ajax', 'true');
        
        fetch(`${window.location.pathname}?${urlParams.toString()}`)
            .then(response => response.text())
            .then(html => {
                tablaBody.innerHTML = html;
                rebindClickFilas();
            })
            .catch(error => console.error("Error cargando datos:", error));
    }

    function dispararBusqueda() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            const params = new URLSearchParams();
            if (buscador.value) params.set('q', buscador.value);
            if (fechaDesde.value) params.set('desde', fechaDesde.value);
            if (fechaHasta.value) params.set('hasta', fechaHasta.value);
            if (filtroEmpleado.value) params.set('empleado', filtroEmpleado.value);
            params.set('sort', currentSort);
            params.set('order', currentOrder);
            params.set('page', '1');
            
            cargarDatosAJAX(params);
        }, 300);
    }

    buscador.addEventListener("input", dispararBusqueda);
    filtroEmpleado.addEventListener("change", dispararBusqueda);
    fechaDesde.addEventListener("change", dispararBusqueda);
    fechaHasta.addEventListener("change", dispararBusqueda);

    btnLimpiar.addEventListener("click", () => {
        buscador.value = "";
        filtroEmpleado.value = "";
        fechaDesde.value = "";
        fechaHasta.value = "";
        currentSort = 'id';
        currentOrder = 'desc';
        document.querySelectorAll('[id^="sort-"]').forEach(span => span.textContent = '⇅');
        document.getElementById('sort-id').textContent = '↓';
        dispararBusqueda();
    });

    document.querySelectorAll('.sort-btn').forEach(th => {
        th.addEventListener('click', function() {
            const sortField = this.dataset.sort;
            currentOrder = (currentSort === sortField && currentOrder === 'desc') ? 'asc' : 'desc';
            currentSort = sortField;
            document.querySelectorAll('[id^="sort-"]').forEach(span => span.textContent = '⇅');
            this.querySelector('span').textContent = currentOrder === 'desc' ? '↓' : '↑';
            dispararBusqueda();
        });
    });

    tablaBody.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-pagina') || e.target.closest('.btn-pagina')) {
            e.preventDefault();
            const btn = e.target.classList.contains('btn-pagina') ? e.target : e.target.closest('.btn-pagina');
            const url = new URL(btn.href);
            const params = new URLSearchParams(url.search);
            
            if (buscador.value) params.set('q', buscador.value);
            if (filtroEmpleado.value) params.set('empleado', filtroEmpleado.value);
            if (fechaDesde.value) params.set('desde', fechaDesde.value);
            if (fechaHasta.value) params.set('hasta', fechaHasta.value);
            params.set('sort', currentSort);
            params.set('orden', currentOrder);
            
            cargarDatosAJAX(params);
        }
    });

    function rebindClickFilas() {
        const filas = tablaBody.querySelectorAll("tr:not(.fila-paginacion)");
        filas.forEach(fila => {
            if (fila.dataset.url) {
                fila.style.cursor = 'pointer';
                fila.addEventListener('click', function(e) {
                    if (e.target.closest('button') || e.target.closest('a')) {
                        return;
                    }
                    window.location.href = this.dataset.url;
                });
            }
        });
    }
    
    rebindClickFilas();
});