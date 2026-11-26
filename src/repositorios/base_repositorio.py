from src.utils.database import obtener_conexion

class BaseRepositorio:
    # Inicializar la conexión a la base de datos para los repositorios.
    def __init__(self):
        self.conexion = obtener_conexion()
