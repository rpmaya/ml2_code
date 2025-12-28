from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
import os

# Configuración del cliente
client = OpenAI()  # Usa OPENAI_API_KEY del entorno

def generar_embedding(texto: str, modelo: str = "text-embedding-3-small") -> list:
    """
    Genera el embedding de un texto usando la API de OpenAI.
    
    Args:
        texto: El texto a convertir en embedding
        modelo: El modelo de embeddings a utilizar
    
    Returns:
        Lista de floats representando el embedding
    """
    response = client.embeddings.create(
        input=texto,
        model=modelo
    )
    return response.data[0].embedding

# Ejemplo de uso
texto = "La política de devoluciones permite reembolsos en 30 días"
embedding = generar_embedding(texto)

print(f"Dimensiones del embedding: {len(embedding)}")
print(f"Primeros 5 valores: {embedding[:5]}")
