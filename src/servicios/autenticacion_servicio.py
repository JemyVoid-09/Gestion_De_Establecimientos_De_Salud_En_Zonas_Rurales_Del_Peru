import uuid

from src.modelos.usuario import Usuario
from src.repositorios.usuario_repositorio import UsuarioRepositorio
from src.repositorios.rol_repositorio import RolRepositorio
from src.utils.seguridad import (
    generar_hash_contrasena,
    verificar_contrasena
)

class AutenticacionServicio:

    def __init__(self):
        # Inicializar los repositorios de usuarios y roles.
        self.usuarios = UsuarioRepositorio()
        self.roles = RolRepositorio()

        # Registrar los roles predeterminados en la base de datos.
        self.roles.inicializar_roles()

    def crear_usuario(self, nombre, contrasena, nombre_rol):
        # Verificar que el nombre de usuario no esté vacío.
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de usuario es obligatorio.")

        # Validar que la contraseña tenga la longitud mínima requerida.
        if not contrasena or len(contrasena) < 8:
            raise ValueError(
                "La contraseña debe tener al menos 8 caracteres."
            )

        # Comprobar que el nombre de usuario no esté registrado.
        if self.usuarios.buscar_por_nombre(nombre.strip()):
            raise ValueError("El nombre de usuario ya existe.")

        # Buscar el rol que se asignará al nuevo usuario.
        rol = self.roles.buscar_por_nombre(nombre_rol)

        if rol is None:
            raise ValueError("El rol indicado no existe.")

        # Crear el usuario con un identificador único y la contraseña protegida mediante hash.
        usuario = Usuario(
            str(uuid.uuid4()),
            nombre.strip(),
            generar_hash_contrasena(contrasena),
            rol
        )

        # Registrar el nuevo usuario en la base de datos.
        self.usuarios.registrar(usuario)
        return usuario

    def autenticar(self, nombre, contrasena):
        # Verificar que se hayan ingresado ambas credenciales.
        if not nombre or not contrasena:
            return None

        # Buscar la cuenta correspondiente al nombre ingresado.
        fila = self.usuarios.buscar_por_nombre(nombre.strip())

        if fila is None:
            return None

        # Impedir el acceso a cuentas desactivadas.
        if not fila["activo"]:
            return None

        # Comprobar que la contraseña ingresada coincida con el hash almacenado.
        if not verificar_contrasena(
            contrasena,
            fila["contraseña_hash"]
        ):
            return None

        # Recuperar el rol asignado al usuario.
        rol = self.roles.buscar_por_id(fila["id_rol"])

        if rol is None:
            return None

        # Retornar el objeto Usuario con sus datos y estado actual.
        return Usuario(
            fila["id_usuario"],
            fila["nombre"],
            fila["contraseña_hash"],
            rol,
            bool(fila["activo"])
        )

    def desactivar_usuario(self, id_usuario, administrador):
        # Verificar que el administrador tenga permiso para gestionar usuarios.
        if not administrador.tiene_permiso("gestionar_usuarios"):
            raise PermissionError(
                "No tiene permiso para gestionar usuarios."
            )

        # Desactivar la cuenta indicada.
        if not self.usuarios.actualizar_estado(id_usuario, False):
            raise ValueError("El usuario no existe.")
