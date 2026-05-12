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
});