from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import os
import string
import random
import json
from datetime import datetime
import base64
from config import config

# Determinar configuración basada en entorno
config_name = os.environ.get('FLASK_ENV', 'development')
if config_name == 'production':
    config_name = 'production'
elif config_name == 'testing':
    config_name = 'testing'
else:
    config_name = 'development'

app = Flask(__name__)
app.config.from_object(config[config_name])

db = SQLAlchemy(app)

# Función para inicializar base de datos (se ejecutará al final)
def init_database():
    """Inicializar la base de datos y crear clave de encriptación"""
    with app.app_context():
        try:
            # Crear todas las tablas
            db.create_all()
            print("✅ Base de datos inicializada correctamente")
            
            # Crear clave de encriptación si no existe
            key_file = 'encryption.key'
            if not os.path.exists(key_file):
                key = Fernet.generate_key()
                with open(key_file, 'wb') as f:
                    f.write(key)
                print("✅ Clave de encriptación generada")
            
            # Crear usuario admin por defecto si no existe
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@genpassw.com',
                    password_hash=generate_password_hash('admin123'),
                    master_password_hash=generate_password_hash('admin123')
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Usuario admin creado (admin/admin123)")
            
        except Exception as e:
            print(f"⚠️  Error al inicializar base de datos: {e}")

# Generar clave de encriptación
def get_encryption_key():
    key_file = 'encryption.key'
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
        return key

# Modelo de base de datos
class PasswordEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(200), nullable=False)
    password_encrypted = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='General')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    master_password_hash = db.Column(db.String(120), nullable=False)

# Funciones de utilidad
def encrypt_password(password):
    fernet = Fernet(get_encryption_key())
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    fernet = Fernet(get_encryption_key())
    return fernet.decrypt(encrypted_password.encode()).decode()

def generate_strong_password(length=16, include_uppercase=True, include_lowercase=True, 
                           include_numbers=True, include_symbols=True):
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

# Rutas
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                session['username'] = user.username
                return redirect(url_for('index'))
            else:
                flash('Usuario o contraseña incorrectos', 'error')
        except Exception as e:
            print(f"Error en login: {e}")
            flash('Error interno del servidor', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form.get('email', f'{username}@example.com')  # Email opcional
            password = request.form['password']
            master_password = request.form['master_password']
            
            if User.query.filter_by(username=username).first():
                flash('El usuario ya existe', 'error')
            else:
                user = User(
                    username=username,
                    email=email,
                    password_hash=generate_password_hash(password),
                    master_password_hash=generate_password_hash(master_password)
                )
                db.session.add(user)
                db.session.commit()
                flash('Usuario registrado exitosamente', 'success')
                return redirect(url_for('login'))
        except Exception as e:
            print(f"Error en registro: {e}")
            flash('Error interno del servidor', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/generate-password', methods=['POST'])
def generate_password():
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    data = request.json
    length = data.get('length', 16)
    include_uppercase = data.get('include_uppercase', True)
    include_lowercase = data.get('include_lowercase', True)
    include_numbers = data.get('include_numbers', True)
    include_symbols = data.get('include_symbols', True)
    
    password = generate_strong_password(
        length=length,
        include_uppercase=include_uppercase,
        include_lowercase=include_lowercase,
        include_numbers=include_numbers,
        include_symbols=include_symbols
    )
    
    return jsonify({'password': password})

@app.route('/api/save-password', methods=['POST'])
def save_password():
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    data = request.json
    email = data.get('email')
    website = data.get('website')
    password = data.get('password')
    category = data.get('category', 'General')
    notes = data.get('notes', '')
    
    if not all([email, website, password]):
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    
    encrypted_password = encrypt_password(password)
    
    entry = PasswordEntry(
        email=email,
        website=website,
        password_encrypted=encrypted_password,
        category=category,
        notes=notes
    )
    
    db.session.add(entry)
    db.session.commit()
    
    return jsonify({'message': 'Contraseña guardada exitosamente', 'id': entry.id})

@app.route('/api/passwords')
def get_passwords():
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = PasswordEntry.query
    
    if search:
        query = query.filter(
            db.or_(
                PasswordEntry.email.contains(search),
                PasswordEntry.website.contains(search),
                PasswordEntry.category.contains(search)
            )
        )
    
    if category:
        query = query.filter(PasswordEntry.category == category)
    
    entries = query.order_by(PasswordEntry.updated_at.desc()).all()
    
    result = []
    for entry in entries:
        result.append({
            'id': entry.id,
            'email': entry.email,
            'website': entry.website,
            'category': entry.category,
            'notes': entry.notes,
            'created_at': entry.created_at.isoformat(),
            'updated_at': entry.updated_at.isoformat()
        })
    
    return jsonify(result)

@app.route('/api/passwords/<int:password_id>', methods=['GET'])
def get_password(password_id):
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    entry = PasswordEntry.query.get_or_404(password_id)
    
    return jsonify({
        'id': entry.id,
        'email': entry.email,
        'website': entry.website,
        'password': decrypt_password(entry.password_encrypted),
        'category': entry.category,
        'notes': entry.notes,
        'created_at': entry.created_at.isoformat(),
        'updated_at': entry.updated_at.isoformat()
    })

@app.route('/api/passwords/<int:password_id>', methods=['DELETE'])
def delete_password(password_id):
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    entry = PasswordEntry.query.get_or_404(password_id)
    db.session.delete(entry)
    db.session.commit()
    
    return jsonify({'message': 'Contraseña eliminada exitosamente'})

@app.route('/api/categories')
def get_categories():
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    categories = db.session.query(PasswordEntry.category).distinct().all()
    return jsonify([cat[0] for cat in categories])

@app.route('/api/export')
def export_passwords():
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    entries = PasswordEntry.query.all()
    export_data = []
    
    for entry in entries:
        export_data.append({
            'email': entry.email,
            'website': entry.website,
            'password': decrypt_password(entry.password_encrypted),
            'category': entry.category,
            'notes': entry.notes,
            'created_at': entry.created_at.isoformat()
        })
    
    return jsonify(export_data)

# Manejo de errores
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Error interno del servidor'}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Recurso no encontrado'}), 404

@app.errorhandler(401)
def unauthorized_error(error):
    return jsonify({'error': 'No autorizado'}), 401

# Inicializar base de datos cuando se importa el módulo
init_database()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
