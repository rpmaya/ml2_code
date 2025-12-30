from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier, RSAKeyPair
import os

# Cargar o generar par de claves
KEYPAIR_FILE = "mcp_keypair.json"

if os.path.exists(KEYPAIR_FILE):
    keypair = RSAKeyPair.load(KEYPAIR_FILE)
else:
    keypair = RSAKeyPair.generate()
    keypair.save(KEYPAIR_FILE)
    
    # Crear token inicial para el cliente
    client_token = keypair.create_token(
        subject="cliente-autorizado",
        issuer="mi-mcp-server",
        audience="mi-mcp"
    )
    
    # Guardar token para el cliente
    with open("client_token.txt", "w") as f:
        f.write(client_token)
    
    print(f"Token de cliente guardado en client_token.txt")

# Configurar verificador JWT
auth = JWTVerifier(
    public_key=keypair.public_key,
    issuer="mi-mcp-server",      # Debe coincidir con el token
    audience="mi-mcp"             # Debe coincidir con el token
)

# Crear servidor con autenticación
mcp = FastMCP("Servidor Seguro", auth=auth)


@mcp.tool
def operacion_protegida(dato: str) -> dict:
    """
    Esta herramienta solo es accesible con un token válido.
    """
    return {"status": "ok", "dato_procesado": dato.upper()}


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8080, path="/mcp")
