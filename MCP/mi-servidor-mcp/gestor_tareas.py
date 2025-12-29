from fastmcp import FastMCP
from datetime import datetime
from typing import Optional

mcp = FastMCP("Gestor de Tareas")

# Almacén de tareas (en memoria para este ejemplo)
tareas = {}
contador_id = 0

@mcp.tool
def crear_tarea(
    titulo: str,
    descripcion: str = "",
    prioridad: str = "media"
) -> dict:
    """
    Crea una nueva tarea en el sistema.
    
    Args:
        titulo: Título de la tarea
        descripcion: Descripción detallada (opcional)
        prioridad: Nivel de prioridad (baja, media, alta)
    
    Returns:
        Información de la tarea creada
    """
    global contador_id
    contador_id += 1
    
    tarea = {
        "id": contador_id,
        "titulo": titulo,
        "descripcion": descripcion,
        "prioridad": prioridad,
        "completada": False,
        "fecha_creacion": datetime.now().isoformat()
    }
    
    tareas[contador_id] = tarea
    return {"status": "creada", "tarea": tarea}


@mcp.tool
def listar_tareas(
    solo_pendientes: bool = False,
    prioridad: Optional[str] = None
) -> list:
    """
    Lista las tareas existentes con filtros opcionales.
    
    Args:
        solo_pendientes: Si es True, solo muestra tareas no completadas
        prioridad: Filtrar por nivel de prioridad
    
    Returns:
        Lista de tareas que cumplen los criterios
    """
    resultado = list(tareas.values())
    
    if solo_pendientes:
        resultado = [t for t in resultado if not t["completada"]]
    
    if prioridad:
        resultado = [t for t in resultado if t["prioridad"] == prioridad]
    
    return resultado


@mcp.tool
def completar_tarea(id_tarea: int) -> dict:
    """
    Marca una tarea como completada.
    
    Args:
        id_tarea: Identificador único de la tarea
    
    Returns:
        Estado de la operación
    """
    if id_tarea not in tareas:
        return {"status": "error", "mensaje": f"Tarea {id_tarea} no encontrada"}
    
    tareas[id_tarea]["completada"] = True
    tareas[id_tarea]["fecha_completada"] = datetime.now().isoformat()
    
    return {"status": "completada", "tarea": tareas[id_tarea]}


if __name__ == "__main__":
    mcp.run()
