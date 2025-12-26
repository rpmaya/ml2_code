from openai import OpenAI
import json

client = OpenAI()

# 1. DEFINIR LAS HERRAMIENTAS DISPONIBLES
tools = [
    {
        "type": "function",
        "function": {
            "name": "obtener_clima",
            "description": "Obtiene el clima actual de una ciudad. Usar cuando el usuario pregunte por el tiempo o clima.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ciudad": {
                        "type": "string",
                        "description": "Nombre de la ciudad, ej: Madrid, Barcelona, México DF"
                    },
                    "unidad": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Unidad de temperatura preferida"
                    }
                },
                "required": ["ciudad"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_restaurantes",
            "description": "Busca restaurantes en una ubicación, opcionalmente filtrados por tipo de cocina",
            "parameters": {
                "type": "object",
                "properties": {
                    "ubicacion": {
                        "type": "string",
                        "description": "Ciudad o zona donde buscar"
                    },
                    "tipo_cocina": {
                        "type": "string",
                        "description": "Tipo de cocina: italiana, japonesa, mexicana, etc."
                    },
                    "precio_max": {
                        "type": "number",
                        "description": "Precio máximo por persona en euros"
                    }
                },
                "required": ["ubicacion"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ejecutar_codigo_python",
            "description": "Ejecuta código Python para cálculos matemáticos o procesamiento de datos",
            "parameters": {
                "type": "object",
                "properties": {
                    "codigo": {
                        "type": "string",
                        "description": "Código Python a ejecutar"
                    }
                },
                "required": ["codigo"]
            }
        }
    }
]

# 2. IMPLEMENTACIONES REALES DE LAS FUNCIONES
def obtener_clima(ciudad: str, unidad: str = "celsius") -> dict:
    """
    Simula llamada a API de clima.
    En producción, usaríamos OpenWeatherMap, WeatherAPI, etc.
    """
    # Datos simulados
    climas = {
        "madrid": {"temp_c": 22, "condicion": "soleado", "humedad": 45},
        "barcelona": {"temp_c": 25, "condicion": "parcialmente nublado", "humedad": 60},
        "londres": {"temp_c": 15, "condicion": "lluvioso", "humedad": 80},
    }
    
    ciudad_lower = ciudad.lower()
    if ciudad_lower in climas:
        data = climas[ciudad_lower]
        temp = data["temp_c"] if unidad == "celsius" else (data["temp_c"] * 9/5) + 32
        return {
            "ciudad": ciudad,
            "temperatura": round(temp, 1),
            "unidad": unidad,
            "condicion": data["condicion"],
            "humedad": data["humedad"]
        }
    return {"ciudad": ciudad, "error": "Ciudad no encontrada en la base de datos"}


def buscar_restaurantes(ubicacion: str, tipo_cocina: str = None, precio_max: float = None) -> list:
    """Simula búsqueda en base de datos de restaurantes."""
    # Datos simulados
    restaurantes = [
        {"nombre": "La Trattoria", "tipo": "italiana", "precio_medio": 25, "rating": 4.5},
        {"nombre": "Sakura", "tipo": "japonesa", "precio_medio": 35, "rating": 4.7},
        {"nombre": "El Rincón", "tipo": "española", "precio_medio": 20, "rating": 4.2},
        {"nombre": "Taquería México", "tipo": "mexicana", "precio_medio": 15, "rating": 4.3},
    ]
    
    resultados = restaurantes
    if tipo_cocina:
        resultados = [r for r in resultados if r["tipo"].lower() == tipo_cocina.lower()]
    if precio_max:
        resultados = [r for r in resultados if r["precio_medio"] <= precio_max]
    
    return resultados[:3]  # Máximo 3 resultados


def ejecutar_codigo_python(codigo: str) -> dict:
    """
    Ejecuta código Python de forma segura.
    ⚠️ En producción, usar sandbox como RestrictedPython o contenedor aislado.
    """
    try:
        # Contexto limitado para seguridad
        allowed_globals = {"__builtins__": {"abs": abs, "round": round, "sum": sum, 
                                             "min": min, "max": max, "len": len}}
        result = eval(codigo, allowed_globals)
        return {"resultado": result, "exito": True}
    except Exception as e:
        return {"error": str(e), "exito": False}


# Mapeo de nombres a funciones
FUNCIONES_DISPONIBLES = {
    "obtener_clima": obtener_clima,
    "buscar_restaurantes": buscar_restaurantes,
    "ejecutar_codigo_python": ejecutar_codigo_python
}


# 3. FUNCIÓN PRINCIPAL QUE MANEJA EL FLUJO COMPLETO
def chat_con_herramientas(mensaje_usuario: str, verbose: bool = True) -> str:
    """
    Chat que puede usar herramientas automáticamente.
    
    Args:
        mensaje_usuario: Pregunta o solicitud del usuario
        verbose: Si True, muestra información de debug
        
    Returns:
        Respuesta final del modelo
    """
    messages = [
        {"role": "system", "content": "Eres un asistente útil con acceso a herramientas. "
                                       "Usa las herramientas cuando sea necesario para dar respuestas precisas."},
        {"role": "user", "content": mensaje_usuario}
    ]
    
    # Primera llamada: el modelo decide si necesita herramientas
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"  # El modelo decide si usar herramientas
    )
    
    assistant_message = response.choices[0].message
    
    # Si el modelo NO quiere usar herramientas, devolver respuesta directa
    if not assistant_message.tool_calls:
        return assistant_message.content
    
    # Si el modelo QUIERE usar herramientas
    if verbose:
        print(f"🔧 El modelo quiere usar {len(assistant_message.tool_calls)} herramienta(s)")
    
    # Añadir mensaje del asistente al historial
    messages.append(assistant_message)
    
    # Ejecutar cada herramienta solicitada
    for tool_call in assistant_message.tool_calls:
        nombre_funcion = tool_call.function.name
        argumentos = json.loads(tool_call.function.arguments)
        
        if verbose:
            print(f"   → Llamando a '{nombre_funcion}' con argumentos: {argumentos}")
        
        # Ejecutar la función real
        if nombre_funcion in FUNCIONES_DISPONIBLES:
            resultado = FUNCIONES_DISPONIBLES[nombre_funcion](**argumentos)
        else:
            resultado = {"error": f"Función {nombre_funcion} no encontrada"}
        
        if verbose:
            print(f"   ← Resultado: {resultado}")
        
        # Añadir resultado al historial
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(resultado, ensure_ascii=False)
        })
    
    # Segunda llamada: el modelo genera respuesta final con los resultados
    response_final = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    return response_final.choices[0].message.content


# EJEMPLOS DE USO
if __name__ == "__main__":
    print("=" * 60)
    print("Ejemplo 1: Pregunta que requiere herramienta de clima")
    print("=" * 60)
    print(chat_con_herramientas("¿Qué tiempo hace hoy en Madrid?"))
    
    print("\n" + "=" * 60)
    print("Ejemplo 2: Búsqueda de restaurantes")
    print("=" * 60)
    print(chat_con_herramientas("Busco restaurantes italianos en Barcelona con precio máximo de 30€"))
    
    print("\n" + "=" * 60)
    print("Ejemplo 3: Cálculo matemático")
    print("=" * 60)
    print(chat_con_herramientas("¿Cuánto es 15% de 2500?"))
    
    print("\n" + "=" * 60)
    print("Ejemplo 4: Pregunta que NO necesita herramientas")
    print("=" * 60)
    print(chat_con_herramientas("¿Cuál es la capital de Francia?"))
