document.addEventListener('DOMContentLoaded', function() {
    const dniInput = document.getElementById('id_dniConductor');

    if (dniInput) {
        dniInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 8) {
                value = value.slice(0, 8);
            }

            let formattedValue = value.replace(/\B(?=(\d{3})+(?!\d))/g, ".");

            e.target.value = formattedValue;
        });
    }

    const form = document.querySelector('form');
    const btn = document.getElementById('btn-submit-reporte');

    if (form && btn) {
        form.addEventListener('submit', function() {
            btn.disabled = true;
            btn.classList.add('opacity-75', 'cursor-not-allowed');
            btn.innerHTML = `
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                Guardando...
            `;
        });
    }
});