document.addEventListener('DOMContentLoaded', function() {
    const toastContainer = document.getElementById('toast-container');
    
    if (!toastContainer) return;

    const messagesElement = document.getElementById('django-messages');
    if (!messagesElement) return;

    const messages = JSON.parse(messagesElement.textContent);

    messages.forEach((msg, index) => {
        let bgColor, borderColor, textColor, iconBg, iconSvg;
        
        switch(msg.tags) {
            case 'error':
                bgColor = 'bg-red-50';
                borderColor = 'border-red-400';
                textColor = 'text-red-700';
                iconBg = 'bg-red-100';
                iconColor = 'text-red-500';
                iconSvg = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>';
                break;
            case 'success':
                bgColor = 'bg-green-50';
                borderColor = 'border-green-400';
                textColor = 'text-green-700';
                iconBg = 'bg-green-100';
                iconColor = 'text-green-500';
                iconSvg = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>';
                break;
            case 'warning':
                bgColor = 'bg-yellow-50';
                borderColor = 'border-yellow-400';
                textColor = 'text-yellow-700';
                iconBg = 'bg-yellow-100';
                iconColor = 'text-yellow-500';
                iconSvg = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>';
                break;
            default:
                bgColor = 'bg-blue-50';
                borderColor = 'border-blue-400';
                textColor = 'text-blue-700';
                iconBg = 'bg-blue-100';
                iconColor = 'text-blue-500';
                iconSvg = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>';
        }

        const toast = document.createElement('div');
        toast.className = `flex items-center gap-3 ${bgColor} border ${borderColor} ${textColor} px-4 py-3 rounded-lg shadow-lg min-w-[300px] max-w-md transform transition-all duration-300 translate-x-full opacity-0`;
        toast.innerHTML = `
            <div class="${iconBg} ${iconColor} p-2 rounded-full">
                ${iconSvg}
            </div>
            <span class="text-sm font-medium">${msg.text}</span>
        `;

        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.classList.remove('translate-x-full', 'opacity-0');
        }, 50 + (index * 100));

        setTimeout(() => {
            toast.classList.add('translate-x-full', 'opacity-0');
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    });
});