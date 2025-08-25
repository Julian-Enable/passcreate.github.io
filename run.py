#!/usr/bin/env python3
"""
Script de inicio para GenPassw Pro
"""

import os
import sys
from app import app, db

def create_app(config_name=None):
    """Crear y configurar la aplicación Flask"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Importar configuración
    from config import config
    
    # Configurar la aplicación
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    
    return app

def init_db():
    """Inicializar la base de datos"""
    with app.app_context():
        db.create_all()
        print("✅ Base de datos inicializada correctamente")

def check_dependencies():
    """Verificar que todas las dependencias estén instaladas"""
    try:
        import flask
        import flask_sqlalchemy
        import cryptography
        import werkzeug
        print("✅ Todas las dependencias están instaladas")
        return True
    except ImportError as e:
        print(f"❌ Error: Falta la dependencia {e.name}")
        print("Ejecuta: pip install -r requirements.txt")
        return False

def main():
    """Función principal"""
    print("🔐 GenPassw Pro - Gestor de Contraseñas Seguro")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        sys.exit(1)
    
    # Crear aplicación
    app = create_app()
    
    # Inicializar base de datos
    try:
        init_db()
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        sys.exit(1)
    
    # Obtener configuración del puerto
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = app.config.get('DEBUG', False)
    
    print(f"🚀 Iniciando servidor en http://{host}:{port}")
    print(f"🔧 Modo debug: {'Activado' if debug else 'Desactivado'}")
    print("=" * 50)
    print("💡 Presiona Ctrl+C para detener el servidor")
    print("=" * 50)
    
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error al iniciar el servidor: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
