// Funciones de utilidad para GenPassw Pro

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Función para copiar texto al portapapeles
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Texto copiado al portapapeles', 'success');
        return true;
    } catch (err) {
        // Fallback para navegadores más antiguos
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showNotification('Texto copiado al portapapeles', 'success');
        return true;
    }
}

// Función para validar contraseña
function validatePassword(password) {
    const checks = {
        length: password.length >= 8,
        uppercase: /[A-Z]/.test(password),
        lowercase: /[a-z]/.test(password),
        numbers: /\d/.test(password),
        symbols: /[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(password)
    };
    
    const score = Object.values(checks).filter(Boolean).length;
    
    if (score <= 2) return { strength: 'weak', score };
    if (score <= 3) return { strength: 'medium', score };
    if (score <= 4) return { strength: 'strong', score };
    return { strength: 'very-strong', score };
}

// Función para formatear fecha
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Función para hacer peticiones HTTP
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const finalOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, finalOptions);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error en petición API:', error);
        throw error;
    }
}

// Función para exportar datos como JSON
function exportAsJSON(data, filename = 'passwords.json') {
    const dataStr = JSON.stringify(data, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = filename;
    link.click();
    
    URL.revokeObjectURL(link.href);
}

// Función para exportar datos como CSV
function exportAsCSV(data, filename = 'passwords.csv') {
    if (data.length === 0) return;
    
    const headers = ['Email', 'Website', 'Password', 'Category', 'Notes', 'Created At'];
    const csvContent = [
        headers.join(','),
        ...data.map(item => [
            `"${item.email}"`,
            `"${item.website}"`,
            `"${item.password}"`,
            `"${item.category}"`,
            `"${item.notes || ''}"`,
            `"${item.created_at}"`
        ].join(','))
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    
    URL.revokeObjectURL(link.href);
}

// Función para debounce
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Función para generar ID único
function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// Función para sanitizar HTML
function sanitizeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// Función para verificar si el navegador soporta características modernas
function checkBrowserSupport() {
    const features = {
        clipboard: 'clipboard' in navigator,
        webcrypto: 'crypto' in window && 'subtle' in window.crypto,
        serviceWorker: 'serviceWorker' in navigator,
        localStorage: 'localStorage' in window
    };
    
    return features;
}

// Función para obtener la fortaleza visual de la contraseña
function getPasswordStrengthVisual(password) {
    const validation = validatePassword(password);
    const strengthClasses = {
        'weak': 'strength-weak',
        'medium': 'strength-medium',
        'strong': 'strength-strong',
        'very-strong': 'strength-very-strong'
    };
    
    return strengthClasses[validation.strength] || 'strength-weak';
}

// Función para mostrar/ocultar contraseña
function togglePasswordVisibility(inputElement, buttonElement) {
    const type = inputElement.type === 'password' ? 'text' : 'password';
    inputElement.type = type;
    
    const icon = buttonElement.querySelector('i');
    icon.className = type === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash';
}

// Función para inicializar tooltips de Bootstrap
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Función para inicializar popovers de Bootstrap
function initPopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Función para manejar errores globales
function handleGlobalError(error) {
    console.error('Error global:', error);
    showNotification('Ha ocurrido un error inesperado. Por favor, recarga la página.', 'danger');
}

// Configurar manejo de errores globales
window.addEventListener('error', handleGlobalError);
window.addEventListener('unhandledrejection', (event) => {
    handleGlobalError(event.reason);
});

// Inicializar componentes cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initTooltips();
    initPopovers();
    
    // Verificar soporte del navegador
    const support = checkBrowserSupport();
    if (!support.clipboard) {
        console.warn('El navegador no soporta la API de Clipboard');
    }
});
