document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('piezas-form');
    const managementForm = document.querySelector('input[name$="-TOTAL_FORMS"]');
    const container = document.getElementById('formset-container');
    const templateHTML = document.getElementById('empty-form-template').innerHTML;
    const errorHandler = document.getElementById('js-error-handler');

    const IMG_CONFIG = { MAX_WIDTH: 1920, MAX_HEIGHT: 1920, QUALITY: 0.95 };

    function updateProgressUI() {
        const rows = container.querySelectorAll('.form-row:not(.hidden)');
        let filled = 0;

        rows.forEach(function(row) {
            const hasPieza = row.querySelector('select[name$="-pieza"]')?.value;
            const hasDano = row.querySelector('select[name$="-categoria_dano"]')?.value;
            
            const fileInput = row.querySelector('input[type="file"]');
            const hasFile = (fileInput && fileInput.files.length > 0) || row.querySelector('a') !== null;

            const isValid = hasPieza && hasDano && hasFile;
            
            const badge = row.querySelector('.pz-card-status');
            if (isValid) {
                filled++;
                badge.textContent = 'Completo';
                badge.classList.remove('bg-gray-600', 'text-gray-300');
                badge.classList.add('bg-green-600', 'text-white');
            } else {
                badge.textContent = 'Incompleto';
                badge.classList.remove('bg-green-600', 'text-white');
                badge.classList.add('bg-gray-600', 'text-gray-300');
            }
        });

        const total = rows.length;
        const pct = total === 0 ? 0 : Math.round((filled / total) * 100);
        document.getElementById('pz-progress-fill').style.width = pct + '%';
        document.getElementById('pz-count-label').textContent = `${total} pieza${total !== 1 ? 's' : ''}`;
        document.getElementById('pz-done-label').textContent = `${filled} completa${filled !== 1 ? 's' : ''}`;
    }

    function reindexRows() {
        const rows = container.querySelectorAll('.form-row:not(.hidden)');
        rows.forEach(function(row, index) {
            row.querySelectorAll('input, select, textarea').forEach(function(el) {
                const name = el.getAttribute('name');
                const id = el.getAttribute('id');
                const regex = /-(\d+|__prefix__)-/;
                if (name) el.setAttribute('name', name.replace(regex, `-${index}-`));
                if (id) el.setAttribute('id', id.replace(regex, `-${index}-`));
            });
            
            row.querySelector('.pz-card-num').textContent = `Pieza #${index + 1}`;
        });
        
        if (managementForm) {
            managementForm.value = container.querySelectorAll('.form-row').length;
        }
        updateProgressUI();
    }

    function showError(msg) {
        const errorText = errorHandler.querySelector('.error-msg-text');
        errorText.textContent = msg;
        errorHandler.classList.remove('hidden');
        errorHandler.style.display = 'none';
        errorHandler.style.display = 'flex';
        document.documentElement.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function hideError() {
        errorHandler.classList.add('hidden');
        document.querySelectorAll('.texto-error-js').forEach(function(el) { el.remove(); });
        document.querySelectorAll('.input-error').forEach(function(el) { el.classList.remove('input-error'); });
    }

    // Compresión de imágenes
    container.addEventListener('change', function(event) {
        if (event.target.type !== 'file') return;
        
        const fileInput = event.target;
        const file = fileInput.files[0];
        const area = fileInput.closest('.pz-foto-area');
        
        updateProgressUI();
        if (!file || !file.type.match(/image.*/)) return;

        area.querySelector('.pz-foto-hint').textContent = 'Comprimiendo...';

        const reader = new FileReader();
        reader.onload = function(e) {
            const img = new Image();
            img.onload = function() {
                let width = img.width;
                let height = img.height;

                if (width > height && width > IMG_CONFIG.MAX_WIDTH) {
                    height = Math.round(height * (IMG_CONFIG.MAX_WIDTH / width));
                    width = IMG_CONFIG.MAX_WIDTH;
                } else if (height > IMG_CONFIG.MAX_HEIGHT) {
                    width = Math.round(width * (IMG_CONFIG.MAX_HEIGHT / height));
                    height = IMG_CONFIG.MAX_HEIGHT;
                }

                const canvas = document.createElement('canvas');
                canvas.width = width;
                canvas.height = height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);

                canvas.toBlob(function(blob) {
                    const compressedFile = new File([blob], file.name, {
                        type: 'image/jpeg',
                        lastModified: Date.now()
                    });

                    const dataTransfer = new DataTransfer();
                    dataTransfer.items.add(compressedFile);
                    fileInput.files = dataTransfer.files;

                    area.querySelector('.pz-foto-name').textContent = compressedFile.name;
                    area.querySelector('.pz-foto-hint').textContent = `Comprimida (${(compressedFile.size / 1024).toFixed(1)} KB) ✓`;
                    area.classList.add('border-brand', 'bg-white');
                    
                    updateProgressUI();
                }, 'image/jpeg', IMG_CONFIG.QUALITY);
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    });

    // Añadir fila
    function addRow(e) {
        if (e) e.preventDefault();
        const total = parseInt(managementForm?.value) || 0;
        const newRow = templateHTML.replace(/__prefix__/g, total);
        
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = newRow;
        const newRowElement = tempDiv.firstElementChild;
        
        container.appendChild(newRowElement);
        if (managementForm) managementForm.value = total + 1;
        reindexRows();
        
        const lastRow = container.querySelector('.form-row:last-child');
        if (lastRow) {
            lastRow.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    const addFormRowBtn = document.getElementById('add-form-row');
    const footerAddBtn = document.getElementById('footer-add-btn');
    if (addFormRowBtn) addFormRowBtn.addEventListener('click', addRow);
    if (footerAddBtn) footerAddBtn.addEventListener('click', addRow);

    // Eliminar fila
    container.addEventListener('click', function(event) {
        const removeBtn = event.target.closest('.remove-row');
        if (!removeBtn) return;
        
        event.preventDefault();
        const row = removeBtn.closest('.form-row');
        const idInput = row.querySelector('input[name$="-id"]');

        if (idInput && idInput.value) {
            const deleteInput = row.querySelector('input[name$="-DELETE"]');
            if (deleteInput) deleteInput.checked = true;
            row.classList.add('hidden');
            row.style.display = 'none';
            updateProgressUI();
        } else {
            row.style.transition = 'opacity 0.2s ease-out';
            row.style.opacity = '0';
            setTimeout(function() {
                row.remove();
                reindexRows();
            }, 200);
        }
    });

    // Validación al cambiar campos
    container.addEventListener('change', function(event) {
        const target = event.target;
        if (target.tagName === 'SELECT' || target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') {
            target.classList.remove('input-error');
            const fieldContainer = target.closest('.js-field-container');
            if (fieldContainer) {
                const errorSpan = fieldContainer.querySelector('.texto-error-js');
                if (errorSpan) {
                    errorSpan.style.display = 'none';
                    setTimeout(function() { errorSpan.remove(); }, 150);
                }
            }
            updateProgressUI();
        }
    });

    // Validación pre-envío
    form.addEventListener('submit', function(e) {
        let isInvalid = false;
        const visibleRows = container.querySelectorAll('.form-row:not(.hidden)');

        hideError();

        if (visibleRows.length === 0) {
            e.preventDefault();
            showError("Debe registrar al menos una pieza en el reporte.");
            return false;
        }

        const camposRequeridos = ['pieza', 'categoria_dano', 'cantidad', 'imagen'];

        visibleRows.forEach(function(row) {
            camposRequeridos.forEach(function(campo) {
                const input = row.querySelector(`[name$="-${campo}"]`);
                if (!input) return;

                const val = input.value;
                const isImageField = (campo === 'imagen');
                const hasExistingImage = isImageField && row.querySelector('a') !== null;

                if (!val && !hasExistingImage) {
                    isInvalid = true;
                    input.classList.add('input-error');
                    
                    const fieldContainer = input.closest('.js-field-container');
                    if (fieldContainer && fieldContainer.querySelectorAll('.texto-error-js').length === 0) {
                        const msgError = input.getAttribute('data-error-msg') || 'Campo obligatorio.';
                        const errorSpan = document.createElement('span');
                        errorSpan.className = 'texto-error-js text-xs font-semibold text-red-600 mt-1.5 flex items-center gap-1.5';
                        errorSpan.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>${msgError}`;
                        fieldContainer.appendChild(errorSpan);
                    }
                }
            });
        });

        if (isInvalid) {
            e.preventDefault();
            showError("Faltan datos obligatorios. Revise las casillas marcadas en rojo.");
            return false;
        }
    });

    // Inicialización
    reindexRows();
});