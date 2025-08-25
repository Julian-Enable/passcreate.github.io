# 🔐 GenPassw Pro - Gestor de Contraseñas Seguro

Una aplicación web moderna y segura para generar, almacenar y gestionar contraseñas de forma segura.

## ✨ Características Principales

### 🔒 Seguridad Avanzada
- **Encriptación AES-256**: Todas las contraseñas se almacenan encriptadas
- **Autenticación de usuarios**: Sistema de login/registro seguro
- **Contraseña maestra**: Acceso protegido a todas las contraseñas
- **Sesiones seguras**: Gestión de sesiones con tokens

### 🎯 Generación de Contraseñas
- **Longitud personalizable**: De 8 a 64 caracteres
- **Opciones configurables**: Mayúsculas, minúsculas, números, símbolos
- **Contraseñas seguras**: Algoritmo que garantiza al menos un carácter de cada tipo seleccionado
- **Indicador de fortaleza**: Visualización de la seguridad de la contraseña

### 📊 Gestión Avanzada
- **Categorización**: Organiza contraseñas por categorías (Trabajo, Personal, Finanzas, etc.)
- **Búsqueda inteligente**: Busca por correo, sitio web o categoría
- **Filtros dinámicos**: Filtra por categorías específicas
- **Notas adicionales**: Añade información extra a cada contraseña

### 💾 Almacenamiento y Exportación
- **Base de datos SQLite**: Almacenamiento local seguro
- **Exportación JSON/CSV**: Exporta tus contraseñas en múltiples formatos
- **Respaldo automático**: Sistema de respaldo integrado
- **Sincronización**: Preparado para sincronización futura

### 🎨 Interfaz Moderna
- **Diseño responsive**: Funciona perfectamente en móviles y tablets
- **Tema moderno**: Interfaz elegante con gradientes y animaciones
- **UX intuitiva**: Navegación clara y fácil de usar
- **Notificaciones**: Feedback visual para todas las acciones

## 🚀 Instalación y Uso

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/genpassw-pro.git
   cd genpassw-pro
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

4. **Acceder a la aplicación**
   - Abre tu navegador y ve a `http://localhost:5000`
   - Registra una nueva cuenta
   - ¡Comienza a usar GenPassw Pro!

### Variables de Entorno (Opcional)
Crea un archivo `.env` en la raíz del proyecto:
```env
SECRET_KEY=tu-clave-secreta-super-segura
FLASK_ENV=development
```

## 📱 Características Técnicas

### Backend
- **Framework**: Flask (Python)
- **Base de datos**: SQLite con SQLAlchemy ORM
- **Encriptación**: Cryptography (Fernet)
- **Autenticación**: Werkzeug Security
- **API RESTful**: Endpoints JSON para todas las operaciones

### Frontend
- **Framework CSS**: Bootstrap 5
- **Iconos**: Font Awesome 6
- **JavaScript**: ES6+ con clases y async/await
- **Responsive**: Mobile-first design
- **Animaciones**: CSS3 transitions y keyframes

### Seguridad
- **Encriptación AES-256**: Para contraseñas almacenadas
- **Hashing bcrypt**: Para contraseñas de usuario
- **Sesiones seguras**: Con cookies encriptadas
- **Validación**: Sanitización de inputs
- **CSRF Protection**: Protección contra ataques CSRF

## 🔧 API Endpoints

### Autenticación
- `POST /login` - Iniciar sesión
- `POST /register` - Registrar usuario
- `GET /logout` - Cerrar sesión

### Contraseñas
- `POST /api/generate-password` - Generar contraseña
- `POST /api/save-password` - Guardar contraseña
- `GET /api/passwords` - Obtener todas las contraseñas
- `GET /api/passwords/<id>` - Obtener contraseña específica
- `DELETE /api/passwords/<id>` - Eliminar contraseña

### Utilidades
- `GET /api/categories` - Obtener categorías
- `GET /api/export` - Exportar contraseñas

## 📊 Estructura del Proyecto

```
genpassw-pro/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias de Python
├── README.md             # Documentación
├── templates/            # Plantillas HTML
│   ├── base.html         # Template base
│   ├── login.html        # Página de login
│   ├── register.html     # Página de registro
│   └── index.html        # Dashboard principal
├── static/               # Archivos estáticos
│   ├── css/
│   │   └── style.css     # Estilos personalizados
│   └── js/
│       ├── app.js        # Funciones de utilidad
│       └── dashboard.js  # Lógica del dashboard
├── passwords.db          # Base de datos SQLite
└── encryption.key        # Clave de encriptación
```

## 🛡️ Medidas de Seguridad

### Encriptación de Datos
- Todas las contraseñas se encriptan antes de almacenarse
- Clave de encriptación única por instalación
- Algoritmo AES-256 para máxima seguridad

### Autenticación
- Contraseñas hasheadas con bcrypt
- Sesiones seguras con tokens
- Protección contra ataques de fuerza bruta

### Validación
- Sanitización de todos los inputs
- Validación de tipos de datos
- Protección contra inyección SQL

## 🔄 Funcionalidades Futuras

- [ ] **Sincronización en la nube**: Backup automático en la nube
- [ ] **Autocompletado**: Integración con navegadores
- [ ] **Autenticación de dos factores**: 2FA para mayor seguridad
- [ ] **Compartir contraseñas**: Compartir de forma segura
- [ ] **Análisis de seguridad**: Auditoría de contraseñas
- [ ] **Notificaciones**: Alertas de contraseñas comprometidas
- [ ] **API pública**: Para integración con otras aplicaciones

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## ⚠️ Disclaimer

Este software se proporciona "tal como está" sin garantías. Los desarrolladores no son responsables del uso indebido de esta aplicación. Siempre sigue las mejores prácticas de seguridad al gestionar contraseñas.

## 📞 Soporte

Si tienes problemas o preguntas:

- Abre un issue en GitHub
- Contacta al equipo de desarrollo
- Consulta la documentación

---

**¡Gracias por usar GenPassw Pro! 🔐✨**
