#!/usr/bin/env python3
"""
Script de instalación para GenPassw Pro
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Mostrar banner de bienvenida"""
    print("🔐 GenPassw Pro - Instalador")
    print("=" * 40)
    print("Gestor de Contraseñas Seguro")
    print("=" * 40)

def check_python_version():
    """Verificar versión de Python"""
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def install_dependencies():
    """Instalar dependencias de Python"""
    print("\n📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False

def setup_environment():
    """Configurar archivo .env"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✅ Archivo .env ya existe")
        return True
    
    if env_example.exists():
        print("\n🔧 Configurando variables de entorno...")
        shutil.copy(env_example, env_file)
        print("✅ Archivo .env creado desde env.example")
        print("⚠️  Recuerda editar .env con tus configuraciones")
        return True
    else:
        print("⚠️  No se encontró env.example, creando .env básico...")
        with open(env_file, 'w') as f:
            f.write("SECRET_KEY=dev-secret-key-change-in-production\n")
            f.write("FLASK_ENV=development\n")
            f.write("FLASK_DEBUG=True\n")
        print("✅ Archivo .env básico creado")
        return True

def create_directories():
    """Crear directorios necesarios"""
    directories = ['logs', 'backups', 'uploads']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Directorios creados")

def main():
    """Función principal de instalación"""
    print_banner()
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Instalar dependencias
    if not install_dependencies():
        sys.exit(1)
    
    # Configurar entorno
    setup_environment()
    
    # Crear directorios
    create_directories()
    
    print("\n🎉 ¡Instalación completada!")
    print("\n📋 Próximos pasos:")
    print("1. Edita el archivo .env con tus configuraciones")
    print("2. Ejecuta: python run.py")
    print("3. Abre http://localhost:5000 en tu navegador")
    print("\n🔐 ¡Disfruta usando GenPassw Pro!")

if __name__ == '__main__':
    main()
