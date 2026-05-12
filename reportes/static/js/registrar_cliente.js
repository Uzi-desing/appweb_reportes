document.addEventListener("DOMContentLoaded", function() {
    const inputTelefono = document.getElementById("id_telefono");
    if (inputTelefono) {
        inputTelefono.addEventListener("input", function(e) {
            this.value = this.value.replace(/\D/g, '');
        });
    }
});