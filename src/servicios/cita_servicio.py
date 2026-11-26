from src.modelos.cita import CitaMedica
from src.repositorios.cita_repositorio import CitaRepositorio
from src.repositorios.paciente_repositorio import PacienteRepositorio

class CitaServicio:
    def __init__(self):
        # Inicializar los repositorios de citas y pacientes.
        self.repositorio = CitaRepositorio()
        self.pacientes = PacienteRepositorio()

    def programar_cita(self, id_cita, id_paciente, fecha, medico, usuario):
        # Verificar que el usuario tenga permiso para gestionar citas.
        if not usuario.tiene_permiso("gestionar_citas"):
            raise PermissionError("No tiene permiso para gestionar citas.")

        # Comprobar que los campos obligatorios estén completos.
        if not all([id_cita.strip(), fecha.strip(), medico.strip()]):
            raise ValueError("Todos los campos son obligatorios.")

        # Buscar al paciente al que se asignará la cita.
        paciente = self.pacientes.buscar_por_id(id_paciente)

        if paciente is None:
            raise ValueError("El paciente no existe.")

        # Crear y registrar la cita médica.
        cita = CitaMedica(id_cita, paciente, fecha, medico)
        self.repositorio.registrar(cita)

        return cita

    def obtener_citas(self, usuario):
        # Verificar que el usuario tenga permiso para consultar citas.
        if not usuario.tiene_permiso("gestionar_citas"):
            raise PermissionError("No tiene permiso para consultar citas.")

        # Recuperar todas las citas registradas.
        return self.repositorio.obtener_todas()

    def cancelar_cita(self, id_cita, usuario):
        # Verificar que el usuario tenga permiso para cancelar citas.
        if not usuario.tiene_permiso("gestionar_citas"):
            raise PermissionError("No tiene permiso para cancelar citas.")

        # Cancelar la cita si existe y todavía está activa.
        if not self.repositorio.cancelar(id_cita):
            raise ValueError(
                "La cita no existe o ya está cancelada."
            )
