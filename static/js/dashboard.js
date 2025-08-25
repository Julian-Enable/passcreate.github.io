// Dashboard JavaScript para GenPassw Pro

class PasswordManager {
    constructor() {
        this.currentPasswordId = null;
        this.passwords = [];
        this.categories = [];
        this.init();
    }

    async init() {
        this.bindEvents();
        await this.loadPasswords();
        await this.loadCategories();
        this.generateNewPassword();
    }

    bindEvents() {
        // Formulario de generación de contraseña
        document.getElementById('passwordForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.savePassword();
        });

        // Slider de longitud
        const lengthSlider = document.getElementById('passwordLength');
        const lengthValue = document.getElementById('lengthValue');
        lengthSlider.addEventListener('input', (e) => {
            lengthValue.textContent = e.target.value;
            this.generateNewPassword();
        });

        // Checkboxes de opciones
        ['includeUppercase', 'includeLowercase', 'includeNumbers', 'includeSymbols'].forEach(id => {
            document.getElementById(id).addEventListener('change', () => {
                this.generateNewPassword();
            });
        });

        // Botones de copiar y generar
        document.getElementById('copyPassword').addEventListener('click', () => {
            this.copyGeneratedPassword();
        });

        document.getElementById('generateNew').addEventListener('click', () => {
            this.generateNewPassword();
        });

        // Búsqueda y filtros
        document.getElementById('searchInput').addEventListener('input', debounce((e) => {
            this.filterPasswords();
        }, 300));

        document.getElementById('categoryFilter').addEventListener('change', () => {
            this.filterPasswords();
        });

        // Botones de exportar y actualizar
        document.getElementById('exportBtn').addEventListener('click', () => {
            this.exportPasswords();
        });

        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.loadPasswords();
        });

        // Modal events
        document.getElementById('togglePassword').addEventListener('click', () => {
            const passwordInput = document.getElementById('modalPassword');
            const button = document.getElementById('togglePassword');
            togglePasswordVisibility(passwordInput, button);
        });

        document.getElementById('copyModalPassword').addEventListener('click', () => {
            const password = document.getElementById('modalPassword').value;
            copyToClipboard(password);
        });

        document.getElementById('deletePassword').addEventListener('click', () => {
            this.deleteCurrentPassword();
        });
    }

    async generateNewPassword() {
        const length = parseInt(document.getElementById('passwordLength').value);
        const includeUppercase = document.getElementById('includeUppercase').checked;
        const includeLowercase = document.getElementById('includeLowercase').checked;
        const includeNumbers = document.getElementById('includeNumbers').checked;
        const includeSymbols = document.getElementById('includeSymbols').checked;

        try {
            const response = await apiRequest('/api/generate-password', {
                method: 'POST',
                body: JSON.stringify({
                    length,
                    include_uppercase: includeUppercase,
                    include_lowercase: includeLowercase,
                    include_numbers: includeNumbers,
                    include_symbols: includeSymbols
                })
            });

            document.getElementById('generatedPassword').value = response.password;
            this.updatePasswordStrength(response.password);
        } catch (error) {
            showNotification('Error al generar contraseña', 'danger');
        }
    }

    updatePasswordStrength(password) {
        const validation = validatePassword(password);
        const strengthBar = document.createElement('div');
        strengthBar.className = `password-strength ${getPasswordStrengthVisual(password)}`;
        
        const container = document.getElementById('generatedPassword').parentElement;
        const existingBar = container.querySelector('.password-strength');
        if (existingBar) {
            existingBar.remove();
        }
        container.appendChild(strengthBar);
    }

    async savePassword() {
        const email = document.getElementById('email').value;
        const website = document.getElementById('website').value;
        const password = document.getElementById('generatedPassword').value;
        const category = document.getElementById('category').value;
        const notes = document.getElementById('notes').value;

        if (!email || !website || !password) {
            showNotification('Por favor completa todos los campos requeridos', 'warning');
            return;
        }

        try {
            const response = await apiRequest('/api/save-password', {
                method: 'POST',
                body: JSON.stringify({
                    email,
                    website,
                    password,
                    category,
                    notes
                })
            });

            showNotification('Contraseña guardada exitosamente', 'success');
            this.resetForm();
            await this.loadPasswords();
        } catch (error) {
            showNotification('Error al guardar la contraseña', 'danger');
        }
    }

    resetForm() {
        document.getElementById('passwordForm').reset();
        document.getElementById('passwordLength').value = 16;
        document.getElementById('lengthValue').textContent = '16';
        document.getElementById('generatedPassword').value = '';
        this.generateNewPassword();
    }

    async loadPasswords() {
        try {
            const passwords = await apiRequest('/api/passwords');
            this.passwords = passwords;
            this.renderPasswords();
        } catch (error) {
            showNotification('Error al cargar las contraseñas', 'danger');
        }
    }

    async loadCategories() {
        try {
            const categories = await apiRequest('/api/categories');
            this.categories = categories;
            this.updateCategoryFilters();
        } catch (error) {
            console.error('Error al cargar categorías:', error);
        }
    }

    updateCategoryFilters() {
        const filterSelect = document.getElementById('categoryFilter');
        const currentValue = filterSelect.value;
        
        // Mantener la opción "Todas las categorías"
        filterSelect.innerHTML = '<option value="">Todas las categorías</option>';
        
        this.categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            filterSelect.appendChild(option);
        });
        
        filterSelect.value = currentValue;
    }

    renderPasswords() {
        const tbody = document.getElementById('passwordsTableBody');
        const noPasswords = document.getElementById('noPasswords');
        const passwordsList = document.getElementById('passwordsList');

        if (this.passwords.length === 0) {
            tbody.innerHTML = '';
            noPasswords.style.display = 'block';
            passwordsList.style.display = 'none';
            return;
        }

        noPasswords.style.display = 'none';
        passwordsList.style.display = 'block';

        tbody.innerHTML = this.passwords.map(password => `
            <tr class="fade-in">
                <td>${sanitizeHTML(password.email)}</td>
                <td>${sanitizeHTML(password.website)}</td>
                <td>
                    <span class="badge bg-secondary">${sanitizeHTML(password.category)}</span>
                </td>
                <td>${formatDate(password.updated_at)}</td>
                <td>
                    <div class="btn-group btn-group-sm" role="group">
                        <button class="btn btn-outline-primary" onclick="passwordManager.viewPassword(${password.id})" 
                                data-bs-toggle="tooltip" title="Ver contraseña">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="btn btn-outline-danger" onclick="passwordManager.deletePassword(${password.id})"
                                data-bs-toggle="tooltip" title="Eliminar">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');

        // Reinicializar tooltips
        initTooltips();
    }

    filterPasswords() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        const categoryFilter = document.getElementById('categoryFilter').value;

        const filteredPasswords = this.passwords.filter(password => {
            const matchesSearch = !searchTerm || 
                password.email.toLowerCase().includes(searchTerm) ||
                password.website.toLowerCase().includes(searchTerm) ||
                password.category.toLowerCase().includes(searchTerm);
            
            const matchesCategory = !categoryFilter || password.category === categoryFilter;
            
            return matchesSearch && matchesCategory;
        });

        this.renderFilteredPasswords(filteredPasswords);
    }

    renderFilteredPasswords(filteredPasswords) {
        const tbody = document.getElementById('passwordsTableBody');
        const noPasswords = document.getElementById('noPasswords');
        const passwordsList = document.getElementById('passwordsList');

        if (filteredPasswords.length === 0) {
            tbody.innerHTML = '';
            noPasswords.style.display = 'block';
            passwordsList.style.display = 'none';
            return;
        }

        noPasswords.style.display = 'none';
        passwordsList.style.display = 'block';

        tbody.innerHTML = filteredPasswords.map(password => `
            <tr class="fade-in">
                <td>${sanitizeHTML(password.email)}</td>
                <td>${sanitizeHTML(password.website)}</td>
                <td>
                    <span class="badge bg-secondary">${sanitizeHTML(password.category)}</span>
                </td>
                <td>${formatDate(password.updated_at)}</td>
                <td>
                    <div class="btn-group btn-group-sm" role="group">
                        <button class="btn btn-outline-primary" onclick="passwordManager.viewPassword(${password.id})" 
                                data-bs-toggle="tooltip" title="Ver contraseña">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="btn btn-outline-danger" onclick="passwordManager.deletePassword(${password.id})"
                                data-bs-toggle="tooltip" title="Eliminar">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');

        initTooltips();
    }

    async viewPassword(passwordId) {
        try {
            const password = await apiRequest(`/api/passwords/${passwordId}`);
            
            document.getElementById('modalEmail').value = password.email;
            document.getElementById('modalWebsite').value = password.website;
            document.getElementById('modalPassword').value = password.password;
            document.getElementById('modalCategory').value = password.category;
            document.getElementById('modalNotes').value = password.notes || '';
            
            this.currentPasswordId = passwordId;
            
            const modal = new bootstrap.Modal(document.getElementById('passwordModal'));
            modal.show();
        } catch (error) {
            showNotification('Error al cargar la contraseña', 'danger');
        }
    }

    async deletePassword(passwordId) {
        if (!confirm('¿Estás seguro de que quieres eliminar esta contraseña?')) {
            return;
        }

        try {
            await apiRequest(`/api/passwords/${passwordId}`, {
                method: 'DELETE'
            });

            showNotification('Contraseña eliminada exitosamente', 'success');
            await this.loadPasswords();
            
            // Si el modal está abierto, cerrarlo
            const modal = bootstrap.Modal.getInstance(document.getElementById('passwordModal'));
            if (modal) {
                modal.hide();
            }
        } catch (error) {
            showNotification('Error al eliminar la contraseña', 'danger');
        }
    }

    async deleteCurrentPassword() {
        if (this.currentPasswordId) {
            await this.deletePassword(this.currentPasswordId);
        }
    }

    copyGeneratedPassword() {
        const password = document.getElementById('generatedPassword').value;
        if (password) {
            copyToClipboard(password);
        } else {
            showNotification('No hay contraseña generada para copiar', 'warning');
        }
    }

    async exportPasswords() {
        try {
            const data = await apiRequest('/api/export');
            
            if (data.length === 0) {
                showNotification('No hay contraseñas para exportar', 'warning');
                return;
            }

            // Crear menú de exportación
            const exportMenu = document.createElement('div');
            exportMenu.className = 'dropdown-menu show';
            exportMenu.innerHTML = `
                <a class="dropdown-item" href="#" onclick="passwordManager.exportAsJSON()">
                    <i class="fas fa-file-code me-2"></i>Exportar como JSON
                </a>
                <a class="dropdown-item" href="#" onclick="passwordManager.exportAsCSV()">
                    <i class="fas fa-file-csv me-2"></i>Exportar como CSV
                </a>
            `;

            // Posicionar el menú
            const button = document.getElementById('exportBtn');
            const rect = button.getBoundingClientRect();
            exportMenu.style.position = 'fixed';
            exportMenu.style.top = `${rect.bottom + 5}px`;
            exportMenu.style.left = `${rect.left}px`;
            exportMenu.style.zIndex = '1000';

            document.body.appendChild(exportMenu);

            // Cerrar menú al hacer clic fuera
            const closeMenu = (e) => {
                if (!exportMenu.contains(e.target) && !button.contains(e.target)) {
                    exportMenu.remove();
                    document.removeEventListener('click', closeMenu);
                }
            };

            setTimeout(() => {
                document.addEventListener('click', closeMenu);
            }, 100);

        } catch (error) {
            showNotification('Error al exportar las contraseñas', 'danger');
        }
    }

    async exportAsJSON() {
        try {
            const data = await apiRequest('/api/export');
            exportAsJSON(data, `passwords_${new Date().toISOString().split('T')[0]}.json`);
            showNotification('Contraseñas exportadas como JSON', 'success');
        } catch (error) {
            showNotification('Error al exportar como JSON', 'danger');
        }
    }

    async exportAsCSV() {
        try {
            const data = await apiRequest('/api/export');
            exportAsCSV(data, `passwords_${new Date().toISOString().split('T')[0]}.csv`);
            showNotification('Contraseñas exportadas como CSV', 'success');
        } catch (error) {
            showNotification('Error al exportar como CSV', 'danger');
        }
    }
}

// Inicializar el gestor de contraseñas cuando el DOM esté listo
let passwordManager;
document.addEventListener('DOMContentLoaded', function() {
    passwordManager = new PasswordManager();
});
