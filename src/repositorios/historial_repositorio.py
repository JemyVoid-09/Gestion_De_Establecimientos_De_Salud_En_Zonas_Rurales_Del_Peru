import uuid
from src.repositorios.base_repositorio import BaseRepositorio
from src.modelos.historial_clinico import HistorialClinico

class HistorialRepositorio(BaseRepositorio):

    def obtener_o_crear(self, id_paciente):
        # Buscar si el paciente ya tiene un historial clínico registrado.
        fila = self.conexion.execute(
            """
            SELECT * FROM historiales_clinicos
            WHERE id_paciente = ?
            """,
            (id_paciente,)
        ).fetchone()

        if fila is None:
            # Generar un identificador único para el nuevo historial.
            id_historial = str(uuid.uuid4())

            self.conexion.execute(
                """
                INSERT INTO historiales_clinicos
                (id_historial, id_paciente)
                VALUES (?, ?)
                """,
                (id_historial, id_paciente)
            )
            self.conexion.commit()

            return HistorialClinico(id_historial, id_paciente)

        # Reconstruir el historial existente como un objeto.
        return HistorialClinico(
            fila["id_historial"],
            fila["id_paciente"]
        )

    def registrar(self, id_paciente, fecha, diagnostico,
                  observaciones, id_usuario):

        # Obtener el historial del paciente o crearlo si no existe.
        historial = self.obtener_o_crear(id_paciente)

        # Generar un identificador único para el registro clínico.
        id_registro = str(uuid.uuid4())

        # Guardar el diagnóstico y las observaciones en la base de datos.
        self.conexion.execute(
            """
            INSERT INTO registros_clinicos
            (id_registro, id_historial, fecha, diagnostico,
             observaciones, id_usuario)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                id_registro,
                historial.get_id_historial(),
                fecha,
                diagnostico,
                observaciones,
                id_usuario
            )
        )

        self.conexion.commit()
        return id_registro

    def obtener_por_paciente(self, id_paciente):
        # Obtener el historial clínico correspondiente al paciente.
        historial = self.obtener_o_crear(id_paciente)

        # Consultar los registros clínicos asociados al historial.
        filas = self.conexion.execute(
            """
            SELECT fecha, diagnostico, observaciones, id_usuario
            FROM registros_clinicos
            WHERE id_historial = ?
            ORDER BY fecha
            """,
            (historial.get_id_historial(),)
        ).fetchall()

        # Convertir los resultados de la consulta en diccionarios.
        registros = [dict(fila) for fila in filas]

        # Retornar el historial junto con sus registros clínicos.
        return HistorialClinico(
            historial.get_id_historial(),
            id_paciente,
            registros
        )
