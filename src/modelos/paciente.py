from src.utils.seguridad import generar_hash
from src.modelos.historial_clinico import HistorialClinico

class Paciente:
    """
    Representa a un paciente del sistema clinico, manejando sus datos personales,
    la seguridad de su DNI mediante hashes y su propio objeto de HistorialClinico.
    """
    def __init__(self, id_paciente, nombre, dni=None,
                 dni_hash=None):
        self.__id_paciente = id_paciente
        self.__nombre = nombre

        # Manejo seguro del DNI: acepta un hash directo o genera uno nuevo a partir
        # del DNI en texto plano
        if dni_hash is not None:
            self.__dni_hash = dni_hash
        elif dni is not None:
            self.__dni_hash = generar_hash(dni)
        else:
            raise ValueError("Se requiere un DNI o su hash.")
            
        # Composicion: cada paciente nace con su propio historial clinico vinculado
        self.__historial = HistorialClinico(
            id_historial=None,
            id_paciente=id_paciente
        )

    def get_id_paciente(self):
        return self.__id_paciente

    def get_nombre(self):
        return self.__nombre

    def get_dni_hash(self):
        return self.__dni_hash

    def get_historial(self):
        return self.__historial

    def agregar_nota_historial(self, nota):
        """
        Validamos que la nota no este vacia antes de añadirlo al historial
        del paciente
        """
        if not nota or not nota.strip():
            raise ValueError("La nota médica no puede estar vacía.")

        #Método de compatibilidad para notas en memoria.
        #Los registros persistentes se agregan desde HistorialServicio
        self.__historial._agregar_nota_compatibilidad(
            nota.strip()
        )
