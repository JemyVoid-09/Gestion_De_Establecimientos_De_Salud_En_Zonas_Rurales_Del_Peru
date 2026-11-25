class CitaMedica: 
    """
    representa un cita medica dentro del sistema.
    Gestiona la informacion importante y permite controlar si la cita sigue activa o fue cancelada
    """
    def __init__(self, id_cita, paciente, fecha, medico):
        #Atributos privados para encapsular los datos de la cita
        self.__id_cita = id_cita
        self.__paciente = paciente
        self.__fecha = fecha
        self.__medico = medico
        self.__activa = True # Por defecto, toda cita nueva nace activa

    def get_id_cita(self):
        return self.__id_cita

    def get_paciente(self):
        return self.__paciente

    def get_fecha(self):
        return self.__fecha

    def get_medico(self):
        return self.__medico

    def get_estado(self):
        return self.__activa

    def cancelar_cita(self):
        """
        Cambia el estado de la cita a cancelada.
        lanza un error (valueError) si la cita ya habia sido cancelada previamente.
        """
        if not self.__activa:
            raise ValueError(
                "La cita ya se encontraba cancelada previamente."
            )

        self.__activa = False
