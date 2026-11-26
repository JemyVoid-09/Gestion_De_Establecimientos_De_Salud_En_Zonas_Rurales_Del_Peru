from src.repositorios.base_repositorio import BaseRepositorio
from src.modelos.rol import Rol

class RolRepositorio(BaseRepositorio):

    # Definir los roles disponibles y los permisos asignados a cada uno.
    ROLES_PREDETERMINADOS = {
        "ADMIN": {
            "nombre": "Administrador",
            "permisos": [
                "registrar_paciente",
                "consultar_paciente",
                "editar_paciente",
                "consultar_historial",
                "registrar_diagnostico",
                "gestionar_usuarios",
                "gestionar_citas"
            ]
        },
        "MEDICO": {
            "nombre": "Medico",
            "permisos": [
                "consultar_paciente",
                "consultar_historial",
                "registrar_diagnostico",
                "gestionar_citas"
            ]
        },
        "RECEPCIONISTA": {
            "nombre": "Recepcionista",
            "permisos": [
                "registrar_paciente",
                "consultar_paciente",
                "gestionar_citas"
            ]
        }
    }

    def inicializar_roles(self):
        # Registrar los roles predeterminados si todavía no existen.
        for id_rol, datos in self.ROLES_PREDETERMINADOS.items():

            self.conexion.execute(
                """
                INSERT OR IGNORE INTO roles (id_rol, nombre)
                VALUES (?, ?)
                """,
                (id_rol, datos["nombre"])
            )

            # Registrar los permisos correspondientes a cada rol.
            for nombre_permiso in datos["permisos"]:

                self.conexion.execute(
                    """
                    INSERT OR IGNORE INTO permisos
                    (id_permiso, nombre)
                    VALUES (?, ?)
                    """,
                    (nombre_permiso, nombre_permiso)
                )

                # Establecer la relación entre el rol y sus permisos.
                self.conexion.execute(
                    """
                    INSERT OR IGNORE INTO rol_permisos
                    (id_rol, id_permiso)
                    VALUES (?, ?)
                    """,
                    (id_rol, nombre_permiso)
                )

        self.conexion.commit()

    def buscar_por_id(self, id_rol):
        # Buscar un rol mediante su identificador.
        fila = self.conexion.execute(
            """
            SELECT id_rol, nombre
            FROM roles
            WHERE id_rol = ?
            """,
            (id_rol,)
        ).fetchone()

        if fila is None:
            return None

        # Obtener los permisos asociados al rol encontrado.
        permisos = self.conexion.execute(
            """
            SELECT p.nombre
            FROM permisos p
            JOIN rol_permisos rp
                ON p.id_permiso = rp.id_permiso
            WHERE rp.id_rol = ?
            """,
            (id_rol,)
        ).fetchall()

        # Construir el objeto Rol con sus respectivos permisos.
        return Rol(
            fila["id_rol"],
            fila["nombre"],
            [permiso["nombre"] for permiso in permisos]
        )

    def buscar_por_nombre(self, nombre):
        # Buscar un rol por su nombre sin distinguir mayúsculas y minúsculas.
        fila = self.conexion.execute(
            """
            SELECT id_rol
            FROM roles
            WHERE LOWER(nombre) = LOWER(?)
            """,
            (nombre,)
        ).fetchone()

        if fila is None:
            return None

        # Recuperar el rol completo mediante su identificador.
        return self.buscar_por_id(fila["id_rol"])
