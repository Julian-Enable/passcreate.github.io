#!/usr/bin/env python3
"""
Sistema de backup para GenPassw Pro
"""

import os
import shutil
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from cryptography.fernet import Fernet

def get_encryption_key():
    """Obtener clave de encriptación"""
    key_file = 'encryption.key'
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            return f.read()
    return None

def create_backup():
    """Crear backup completo de la aplicación"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path("backups") / f"backup_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"💾 Creando backup en: {backup_dir}")
    
    # Backup de la base de datos
    if os.path.exists("passwords.db"):
        db_backup = backup_dir / "passwords.db"
        shutil.copy2("passwords.db", db_backup)
        print("✅ Base de datos respaldada")
    
    # Backup de la clave de encriptación
    if os.path.exists("encryption.key"):
        key_backup = backup_dir / "encryption.key"
        shutil.copy2("encryption.key", key_backup)
        print("✅ Clave de encriptación respaldada")
    
    # Backup de configuración
    if os.path.exists(".env"):
        env_backup = backup_dir / ".env"
        shutil.copy2(".env", env_backup)
        print("✅ Configuración respaldada")
    
    # Crear archivo de metadatos del backup
    metadata = {
        "timestamp": timestamp,
        "datetime": datetime.now().isoformat(),
        "files": list(backup_dir.glob("*")),
        "version": "1.0.0"
    }
    
    with open(backup_dir / "backup_info.json", 'w') as f:
        json.dump(metadata, f, indent=2, default=str)
    
    print(f"✅ Backup completado: {backup_dir}")
    return backup_dir

def restore_backup(backup_path):
    """Restaurar desde un backup"""
    backup_dir = Path(backup_path)
    
    if not backup_dir.exists():
        print(f"❌ Backup no encontrado: {backup_path}")
        return False
    
    print(f"🔄 Restaurando desde: {backup_dir}")
    
    # Restaurar base de datos
    db_backup = backup_dir / "passwords.db"
    if db_backup.exists():
        shutil.copy2(db_backup, "passwords.db")
        print("✅ Base de datos restaurada")
    
    # Restaurar clave de encriptación
    key_backup = backup_dir / "encryption.key"
    if key_backup.exists():
        shutil.copy2(key_backup, "encryption.key")
        print("✅ Clave de encriptación restaurada")
    
    # Restaurar configuración
    env_backup = backup_dir / ".env"
    if env_backup.exists():
        shutil.copy2(env_backup, ".env")
        print("✅ Configuración restaurada")
    
    print("✅ Restauración completada")
    return True

def list_backups():
    """Listar backups disponibles"""
    backup_dir = Path("backups")
    if not backup_dir.exists():
        print("❌ No hay directorio de backups")
        return
    
    backups = [d for d in backup_dir.iterdir() if d.is_dir() and d.name.startswith("backup_")]
    
    if not backups:
        print("📋 No hay backups disponibles")
        return
    
    print("📋 Backups disponibles:")
    for backup in sorted(backups, reverse=True):
        info_file = backup / "backup_info.json"
        if info_file.exists():
            with open(info_file, 'r') as f:
                info = json.load(f)
                print(f"  📁 {backup.name} - {info.get('datetime', 'N/A')}")
        else:
            print(f"  📁 {backup.name}")

def main():
    """Función principal"""
    import sys
    
    if len(sys.argv) < 2:
        print("🔐 GenPassw Pro - Sistema de Backup")
        print("Uso:")
        print("  python utils/backup.py create    # Crear backup")
        print("  python utils/backup.py list      # Listar backups")
        print("  python utils/backup.py restore <backup_path>  # Restaurar backup")
        return
    
    command = sys.argv[1]
    
    if command == "create":
        create_backup()
    elif command == "list":
        list_backups()
    elif command == "restore":
        if len(sys.argv) < 3:
            print("❌ Especifica el path del backup a restaurar")
            return
        restore_backup(sys.argv[2])
    else:
        print(f"❌ Comando desconocido: {command}")

if __name__ == '__main__':
    main()
