from anthropic import Anthropic

client = Anthropic()

def chat_streaming_claude(prompt: str, system: str = "Eres un asistente útil."):
    """Streaming con Claude usando context manager."""
    
    with client.messages.stream(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        full_response = ""
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_response += text
    
    print()
    return full_response

# Uso
respuesta = chat_streaming_claude("¿Cuáles son los principios SOLID?")
