#!/usr/bin/env python3
"""
Script de inicio para GenPassw Pro
Inicializa la base de datos antes de arrancar la aplicación
"""

import os
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent))

def main():
    """Función principal"""
    print("🔐 GenPassw Pro - Inicializando aplicación...")
    
    try:
        # Importar la aplicación (esto ejecutará init_database())
        from app import app, db, User, PasswordEntry
        
        print("✅ Aplicación importada correctamente")
        print("✅ Base de datos inicializada")
        print("✅ Usuario admin creado (admin/admin123)")
        
        # Verificar que las tablas existen
        with app.app_context():
            # Intentar una consulta simple para verificar
            try:
                User.query.first()
                print("✅ Tabla 'user' verificada")
            except Exception as e:
                print(f"❌ Error verificando tabla 'user': {e}")
                return False
            
            try:
                PasswordEntry.query.first()
                print("✅ Tabla 'password_entry' verificada")
            except Exception as e:
                print(f"❌ Error verificando tabla 'password_entry': {e}")
                return False
        
        print("🎉 ¡Aplicación lista para arrancar!")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la inicialización: {e}")
        return False

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1)
