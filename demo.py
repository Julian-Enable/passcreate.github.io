#!/usr/bin/env python3
"""
Script de demostración para GenPassw Pro
Este script muestra las principales funcionalidades de la aplicación
"""

import os
import sys
import string
import random
from datetime import datetime

def print_banner():
    """Imprimir banner de bienvenida"""
    print("=" * 60)
    print("🔐 GENPASSW PRO - DEMOSTRACIÓN")
    print("=" * 60)
    print("Gestor de Contraseñas Seguro y Moderno")
    print("=" * 60)

def generate_demo_password(length=16, include_uppercase=True, include_lowercase=True, 
                          include_numbers=True, include_symbols=True):
    """Generar contraseña de demostración"""
    characters = ""
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_numbers:
        characters += string.digits
    if include_symbols:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not characters:
        characters = string.ascii_letters + string.digits
    
    # Asegurar que al menos hay un carácter de cada tipo seleccionado
    password = ""
    if include_uppercase:
        password += random.choice(string.ascii_uppercase)
    if include_lowercase:
        password += random.choice(string.ascii_lowercase)
    if include_numbers:
        password += random.choice(string.digits)
    if include_symbols:
        password += random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?")
    
    # Completar el resto de la contraseña
    remaining_length = length - len(password)
    password += ''.join(random.choice(characters) for _ in range(remaining_length))
    
    # Mezclar la contraseña
    password_list = list(password)
    random.shuffle(password_list)
    return ''.join(password_list)

def validate_password_strength(password):
    """Validar la fortaleza de una contraseña"""
    checks = {
        'length': len(password) >= 8,
        'uppercase': any(c.isupper() for c in password),
        'lowercase': any(c.islower() for c in password),
        'numbers': any(c.isdigit() for c in password),
        'symbols': any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    }
    
    score = sum(checks.values())
    
    if score <= 2:
        return "Débil", "🔴"
    elif score <= 3:
        return "Media", "🟡"
    elif score <= 4:
        return "Fuerte", "🟢"
    else:
        return "Muy Fuerte", "🟢"

def demo_password_generation():
    """Demostrar generación de contraseñas"""
    print("\n🎯 DEMOSTRACIÓN: Generación de Contraseñas")
    print("-" * 50)
    
    # Generar diferentes tipos de contraseñas
    configs = [
        ("Contraseña básica (8 caracteres)", 8, True, True, True, False),
        ("Contraseña estándar (16 caracteres)", 16, True, True, True, True),
        ("Contraseña fuerte (32 caracteres)", 32, True, True, True, True),
        ("Contraseña solo números (12 caracteres)", 12, False, False, True, False),
        ("Contraseña alfanumérica (20 caracteres)", 20, True, True, True, False)
    ]
    
    for name, length, upper, lower, numbers, symbols in configs:
        password = generate_demo_password(length, upper, lower, numbers, symbols)
        strength, icon = validate_password_strength(password)
        
        print(f"\n{name}:")
        print(f"  Contraseña: {password}")
        print(f"  Longitud: {len(password)} caracteres")
        print(f"  Fortaleza: {icon} {strength}")
        
        # Mostrar configuración
        config_parts = []
        if upper: config_parts.append("Mayúsculas")
        if lower: config_parts.append("Minúsculas")
        if numbers: config_parts.append("Números")
        if symbols: config_parts.append("Símbolos")
        print(f"  Configuración: {', '.join(config_parts)}")

def demo_features():
    """Demostrar características principales"""
    print("\n✨ CARACTERÍSTICAS PRINCIPALES")
    print("-" * 50)
    
    features = [
        ("🔒 Encriptación AES-256", "Todas las contraseñas se almacenan encriptadas"),
        ("👤 Autenticación de usuarios", "Sistema de login/registro seguro"),
        ("🔑 Contraseña maestra", "Acceso protegido a todas las contraseñas"),
        ("📊 Categorización", "Organiza contraseñas por categorías"),
        ("🔍 Búsqueda inteligente", "Busca por correo, sitio web o categoría"),
        ("📱 Interfaz responsive", "Funciona en móviles y tablets"),
        ("💾 Exportación", "Exporta en formato JSON y CSV"),
        ("🎨 Diseño moderno", "Interfaz elegante con animaciones"),
        ("⚡ Generación rápida", "Contraseñas seguras en tiempo real"),
        ("🛡️ Validación de fortaleza", "Indicador visual de seguridad")
    ]
    
    for feature, description in features:
        print(f"{feature}: {description}")

def demo_usage_instructions():
    """Mostrar instrucciones de uso"""
    print("\n🚀 INSTRUCCIONES DE USO")
    print("-" * 50)
    
    steps = [
        ("1. Instalar dependencias", "pip install -r requirements.txt"),
        ("2. Ejecutar la aplicación", "python run.py"),
        ("3. Abrir navegador", "http://localhost:5000"),
        ("4. Registrar cuenta", "Crear usuario y contraseña maestra"),
        ("5. Generar contraseñas", "Usar el panel de generación"),
        ("6. Guardar y gestionar", "Organizar por categorías"),
        ("7. Exportar datos", "Backup en JSON o CSV")
    ]
    
    for step, command in steps:
        print(f"{step}: {command}")

def demo_security_features():
    """Demostrar características de seguridad"""
    print("\n🛡️ CARACTERÍSTICAS DE SEGURIDAD")
    print("-" * 50)
    
    security_features = [
        "Encriptación AES-256 para contraseñas almacenadas",
        "Hashing bcrypt para contraseñas de usuario",
        "Sesiones seguras con cookies encriptadas",
        "Protección contra inyección SQL",
        "Sanitización de inputs",
        "Validación de tipos de datos",
        "Protección CSRF",
        "Contraseñas maestras separadas",
        "Claves de encriptación únicas por instalación",
        "Logout automático por inactividad"
    ]
    
    for i, feature in enumerate(security_features, 1):
        print(f"{i}. {feature}")

def main():
    """Función principal de demostración"""
    print_banner()
    
    # Verificar si la aplicación está instalada
    try:
        import flask
        import flask_sqlalchemy
        import cryptography
        print("✅ Dependencias detectadas - Aplicación lista para usar")
    except ImportError:
        print("❌ Dependencias no encontradas")
        print("Ejecuta: pip install -r requirements.txt")
        return
    
    # Ejecutar demostraciones
    demo_password_generation()
    demo_features()
    demo_security_features()
    demo_usage_instructions()
    
    print("\n" + "=" * 60)
    print("🎉 ¡DEMOSTRACIÓN COMPLETADA!")
    print("=" * 60)
    print("Para usar la aplicación completa:")
    print("1. Ejecuta: python run.py")
    print("2. Abre: http://localhost:5000")
    print("3. ¡Disfruta de GenPassw Pro!")
    print("=" * 60)

if __name__ == '__main__':
    main()
