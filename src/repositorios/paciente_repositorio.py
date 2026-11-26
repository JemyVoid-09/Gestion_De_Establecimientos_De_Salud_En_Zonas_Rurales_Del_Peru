from src.repositorios.base_repositorio import BaseRepositorio
from src.modelos.paciente import Paciente

class PacienteRepositorio(BaseRepositorio):

    def generar_siguiente_id(self):
        # Obtener los identificadores de los pacientes registrados.
        consulta = "SELECT id_paciente FROM pacientes"
        filas = self.conexion.execute(consulta).fetchall()
        
        # Identificar el número más alto de los ID existentes.
        numeros = [
            int(fila["id_paciente"][1:])
            for fila in filas
            if fila["id_paciente"].startswith("P")
            and fila["id_paciente"][1:].isdigit()
        ]
        
        # Generar el siguiente ID con el formato P001.
        siguiente_numero = max(numeros, default=0) + 1
        
        return f"P{siguiente_numero:03d}"

    def registrar(self, paciente):
        # Preparar la consulta para guardar los datos del paciente.
        consulta = """
            INSERT INTO pacientes (id_paciente, nombre, dni_hash)
            VALUES (?, ?, ?)
        """

        self.conexion.execute(
            consulta,
            (
                paciente.get_id_paciente(),
                paciente.get_nombre(),
                paciente.get_dni_hash()
            )
        )

        self.conexion.commit()

    def obtener_todos(self):
        # Obtener todos los pacientes ordenados alfabéticamente por nombre.
        consulta = "SELECT * FROM pacientes ORDER BY nombre"
        filas = self.conexion.execute(consulta).fetchall()

        # Convertir los resultados en objetos Paciente.
        return [
            Paciente(
                fila["id_paciente"],
                fila["nombre"],
                dni_hash=fila["dni_hash"]
            )
            for fila in filas
        ]

    def buscar_por_nombre(self, criterio):
        # Buscar pacientes cuyo nombre coincida con el criterio ingresado.
        consulta = """
            SELECT * FROM pacientes
            WHERE LOWER(nombre) LIKE LOWER(?)
            ORDER BY nombre
        """

        filas = self.conexion.execute(
            consulta, (f"%{criterio}%",)
        ).fetchall()

        # Convertir los resultados encontrados en objetos Paciente.
        return [
            Paciente(
                fila["id_paciente"],
                fila["nombre"],
                dni_hash=fila["dni_hash"]
            )
            for fila in filas
        ]

    def buscar_por_id(self, id_paciente):
        # Consultar los datos de un paciente mediante su identificador.
        consulta = """
            SELECT * FROM pacientes
            WHERE id_paciente = ?
        """

        fila = self.conexion.execute(
            consulta, (id_paciente,)
        ).fetchone()

        # Retornar None si no se encuentra el paciente.
        if fila is None:
            return None

        # Reconstruir el registro encontrado como un objeto Paciente.
        return Paciente(
            fila["id_paciente"],
            fila["nombre"],
            dni_hash=fila["dni_hash"]
        )
