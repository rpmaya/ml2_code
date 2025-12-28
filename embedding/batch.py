from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuración del cliente
client = OpenAI()  # Usa OPENAI_API_KEY del entorno

def generar_embeddings_batch(textos: list, modelo: str = "text-embedding-3-small") -> list:
    """
    Genera embeddings para múltiples textos en una sola llamada API.
    
    Args:
        textos: Lista de textos a procesar
        modelo: El modelo de embeddings a utilizar
    
    Returns:
        Lista de embeddings (uno por cada texto de entrada)
    """
    response = client.embeddings.create(
        input=textos,
        model=modelo
    )
    # Ordenar por índice para mantener correspondencia con entrada
    return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]

# Ejemplo: procesar múltiples fragmentos
fragmentos = [
    "Política de devoluciones: 30 días para productos sin usar",
    "Envío gratuito en pedidos superiores a 50 euros",
    "Atención al cliente disponible de lunes a viernes"
]

embeddings = generar_embeddings_batch(fragmentos)
print(f"Generados {len(embeddings)} embeddings")
