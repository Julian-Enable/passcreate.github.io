# 🔐 GenPassw Pro - Gestor de Contraseñas Seguro

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Online-brightgreen.svg)](https://password-create.onrender.com)

Una aplicación web moderna y segura para generar, almacenar y gestionar contraseñas de forma segura. Desarrollada con Flask y desplegada en Render.com.

## 🌟 Características Principales

### 🔒 Seguridad Avanzada
- **Encriptación AES-256**: Todas las contraseñas se almacenan encriptadas
- **Autenticación de usuarios**: Sistema de login/registro seguro
- **Contraseña maestra**: Acceso protegido a todas las contraseñas
- **Sesiones seguras**: Gestión de sesiones con tokens
- **Hashing bcrypt**: Para contraseñas de usuario

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
- **Base de datos SQLite/PostgreSQL**: Almacenamiento seguro
- **Exportación JSON/CSV**: Exporta tus contraseñas en múltiples formatos
- **Respaldo automático**: Sistema de respaldo integrado
- **Sincronización**: Preparado para sincronización futura

### 🎨 Interfaz Moderna
- **Diseño responsive**: Funciona perfectamente en móviles y tablets
- **Tema oscuro**: Interfaz elegante con gradientes y animaciones
- **UX intuitiva**: Navegación clara y fácil de usar
- **Notificaciones**: Feedback visual para todas las acciones

## 🚀 Demo en Vivo

**¡Prueba la aplicación ahora mismo!**

🌐 **URL**: [https://password-create.onrender.com](https://password-create.onrender.com)

🔑 **Credenciales de Demo**:
- **Usuario**: `admin`
- **Contraseña**: `admin123`

## 📱 Características Técnicas

### Backend
- **Framework**: Flask (Python)
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **ORM**: SQLAlchemy
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

## 🛠️ Instalación y Uso

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Instalación Rápida

**Opción 1: Instalación automática (Recomendada)**
```bash
# Clonar el repositorio
git clone https://github.com/Julian-Enable/passcreate.github.io.git
cd passcreate.github.io

# Instalación automática
python install.py
```

**Opción 2: Instalación manual**
```bash
# Clonar el repositorio
git clone https://github.com/Julian-Enable/passcreate.github.io.git
cd passcreate.github.io

# Instalar dependencias
pip install -r requirements.txt

# Configurar entorno (opcional)
cp env.example .env
# Edita .env con tus configuraciones
```

### Ejecutar la Aplicación

```bash
# Usar el script de inicio (recomendado)
python run.py

# O ejecutar directamente
python app.py
```

### Acceder a la Aplicación
- Abre tu navegador y ve a `http://localhost:5000`
- Registra una nueva cuenta o usa las credenciales de demo
- ¡Comienza a usar GenPassw Pro!

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
├── config.py              # Configuración de la aplicación
├── run.py                 # Script de inicio
├── start.py               # Script de inicialización para producción
├── install.py             # Script de instalación automática
├── requirements.txt       # Dependencias de Python
├── Procfile               # Configuración para Render/Heroku
├── render.yaml            # Configuración para Render.com
├── runtime.txt            # Versión de Python
├── README.md              # Documentación
├── templates/             # Plantillas HTML
│   ├── base.html          # Template base
│   ├── login.html         # Página de login
│   ├── register.html      # Página de registro
│   └── index.html         # Dashboard principal
├── static/                # Archivos estáticos
│   ├── css/
│   │   └── style.css      # Estilos personalizados
│   └── js/
│       ├── app.js         # Funciones de utilidad
│       └── dashboard.js   # Lógica del dashboard
├── utils/                 # Utilidades
│   ├── __init__.py
│   ├── logger.py          # Sistema de logging
│   └── backup.py          # Sistema de backup
├── logs/                  # Archivos de log
├── backups/               # Backups de la aplicación
└── uploads/               # Archivos subidos
```

## 🚀 Despliegue en Producción

### Desplegado en Render.com

La aplicación está actualmente desplegada en [Render.com](https://render.com) y disponible en:
**https://password-create.onrender.com**

### Variables de Entorno Necesarias
```env
SECRET_KEY=tu-clave-secreta-super-segura
FLASK_ENV=production
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/db
```

### Verificación Previa al Despliegue
```bash
# Verificar que todo esté listo
python deploy.py
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

### Guía de Contribución
- Asegúrate de que tu código siga las convenciones de Python (PEP 8)
- Agrega tests para nuevas funcionalidades
- Actualiza la documentación según sea necesario
- Verifica que todos los tests pasen

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Si tienes problemas o preguntas:

- 🌐 **Demo en vivo**: [https://password-create.onrender.com](https://password-create.onrender.com)
- 📧 **Issues**: Abre un issue en GitHub
- 📖 **Documentación**: Consulta este README
- 🔧 **Desarrollo**: Fork el proyecto y contribuye

## 🏆 Créditos

**Desarrollado por**: Julian Enable

**Tecnologías utilizadas**:
- Flask (Python Web Framework)
- SQLAlchemy (ORM)
- Bootstrap 5 (CSS Framework)
- Cryptography (Encriptación)
- Render.com (Hosting)

---

## ⚠️ Disclaimer

Este software se proporciona "tal como está" sin garantías. Los desarrolladores no son responsables del uso indebido de esta aplicación. Siempre sigue las mejores prácticas de seguridad al gestionar contraseñas.

**¡Gracias por usar GenPassw Pro! 🔐✨**

---

<div align="center">

**⭐ ¡Dale una estrella al proyecto si te gustó! ⭐**

[![GitHub stars](https://img.shields.io/github/stars/Julian-Enable/passcreate.github.io?style=social)](https://github.com/Julian-Enable/passcreate.github.io/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Julian-Enable/passcreate.github.io?style=social)](https://github.com/Julian-Enable/passcreate.github.io/network)

</div>
