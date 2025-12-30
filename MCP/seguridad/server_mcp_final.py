"""
Servidor MCP con buenas prácticas de seguridad:
- Autenticación JWT obligatoria
- Validación de entrada
- Sanitización de datos
- Logging de operaciones
- Enviroments
"""

from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier, RSAKeyPair
import os
import logging
import re
import html

# Configurar logging a archivo de auditoría
logging.basicConfig(
    filename='mcp_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Añadir handler para consola también
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

# Constantes de seguridad
MAX_INPUT_LENGTH = 10000
KEYPAIR_FILE = "mcp_keypair.json"

# Configuración desde variables de entorno
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")


def sanitize(datos: str) -> str:
    """
    Sanitiza la entrada eliminando caracteres potencialmente peligrosos.
    """
    # Escapar caracteres HTML
    datos = html.escape(datos)

    # Eliminar caracteres de control (excepto newline y tab)
    datos = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', datos)

    return datos


def validar_entrada(datos: str, max_length: int = MAX_INPUT_LENGTH) -> tuple[bool, str]:
    """
    Valida la entrada y retorna (es_valido, mensaje_error).
    """
    if not datos:
        return False, "Datos vacíos"

    if len(datos) > max_length:
        return False, f"Datos demasiado grandes (máximo {max_length} caracteres)"

    return True, ""


# Cargar o generar par de claves RSA
if os.path.exists(KEYPAIR_FILE):
    keypair = RSAKeyPair.load(KEYPAIR_FILE)
    logger.info("Par de claves cargado desde archivo")
else:
    keypair = RSAKeyPair.generate()
    keypair.save(KEYPAIR_FILE)
    logger.info("Nuevo par de claves generado y guardado")

    # Crear token inicial para el cliente
    client_token = keypair.create_token(
        subject="cliente-autorizado",
        issuer="mi-mcp-server",
        audience="mi-mcp"
    )

    # Guardar token para el cliente
    with open("client_token.txt", "w") as f:
        f.write(client_token)

    logger.info("Token de cliente guardado en client_token.txt")

# Configurar verificador JWT
auth = JWTVerifier(
    public_key=keypair.public_key,
    issuer="mi-mcp-server",
    audience="mi-mcp"
)

# Crear servidor con autenticación obligatoria
mcp = FastMCP(
    "Servidor Seguro",
    auth=auth,  # Autenticación obligatoria
)


@mcp.tool
def operacion_sensible(datos: str) -> dict:
    """
    Herramienta con validación y sanitización de entrada.
    Solo accesible con token válido.
    """
    # Validar longitud de entrada
    es_valido, error = validar_entrada(datos)
    if not es_valido:
        logger.warning(f"Validación fallida: {error}")
        return {"error": error}

    # Sanitizar entrada
    datos_limpios = sanitize(datos)

    # Registrar operación
    logger.info(f"Operación ejecutada: {len(datos)} caracteres procesados")

    # Procesar datos
    resultado = {
        "status": "ok",
        "datos_procesados": datos_limpios.upper(),
        "longitud_original": len(datos),
        "longitud_procesada": len(datos_limpios)
    }

    return resultado


@mcp.tool
def consulta_segura(query: str) -> dict:
    """
    Ejemplo de consulta con validaciones de seguridad.
    """
    # Validar entrada con límite más restrictivo para consultas
    es_valido, error = validar_entrada(query, max_length=1000)
    if not es_valido:
        logger.warning(f"Consulta rechazada: {error}")
        return {"error": error}

    # Sanitizar
    query_limpia = sanitize(query)

    # Registrar
    logger.info(f"Consulta ejecutada: '{query_limpia[:50]}...'")

    return {
        "status": "ok",
        "query": query_limpia,
        "resultado": f"Resultado para: {query_limpia}"
    }


@mcp.tool
def herramienta_auditada(parametro: str) -> dict:
    """
    Herramienta con auditoría completa de invocaciones y errores.
    """
    # Registrar invocación
    logging.info(f"Tool invocada: herramienta_auditada, param={parametro[:50]}")

    try:
        # Validar entrada
        es_valido, error = validar_entrada(parametro)
        if not es_valido:
            logging.warning(f"Validación fallida en herramienta_auditada: {error}")
            return {"error": error}

        # Sanitizar y procesar
        parametro_limpio = sanitize(parametro)
        resultado = {
            "status": "ok",
            "parametro_procesado": parametro_limpio.upper(),
            "longitud": len(parametro_limpio)
        }

        logging.info("Resultado exitoso en herramienta_auditada")
        return resultado

    except Exception as e:
        logging.error(f"Error en herramienta_auditada: {str(e)}")
        raise


if __name__ == "__main__":
    logger.info(f"Iniciando servidor MCP seguro en {HOST}:{PORT}...")
    mcp.run(transport="http", host=HOST, port=PORT, path="/mcp")
