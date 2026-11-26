from getpass import getpass

from src.servicios.autenticacion_servicio import AutenticacionServicio

def main():
    # Inicializa el servicio encargado de la autenticación y gestión de usuarios.
    servicio = AutenticacionServicio()

    print("--- AUTENTICACIÓN DEL ADMINISTRADOR ---")

    # Solicita las credenciales del administrador.
    nombre_admin = input("Usuario administrador: ").strip()
    contrasena_admin = getpass("Contraseña: ")

    # Verifica las credenciales ingresadas.
    administrador = servicio.autenticar(
        nombre_admin,
        contrasena_admin
    )

    # Detiene el proceso si las credenciales son incorrectas.
    if administrador is None:
        print("Credenciales incorrectas.")
        return

    # Comprueba que el administrador tenga permiso para gestionar usuarios.
    if not administrador.tiene_permiso("gestionar_usuarios"):
        print("No tiene permiso para crear usuarios.")
        return

    print("\n--- REGISTRO DE NUEVO USUARIO ---")

    # Solicita los datos de acceso del nuevo usuario.
    nombre = input("Nombre de usuario: ").strip()
    contrasena = getpass("Contraseña: ")
    confirmar = getpass("Confirmar contraseña: ")

    # Verifica que ambas contraseñas coincidan.
    if contrasena != confirmar:
        print("Las contraseñas no coinciden.")
        return

    # Muestra los roles disponibles para asignar al nuevo usuario.
    print("\nRoles disponibles:")
    print("1. Administrador")
    print("2. Medico")
    print("3. Recepcionista")

    opcion = input("Seleccione el rol: ").strip()

    # Relaciona cada opción del menú con el nombre de su rol.
    roles = {
        "1": "Administrador",
        "2": "Medico",
        "3": "Recepcionista"
    }

    # Obtiene el rol seleccionado por el administrador.
    nombre_rol = roles.get(opcion)

    # Detiene el proceso si la opción ingresada no es válida.
    if nombre_rol is None:
        print("Opción no válida.")
        return

    try:
        # Registra al nuevo usuario con sus credenciales y el rol seleccionado.
        servicio.crear_usuario(nombre, contrasena, nombre_rol)
        print("Usuario registrado correctamente.")

    except ValueError as error:
        # Muestra los errores relacionados con el registro del usuario.
        print(f"Error: {error}")

# Ejecuta el registro únicamente cuando el archivo se inicia directamente.
if __name__ == "__main__":
    main()
