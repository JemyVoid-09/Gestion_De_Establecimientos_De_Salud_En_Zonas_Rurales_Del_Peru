from datetime import datetime

from src.repositorios.historial_repositorio import HistorialRepositorio
from src.repositorios.paciente_repositorio import PacienteRepositorio

class HistorialServicio:

    def __init__(self):
        # Inicializar los repositorios de historiales clínicos y pacientes.
        self.repositorio = HistorialRepositorio()
        self.pacientes = PacienteRepositorio()

    def registrar_diagnostico(self, id_paciente, diagnostico,
                              observaciones, usuario):

        # Verificar que el usuario tenga permiso para registrar diagnósticos.
        if not usuario.tiene_permiso("registrar_diagnostico"):
            raise PermissionError(
                "No tiene permiso para registrar diagnósticos."
            )

        # Comprobar que el paciente esté registrado.
        paciente = self.pacientes.buscar_por_id(id_paciente)

        if paciente is None:
            raise ValueError("El paciente no existe.")

        # Validar que el diagnóstico contenga información.
        if not diagnostico or not diagnostico.strip():
            raise ValueError("El diagnóstico no puede estar vacío.")

        # Obtener la fecha y hora actuales para el registro clínico.
        fecha = datetime.now().isoformat(timespec="seconds")

        # Registrar el diagnóstico junto con el usuario responsable.
        return self.repositorio.registrar(
            id_paciente,
            fecha,
            diagnostico.strip(),
            observaciones,
            usuario.get_id_usuario()
        )

    def consultar_historial(self, id_paciente, usuario):

        # Verificar que el usuario tenga permiso para consultar historiales.
        if not usuario.tiene_permiso("consultar_historial"):
            raise PermissionError(
                "No tiene permiso para consultar historiales."
            )

        # Comprobar que el paciente exista antes de consultar su historial.
        paciente = self.pacientes.buscar_por_id(id_paciente)

        if paciente is None:
            raise ValueError("El paciente no existe.")

        # Recuperar el historial clínico del paciente.
        return self.repositorio.obtener_por_paciente(id_paciente)
