import os
import string
import random
import base64
import bcrypt
from cryptography.fernet import Fernet

# Carpeta de contraseñas en el escritorio
escritorio = os.path.expanduser("~/Escritorio")
carpeta_contraseñas = os.path.join(escritorio, "contraseñas")

# Función para generar una clave maestra aleatoria
def generar_clave_maestra():
    return base64.urlsafe_b64encode(os.urandom(32))

# Función para encriptar una contraseña
def encriptar_contraseña(contraseña, clave_maestra):
    f = Fernet(clave_maestra)
    return f.encrypt(contraseña.encode()).decode()

# Función para desencriptar una contraseña
def desencriptar_contraseña(contraseña_encriptada, clave_maestra):
    f = Fernet(clave_maestra)
    return f.decrypt(contraseña_encriptada.encode()).decode()

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
    # Generar la clave maestra y encriptar la contraseña
    clave_maestra = generar_clave_maestra()
    contrasena = "".join(random.choice(caracteres) for i in range(longitud))
    print("La contraseña generada es: " + contrasena)

    # Encriptar la contraseña antes de guardarla
    contraseña_encriptada = encriptar_contraseña(contrasena, clave_maestra)

    # Crear o actualizar un archivo de texto con la información de la contraseña en el escritorio
    archivo_contraseña = os.path.join(carpeta_contraseñas, "contraseñas.txt")
    with open(archivo_contraseña, "a") as archivo:
        archivo.write(f"Correo: {correo}\n")
        archivo.write(f"Página: {pagina}\n")
        archivo.write(f"Contraseña encriptada: {contraseña_encriptada}\n\n")

    print(f"La información se ha guardado en {archivo_contraseña} en el escritorio.")

    # Desencriptar la contraseña (ejemplo)
    contraseña_desencriptada = desencriptar_contraseña(contraseña_encriptada, clave_maestra)
    print("Contraseña desencriptada:", contraseña_desencriptada)
