from fastmcp import FastMCP
import sqlite3
from typing import Optional

# Ruta a la base de datos
DB_PATH = "./tienda_videojuegos.db"

# Crear servidor MCP
mcp = FastMCP("Tienda Videojuegos DB")


def get_connection():
    """Obtiene una conexión a la base de datos en modo solo lectura."""
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


@mcp.tool
def listar_tablas() -> list:
    """
    Lista todas las tablas disponibles en la base de datos.
    
    Returns:
        Lista con los nombres de las tablas
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' 
        ORDER BY name
    """)
    
    tablas = [row["name"] for row in cursor.fetchall()]
    conn.close()
    
    return tablas


@mcp.tool
def describir_tabla(nombre_tabla: str) -> dict:
    """
    Obtiene la estructura de una tabla específica.
    
    Args:
        nombre_tabla: Nombre de la tabla a describir
    
    Returns:
        Información sobre las columnas de la tabla
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Validar que la tabla existe (previene SQL injection)
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (nombre_tabla,)
    )
    if not cursor.fetchone():
        conn.close()
        return {"error": f"Tabla '{nombre_tabla}' no encontrada"}
    
    cursor.execute(f"PRAGMA table_info({nombre_tabla})")
    columnas = [
        {
            "nombre": row["name"],
            "tipo": row["type"],
            "nullable": not row["notnull"],
            "primary_key": bool(row["pk"])
        }
        for row in cursor.fetchall()
    ]
    
    conn.close()
    return {"tabla": nombre_tabla, "columnas": columnas}


@mcp.tool
def ejecutar_consulta(consulta_sql: str, limite: int = 100) -> dict:
    """
    Ejecuta una consulta SELECT en la base de datos.
    
    Args:
        consulta_sql: Consulta SQL (solo SELECT permitido)
        limite: Número máximo de filas a retornar
    
    Returns:
        Resultados de la consulta
    """
    # Validación de seguridad: solo permitir SELECT
    consulta_limpia = consulta_sql.strip().upper()
    if not consulta_limpia.startswith("SELECT"):
        return {
            "error": "Solo se permiten consultas SELECT",
            "consejo": "Esta herramienta es de solo lectura"
        }
    
    # Verificar que no hay comandos peligrosos
    palabras_prohibidas = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "CREATE"]
    for palabra in palabras_prohibidas:
        if palabra in consulta_limpia:
            return {"error": f"Comando '{palabra}' no permitido"}
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Añadir LIMIT si no está presente
        if "LIMIT" not in consulta_limpia:
            consulta_sql = f"{consulta_sql} LIMIT {limite}"
        
        cursor.execute(consulta_sql)
        
        # Obtener nombres de columnas
        columnas = [description[0] for description in cursor.description]
        
        # Convertir filas a diccionarios
        filas = [dict(zip(columnas, row)) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            "columnas": columnas,
            "filas": filas,
            "total_filas": len(filas)
        }
        
    except sqlite3.Error as e:
        return {"error": f"Error SQL: {str(e)}"}


@mcp.tool
def obtener_estadisticas() -> dict:
    """
    Obtiene estadísticas generales de la base de datos.
    
    Returns:
        Resumen con conteos de registros por tabla
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Obtener lista de tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = [row[0] for row in cursor.fetchall()]
    
    estadisticas = {}
    for tabla in tablas:
        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
        estadisticas[tabla] = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total_tablas": len(tablas),
        "registros_por_tabla": estadisticas
    }


if __name__ == "__main__":
    mcp.run()
