import os
import string
import random
import bcrypt
from cryptography.fernet import Fernet
salt = bcrypt.gensalt()

# Carpeta de contraseñas en el escritorio
escritorio = os.path.expanduser("~/Escritorio")
carpeta_contraseñas = os.path.join(escritorio, "contraseñas")

# Crear la carpeta si no existe
if not os.path.exists(carpeta_contraseñas):
    os.makedirs(carpeta_contraseñas)

# Clave maestra para encriptar contraseñas
clave_maestra = input("Ingrese la clave maestra: ")
clave_maestra = clave_maestra.encode()  # Convertir la clave a bytes

# Función para encriptar una contraseña
def encriptar_contraseña(contraseña):
    f = Fernet(base64.urlsafe_b64encode(clave_maestra))
    return f.encrypt(contraseña.encode()).decode()

# Función para desencriptar una contraseña
def desencriptar_contraseña(contraseña_encriptada):
    f = Fernet(base64.urlsafe_b64encode(clave_maestra))
    return f.decrypt(contraseña_encriptada.encode()).decode()

# Función para autenticar al usuario con la clave maestra
def autenticar_usuario():
    global clave_maestra
    intentos = 3

    while intentos > 0:
        entrada = input("Ingrese la clave maestra para acceder a las contraseñas: ")
        entrada = entrada.encode()

        # Verificar la clave maestra
        if bcrypt.checkpw(entrada, clave_maestra):
            print("Autenticación exitosa.")
            return True
        else:
            print("Clave maestra incorrecta. Intentos restantes:", intentos)
            intentos -= 1

    print("Demasiados intentos fallidos. Saliendo.")
    return False

# Autenticar al usuario antes de continuar
if not autenticar_usuario():
    exit()

# Obtener el tamaño de la contraseña
longitud = int(input("Ingrese el tamaño de la contraseña: "))

# Preguntar para qué correo y página se usará la contraseña
correo = input("Para qué correo se utilizará esta contraseña: ")
pagina = input("Para qué página se utilizará esta contraseña: ")

# Preguntar qué caracteres incluir en la contraseña
permitir_mayusculas = input("¿Desea incluir letras mayúsculas en la contraseña? (S/N): ").lower() == "s"
permitir_minusculas = input("¿Desea incluir letras minúsculas en la contraseña? (S/N): ").lower() == "s"
permitir_numeros = input("¿Desea incluir números en la contraseña? (S/N): ").lower() == "s"

caracteres = ""

if permitir_mayusculas:
    caracteres += string.ascii_uppercase
if permitir_minusculas:
    caracteres += string.ascii_lowercase
if permitir_numeros:
    caracteres += string.digits

if not caracteres:
    print("No se han seleccionado opciones válidas para la contraseña.")
else:
    # Generar la contraseña
    contrasena = "".join(random.choice(caracteres) for i in range(longitud))
    print("La contraseña generada es: " + contrasena)

    # Encriptar la contraseña antes de guardarla
    contraseña_encriptada = encriptar_contraseña(contrasena)

    # Crear o actualizar un archivo de texto con la información de la contraseña en el escritorio
    archivo_contraseña = os.path.join(carpeta_contraseñas, "contraseñas.txt")
    with open(archivo_contraseña, "a") as archivo:
        archivo.write(f"Correo: {correo}\n")
        archivo.write(f"Página: {pagina}\n")
        archivo.write(f"Contraseña encriptada: {contraseña_encriptada}\n\n")

    print(f"La información se ha guardado en {archivo_contraseña} en el escritorio.")