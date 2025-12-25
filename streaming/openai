from openai import OpenAI

client = OpenAI()

def chat_streaming(prompt: str, system: str = "Eres un asistente útil."):
    """
    Genera respuesta en streaming, imprimiendo token a token.
    
    Args:
        prompt: Mensaje del usuario
        system: System prompt opcional
        
    Returns:
        Respuesta completa como string
    """
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        stream=True  # Habilita streaming
    )
    
    full_response = ""
    for chunk in stream:
        # Cada chunk contiene un delta con el nuevo contenido
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)  # Imprime sin salto de línea
            full_response += content
    
    print()  # Salto de línea final
    return full_response

# Uso
respuesta = chat_streaming(
    "Explica qué es la recursión en programación con un ejemplo en Python"
)
