class Usuario:
    """
    Esto representa a una persona que accede al sistema.
    controlando su autenticacion (contraseña en formato hash), su rol
    y si su cuenta esta activa o bloqueada.
    """

    def __init__(self, id_usuario, nombre, contraseña_hash,
                 rol, activo=True):

        self.__id_usuario = id_usuario
        self.__nombre = nombre
        self.__contraseña_hash = contraseña_hash
        self.__rol = rol
        self.__activo = bool(activo)

    def get_id_usuario(self):
        return self.__id_usuario

    def get_nombre(self):
        return self.__nombre

    def get_rol(self):
        return self.__rol

    def esta_activo(self):
        return self.__activo

    def tiene_permiso(self, permiso):
        """
        Valida si el usuario puede realizar una accion:
        primero verifica si esta activo, si es asi, consulta con su rol asignado.
        """
        if not self.__activo:
            return False

        return self.__rol.tiene_permiso(permiso)

    def desactivar(self):
        """inabilita al usuario cambiando su estado a false."""
        self.__activo = False

    def activar(self):
        """Habilita nuevamente al usuario cambiando su estado a true"""
        self.__activo = True

    def _obtener_contraseña_hash(self):
        # Metodo interno para procesos de autenticacion y verificacion se seguridad
        return self.__contraseña_hash
