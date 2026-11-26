import sqlite3
from pathlib import Path

# Define las rutas principales del proyecto y de la base de datos.
RUTA_BASE = Path(__file__).resolve().parents[2]
RUTA_DATA = RUTA_BASE / "data"
RUTA_DB = RUTA_DATA / "gestion_essalud.db"

# Almacena la conexión compartida con la base de datos.
_conexion = None

def obtener_conexion():
    global _conexion

    # Crea la conexión únicamente si todavía no existe.
    if _conexion is None:
        # Crea la carpeta de datos si aún no está disponible.
        RUTA_DATA.mkdir(parents=True, exist_ok=True)

        # Establece la conexión con SQLite y permite acceder a las filas por nombre de columna.
        _conexion = sqlite3.connect(RUTA_DB)
        _conexion.row_factory = sqlite3.Row

        # Activa la comprobación de claves foráneas en la base de datos.
        _conexion.execute("PRAGMA foreign_keys = ON")

        # Crea las tablas necesarias si todavía no existen.
        inicializar_base_datos()

    return _conexion

def inicializar_base_datos():
    # Define la ubicación del script SQL que contiene la estructura de las tablas.
    ruta_sql = RUTA_DATA / "scripts" / "create_tables.sql"

    conexion = _conexion

    # Lee y ejecuta las instrucciones SQL para preparar la base de datos.
    with open(ruta_sql, "r", encoding="utf-8") as archivo:
        conexion.executescript(archivo.read())

    # Confirma los cambios realizados en la base de datos.
    conexion.commit()

def cerrar_conexion():
    global _conexion

    # Cierra la conexión y restablece la variable para permitir una nueva conexión.
    if _conexion is not None:
        _conexion.close()
        _conexion = None
