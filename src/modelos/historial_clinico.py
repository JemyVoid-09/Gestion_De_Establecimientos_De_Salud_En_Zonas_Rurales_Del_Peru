class HistorialClinico:
    """
    Aqui se Administra el historial médico de un paciente utilizando una lista de diccionarios 
    para guardar los diferentes registros y diagnosticos.
    """

    def __init__(self, id_historial, id_paciente, registros=None):
        #Validamos obligatoriamente que el historial este relacionado a un paciente
        if not id_paciente:
            raise ValueError("El historial debe pertenecer a un paciente.")

        self.__id_historial = id_historial
        self.__id_paciente = id_paciente
        #Si no se pasan los registros previos, inicializamos una lista vacia
        self.__registros = list(registros) if registros else []

    def get_id_historial(self):
        return self.__id_historial

    def get_id_paciente(self):
        return self.__id_paciente

    def get_registros(self):
        #se hara una copia de la lista para proteger la integridad de los datos originales
        #(encapsulamiento)
        return [registro.copy() for registro in self.__registros]

    def agregar_registro(self, fecha, diagnostico, observaciones, id_usuario):
        """
        se Añade un nuevo registro medico tras validar que el diagnostico y el ID del profesionarl responsable
        no esten vacion.
        """
        if not diagnostico or not diagnostico.strip():
            raise ValueError("El diagnóstico no puede estar vacío.")

        if not id_usuario:
            raise ValueError("Se requiere identificar al profesional responsable.")
        #Estructuramos el registro en formato diccionario
        registro = {
            "fecha": fecha,
            "diagnostico": diagnostico.strip(),
            "observaciones": observaciones.strip() if observaciones else "",
            "id_usuario": id_usuario
        }

        self.__registros.append(registro)
        
        return registro.copy()
    
    def _agregar_nota_compatibilidad(self, nota):
        """
        Utilizamos el metodo auxiliar de compatibilidad para notas rapidas en memoria.
        Nota: los registros persistentes principales se gestiona desde HistorialServicio.
        """
        registro = {
            "fecha": None,
            "diagnostico": nota,
            "observaciones": "",
            "id_usuario": None
        }

        self.__registros.append(registro)
        return registro.copy()
