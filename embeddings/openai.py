from openai import OpenAI
import numpy as np

client = OpenAI()

def obtener_embedding(texto: str, modelo: str = "text-embedding-3-small") -> list[float]:
    """
    Obtiene el embedding de un texto.
    
    Modelos disponibles:
    - text-embedding-3-small: 1536 dims, más económico
    - text-embedding-3-large: 3072 dims, mayor calidad
    - text-embedding-ada-002: 1536 dims, modelo anterior
    """
    response = client.embeddings.create(
        input=texto,
        model=modelo
    )
    return response.data[0].embedding


def obtener_embeddings_batch(textos: list[str], modelo: str = "text-embedding-3-small") -> list[list[float]]:
    """
    Obtiene embeddings de múltiples textos en una sola llamada.
    Más eficiente que llamadas individuales.
    """
    response = client.embeddings.create(
        input=textos,
        model=modelo
    )
    # Mantener el orden original
    return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]


# Ejemplo básico
texto = "La inteligencia artificial está transformando la industria del software"
embedding = obtener_embedding(texto)
print(f"Texto: '{texto[:50]}...'")
print(f"Dimensiones del embedding: {len(embedding)}")
print(f"Primeros 5 valores: {embedding[:5]}")
