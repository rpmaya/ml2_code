import time
from openai import OpenAI, RateLimitError, APIError
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

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

def generar_embedding_robusto(texto: str, max_reintentos: int = 3) -> list:
    """
    Genera embedding con manejo de errores y reintentos.
    """
    for intento in range(max_reintentos):
        try:
            return generar_embedding(texto)
        except RateLimitError:
            espera = 2 ** intento  # Backoff exponencial
            print(f"Rate limit alcanzado. Esperando {espera}s...")
            time.sleep(espera)
        except APIError as e:
            print(f"Error de API: {e}")
            if intento == max_reintentos - 1:
                raise
    return None

texto = "La política de devoluciones permite reembolsos en 30 días"
embedding = generar_embedding_robusto(texto)

print(f"Dimensiones del embedding: {len(embedding)}")
print(f"Primeros 5 valores: {embedding[:5]}")
