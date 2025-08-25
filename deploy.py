#!/usr/bin/env python3
"""
Script de verificación para despliegue
"""

import os
import sys
from pathlib import Path

def check_deployment_files():
    """Verificar archivos necesarios para despliegue"""
    required_files = [
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'render.yaml',
        'app.py',
        'config.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
        return False
    
    print("✅ Todos los archivos de despliegue están presentes")
    return True

def check_requirements():
    """Verificar dependencias de producción"""
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    required_deps = ['gunicorn', 'psycopg2-binary']
    missing_deps = []
    
    for dep in required_deps:
        if dep not in content:
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"❌ Dependencias faltantes: {', '.join(missing_deps)}")
        return False
    
    print("✅ Todas las dependencias de producción están incluidas")
    return True

def check_config():
    """Verificar configuración de producción"""
    try:
        from config import Config
        config = Config()
        
        # Verificar que la configuración de producción existe
        if hasattr(config, 'SECRET_KEY'):
            print("✅ Configuración de producción verificada")
            return True
        else:
            print("❌ Configuración de producción incompleta")
            return False
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def main():
    """Función principal"""
    print("🔐 GenPassw Pro - Verificación de Despliegue")
    print("=" * 50)
    
    checks = [
        check_deployment_files(),
        check_requirements(),
        check_config()
    ]
    
    if all(checks):
        print("\n🎉 ¡Todo listo para el despliegue!")
        print("\n📋 Pasos para desplegar:")
        print("1. Sube tu código a GitHub")
        print("2. Ve a render.com y crea una cuenta")
        print("3. Conecta tu repositorio de GitHub")
        print("4. Selecciona 'Web Service'")
        print("5. Configura las variables de entorno")
        print("6. ¡Despliega!")
    else:
        print("\n❌ Hay problemas que resolver antes del despliegue")
        sys.exit(1)

if __name__ == '__main__':
    main()
