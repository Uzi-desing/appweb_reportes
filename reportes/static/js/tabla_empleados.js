document.addEventListener("DOMContentLoaded", function () {
    const tablaBody = document.getElementById("tablaBody");
    const buscador = document.getElementById("buscador");
    const filtroRol = document.getElementById("filtroRol");
    const btnLimpiar = document.getElementById("btnLimpiar");

    let currentSort = 'nombre';
    let currentOrder = 'asc';
    let debounceTimer;

    function cargarDatosAJAX(urlParams) {
        urlParams.set('ajax', 'true');
        fetch(`${window.location.pathname}?${urlParams.toString()}`)
            .then(response => response.text())
            .then(html => { tablaBody.innerHTML = html; rebindClickFilas(); })
            .catch(error => console.error("Error cargando datos:", error));
    }

    function dispararBusqueda() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            const params = new URLSearchParams();
            if (buscador.value) params.set('q', buscador.value);
            if (filtroRol.value) params.set('rol', filtroRol.value);
            params.set('sort', currentSort);
            params.set('order', currentOrder);
            params.set('page', '1');
            cargarDatosAJAX(params);
        }, 300);
    }

    buscador.addEventListener("input", dispararBusqueda);
    filtroRol.addEventListener("change", dispararBusqueda);

    btnLimpiar.addEventListener("click", () => {
        buscador.value = ""; filtroRol.value = "";
        currentSort = 'nombre'; currentOrder = 'asc';
        document.querySelectorAll('[id^="sort-"]').forEach(span => span.innerText = '⇅');
        document.getElementById('sort-nombre').innerText = '↑';
        dispararBusqueda();
    });

    document.querySelectorAll('.sort-btn').forEach(th => {
        th.addEventListener('click', function() {
            const sortField = this.dataset.sort;
            currentOrder = (currentSort === sortField && currentOrder === 'asc') ? 'desc' : 'asc';
            currentSort = sortField;
            document.querySelectorAll('[id^="sort-"]').forEach(span => span.innerText = '⇅');
            this.querySelector('span').innerText = currentOrder === 'asc' ? '↑' : '↓';
            dispararBusqueda();
        });
    });

    tablaBody.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-pagina')) {
            e.preventDefault();
            const url = new URL(e.target.href);
            const params = new URLSearchParams(url.search);
            if (buscador.value) params.set('q', buscador.value);
            if (filtroRol.value) params.set('rol', filtroRol.value);
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
                fila.onclick = function(e) {
                    if (e.target.closest('button') || e.target.closest('a')) return;
                    window.location.href = this.dataset.url;
                };
            }
        });
    }
    rebindClickFilas();
});