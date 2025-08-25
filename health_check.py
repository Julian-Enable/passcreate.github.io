#!/usr/bin/env python3
"""
Script de verificación de salud para Render
"""

import os
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent))

def check_environment():
    """Verificar variables de entorno"""
    print("🔍 Verificando variables de entorno...")
    
    required_vars = ['SECRET_KEY', 'DATABASE_URL']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables faltantes: {', '.join(missing_vars)}")
        return False
    
    print("✅ Variables de entorno configuradas")
    return True

def check_database():
    """Verificar conexión a base de datos"""
    print("🔍 Verificando conexión a base de datos...")
    
    try:
        from app import app, db
        
        with app.app_context():
            # Intentar una consulta simple
            db.session.execute('SELECT 1')
            print("✅ Conexión a base de datos exitosa")
            return True
    except Exception as e:
        print(f"❌ Error de conexión a base de datos: {e}")
        return False

def check_encryption():
    """Verificar clave de encriptación"""
    print("🔍 Verificando clave de encriptación...")
    
    key_file = 'encryption.key'
    if not os.path.exists(key_file):
        print("❌ Clave de encriptación no encontrada")
        return False
    
    try:
        from cryptography.fernet import Fernet
        with open(key_file, 'rb') as f:
            key = f.read()
        Fernet(key)  # Verificar que la clave es válida
        print("✅ Clave de encriptación válida")
        return True
    except Exception as e:
        print(f"❌ Error con clave de encriptación: {e}")
        return False

def main():
    """Función principal"""
    print("🔐 GenPassw Pro - Verificación de Salud")
    print("=" * 40)
    
    checks = [
        check_environment(),
        check_database(),
        check_encryption()
    ]
    
    if all(checks):
        print("\n🎉 ¡Sistema funcionando correctamente!")
        sys.exit(0)
    else:
        print("\n❌ Hay problemas que resolver")
        sys.exit(1)

if __name__ == '__main__':
    main()
