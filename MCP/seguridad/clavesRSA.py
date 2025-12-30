from fastmcp.server.auth.providers.jwt import RSAKeyPair

# Generar par de claves
keypair = RSAKeyPair.generate()

# Guardar a archivo
keypair.save("mcp_keypair.json")

# Cargar desde archivo
keypair = RSAKeyPair.load("mcp_keypair.json")

# Obtener clave pública (para el verificador)
public_key = keypair.public_key

# Crear token JWT
token = keypair.create_token(
    subject="cliente-ejemplo",      # Identificador del cliente
    issuer="gmail-mcp-server",      # Quién emite el token
    audience="gmail-mcp",           # Para quién es el token
    expiration_hours=24             # Validez del token
)

print(f"Token generado: {token}")

