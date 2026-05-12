document.addEventListener("DOMContentLoaded", function() {
    const tablaBody = document.getElementById("tablaBody");
    const buscador = document.getElementById("buscador");
    const btnLimpiar = document.getElementById("btnLimpiar");

    let currentSort = 'nombre';
    let currentOrder = 'asc';
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
            params.set('sort', currentSort);
            params.set('orden', currentOrder); 
            params.set('page', '1');
            
            cargarDatosAJAX(params);
        }, 300);
    }

    buscador.addEventListener("input", dispararBusqueda);

    btnLimpiar.addEventListener("click", () => {
        buscador.value = "";
        currentSort = 'nombre';
        currentOrder = 'asc';
        
        document.getElementById('sort-nombre').textContent = '↑';
        dispararBusqueda();
    });

    document.querySelectorAll('.sort-btn').forEach(th => {
        th.addEventListener('click', function() {
            const sortField = this.dataset.sort;
            
            currentOrder = (currentSort === sortField && currentOrder === 'asc') ? 'desc' : 'asc';
            currentSort = sortField;
            
            this.querySelector('span').textContent = currentOrder === 'asc' ? '↑' : '↓';

            // Reset other sort indicators
            document.querySelectorAll('[id^="sort-"]').forEach(span => {
                if (span.id !== `sort-${sortField}`) span.textContent = '⇅';
            });

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
            params.set('sort', currentSort);
            params.set('orden', currentOrder);
            
            cargarDatosAJAX(params);
        }
    });

    function rebindClickFilas() {
        const filas = tablaBody.querySelectorAll("tr:not(.fila-paginacion)");
        filas.forEach(fila => {
            if (fila.dataset.url && fila.dataset.url !== '#') {
                fila.style.cursor = 'pointer';
                fila.classList.add('hover:bg-black/5');
                fila.addEventListener('click', function(e) {
                    if (e.target.closest('button') || e.target.closest('a')) return;
                    window.location.href = this.dataset.url;
                });
            } else {
                fila.style.cursor = 'default';
            }
        });
    }
    
    rebindClickFilas();
});