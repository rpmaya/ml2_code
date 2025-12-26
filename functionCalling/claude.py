from anthropic import Anthropic
import json

client = Anthropic()

tools_claude = [
    {
        "name": "obtener_clima",
        "description": "Obtiene información meteorológica actual de una ciudad",
        "input_schema": {
            "type": "object",
            "properties": {
                "ciudad": {
                    "type": "string",
                    "description": "Nombre de la ciudad"
                },
                "unidad": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Unidad de temperatura"
                }
            },
            "required": ["ciudad"]
        }
    }
]

def chat_con_tools_claude(mensaje: str) -> str:
    """Chat con Claude usando herramientas."""
    
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        tools=tools_claude,
        messages=[{"role": "user", "content": mensaje}]
    )
    
    # Procesar respuesta (puede contener múltiples bloques)
    for block in response.content:
        if block.type == "tool_use":
            # El modelo quiere usar una herramienta
            tool_name = block.name
            tool_input = block.input
            tool_use_id = block.id
            
            print(f"🔧 Claude quiere usar: {tool_name}({tool_input})")
            
            # Ejecutar herramienta
            resultado = obtener_clima(**tool_input)
            
            # Segunda llamada con el resultado
            response_final = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                tools=tools_claude,
                messages=[
                    {"role": "user", "content": mensaje},
                    {"role": "assistant", "content": response.content},
                    {
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": json.dumps(resultado, ensure_ascii=False)
                        }]
                    }
                ]
            )
            
            # Extraer texto de la respuesta final
            for final_block in response_final.content:
                if hasattr(final_block, 'text'):
                    return final_block.text
        
        elif block.type == "text":
            return block.text
    
    return "No se pudo procesar la respuesta"
