import os
import string
import random

# Carpeta de contraseñas en el escritorio del usuario (compatible con Windows)
escritorio = os.path.expanduser("~/Desktop")  # Usamos "Desktop" en lugar de "Escritorio" en Windows
carpeta_contraseñas = os.path.join(escritorio, "contraseñaGenPassw")

# Crear la carpeta si no existe
if not os.path.exists(carpeta_contraseñas):
    os.makedirs(carpeta_contraseñas)

#Saludo
print("Bienvenido a GenPassw")
print("Este programa te permite generar contraseñas aleatorias y guardarlas en tu escritorio, esto junto a tu informacion de correo electronico usado y pagina las cuales estan enlazadas con la contraseña.")

while True:
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

        # Crear o actualizar un archivo de texto con la información de la contraseña en el escritorio
        archivo_contraseña = os.path.join(carpeta_contraseñas, "contraseñas.txt")
        with open(archivo_contraseña, "a") as archivo:
            archivo.write(f"Correo: {correo}\n")
            archivo.write(f"Página: {pagina}\n")
            archivo.write(f"Contraseña: {contrasena}\n\n")

        print(f"La información se ha guardado en {archivo_contraseña} en el escritorio.")

    respuesta = input("¿Desea generar otra contraseña? (S/N): ").lower()
    if respuesta != "s":
        break
