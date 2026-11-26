import hashlib
import secrets
import hmac

def generar_hash(texto):
    # Genera un hash SHA-256 del texto recibido.
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()

def generar_hash_contrasena(contrasena):
    # Evita generar un hash si la contraseña está vacía.
    if not contrasena:
        raise ValueError("La contraseña no puede estar vacía.")

    # Genera una sal aleatoria y define el número de iteraciones.
    sal = secrets.token_hex(16)
    iteraciones = 600000

    # Deriva un hash seguro de la contraseña mediante PBKDF2-HMAC-SHA256.
    resultado = hashlib.pbkdf2_hmac(
        "sha256",
        contrasena.encode("utf-8"),
        bytes.fromhex(sal),
        iteraciones
    )

    # Devuelve el algoritmo, las iteraciones, la sal y el hash generado.
    return f"pbkdf2_sha256${iteraciones}${sal}${resultado.hex()}"

def verificar_contrasena(contrasena, hash_guardado):
    try:
        # Recupera los componentes almacenados del hash de la contraseña.
        algoritmo, iteraciones, sal, hash_original = hash_guardado.split("$")

        # Comprueba que el algoritmo utilizado sea el esperado.
        if algoritmo != "pbkdf2_sha256":
            return False

        # Genera nuevamente el hash con la contraseña ingresada y la sal almacenada.
        resultado = hashlib.pbkdf2_hmac(
            "sha256",
            contrasena.encode("utf-8"),
            bytes.fromhex(sal),
            int(iteraciones)
        )

        # Compara ambos hashes de forma segura para evitar ataques de temporización.
        return hmac.compare_digest(
            resultado.hex(),
            hash_original
        )

    # Devuelve False si el formato del hash o los datos no son válidos.
    except (ValueError, TypeError):
        return False
