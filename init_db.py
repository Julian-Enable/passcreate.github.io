#!/usr/bin/env python3
"""
Script para inicializar la base de datos en producción
"""

import os
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent))

from app import app, db, User, PasswordEntry
from cryptography.fernet import Fernet
import secrets

def init_database():
    """Inicializar la base de datos"""
    print("🔐 Inicializando base de datos...")
    
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("✅ Tablas creadas")
        
        # Crear categorías por defecto (se crearán automáticamente al guardar contraseñas)
        print("✅ Categorías se crearán automáticamente")
        
        # Crear clave de encriptación si no existe
        key_file = 'encryption.key'
        if not os.path.exists(key_file):
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            print("✅ Clave de encriptación generada")
        
        print("🎉 Base de datos inicializada correctamente")

def create_admin_user():
    """Crear usuario administrador por defecto"""
    print("👤 Creando usuario administrador...")
    
    with app.app_context():
        # Verificar si ya existe un usuario admin
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("⚠️  Usuario admin ya existe")
            return
        
        # Crear usuario admin
        from werkzeug.security import generate_password_hash
        
        admin = User(
            username='admin',
            email='admin@genpassw.com',
            password_hash=generate_password_hash('admin123')
        )
        
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuario admin creado:")
        print("   Usuario: admin")
        print("   Contraseña: admin123")
        print("   ⚠️  Cambia la contraseña después del primer login")

def main():
    """Función principal"""
    print("🔐 GenPassw Pro - Inicialización de Base de Datos")
    print("=" * 50)
    
    try:
        init_database()
        create_admin_user()
        print("\n🎉 ¡Inicialización completada!")
        print("\n📋 Próximos pasos:")
        print("1. Reinicia tu aplicación en Render")
        print("2. Intenta registrar un nuevo usuario")
        print("3. O usa el usuario admin creado")
        
    except Exception as e:
        print(f"❌ Error durante la inicialización: {e}")
        print("\n🔧 Soluciones:")
        print("1. Verifica las variables de entorno")
        print("2. Asegúrate de que la base de datos esté conectada")
        print("3. Revisa los logs de Render")
        sys.exit(1)

if __name__ == '__main__':
    main()
