from fastmcp import FastMCP

# Crear instancia del servidor
mcp = FastMCP("Mi Servidor MCP")

# Definir una herramienta simple
@mcp.tool
def saludar(nombre: str) -> str:
    """Saluda a una persona por su nombre"""
    return f"¡Hola, {nombre}! Bienvenido."

@mcp.tool
def calcular_precio(
    precio_base: float,
    cantidad: int,
    descuento: float = 0.0
) -> dict:
    """
    Calcula el precio total de una compra.
    
    Args:
        precio_base: Precio unitario del producto
        cantidad: Número de unidades
        descuento: Porcentaje de descuento (0-100)
    
    Returns:
        Diccionario con el desglose del precio
    """
    subtotal = precio_base * cantidad
    descuento_aplicado = subtotal * (descuento / 100)
    total = subtotal - descuento_aplicado
    
    return {
        "subtotal": subtotal,
        "descuento": descuento_aplicado,
        "total": total
    }


# Punto de entrada
if __name__ == "__main__":
    mcp.run()
