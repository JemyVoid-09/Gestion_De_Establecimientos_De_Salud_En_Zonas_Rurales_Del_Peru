from src.repositorios.base_repositorio import BaseRepositorio
from src.modelos.cita import CitaMedica
from src.modelos.paciente import Paciente

class CitaRepositorio(BaseRepositorio):

    def registrar(self, cita):
        # Guardar los datos de la cita en la base de datos.
        self.conexion.execute(
            """
            INSERT INTO citas
            (id_cita, id_paciente, fecha, medico, activa)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                cita.get_id_cita(),
                cita.get_paciente().get_id_paciente(),
                cita.get_fecha(),
                cita.get_medico(),
                int(cita.get_estado())
            )
        )
        self.conexion.commit()

    def obtener_todas(self):
        # Obtener las citas junto con los datos de sus pacientes asociados.
        filas = self.conexion.execute(
            """
            SELECT c.*, p.nombre, p.dni_hash
            FROM citas c
            JOIN pacientes p
            ON c.id_paciente = p.id_paciente
            ORDER BY c.fecha
            """
        ).fetchall()

        citas = []

        # Reconstruir los objetos de paciente y cita a partir de los registros.
        for fila in filas:
            paciente = Paciente(
                fila["id_paciente"],
                fila["nombre"],
                dni_hash=fila["dni_hash"]
            )

            cita = CitaMedica(
                fila["id_cita"],
                paciente,
                fila["fecha"],
                fila["medico"]
            )

            # Restaurar el estado de las citas canceladas.
            if not fila["activa"]:
                cita.cancelar_cita()

            citas.append(cita)

        return citas

    def cancelar(self, id_cita):
        # Desactivar la cita únicamente si todavía está activa.
        cursor = self.conexion.execute(
            """
            UPDATE citas
            SET activa = 0
            WHERE id_cita = ? AND activa = 1
            """,
            (id_cita,)
        )

        self.conexion.commit()

        # Indicar si se logró cancelar una cita.
        return cursor.rowcount > 0
