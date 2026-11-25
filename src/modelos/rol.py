class Rol:
    """
    Aca de define los roles dentro del sistema (por ejemplo: administrador,
    medico, enfermero) y se agrupa los permisos que estan relacionados utilizando
    conjuntos inmutables (frozenset)
    """

    def __init__(self, id_rol, nombre, permisos=None):
        self.__id_rol = id_rol
        self.__nombre = nombre
        # Usamos frozenset para asegurar que la lista de permisos no sea alterado por error
        self.__permisos = frozenset(permisos or [])

    def get_id_rol(self):
        return self.__id_rol

    def get_nombre(self):
        return self.__nombre

    def get_permisos(self):
        return self.__permisos

    def tiene_permiso(self, permiso):
        """ 
        Retorna true si el permiso consultante se encuentra dentro de los permisos
        del rol
        """
        return permiso in self.__permisos
