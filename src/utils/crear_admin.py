from getpass import getpass
from src.servicios.autenticacion_servicio import AutenticacionServicio

def main():
    # Inicializar el servicio de autenticación.
    servicio = AutenticacionServicio()

    # Solicitar los datos para crear la cuenta de administrador.
    nombre = input("Nombre de usuario administrador: ").strip()
    contrasena = getpass("Contraseña: ")
    confirmar = getpass("Confirmar contraseña: ")

    # Verificar que ambas contraseñas coincidan.
    if contrasena != confirmar:
        print("Las contraseñas no coinciden.")
        return

    try:
        # Crear el usuario con el rol de administrador.
        servicio.crear_usuario(
            nombre,
            contrasena,
            "Administrador"
        )

        print("Usuario administrador creado correctamente.")

    except ValueError as error:
        # Mostrar los errores producidos durante la creación de la cuenta.
        print(f"Error: {error}")

# Ejecutar el programa cuando se inicie directamente este archivo.
if __name__ == "__main__":
    main()
