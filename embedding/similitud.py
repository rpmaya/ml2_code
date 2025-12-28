import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

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

def similitud_coseno(vec1: list, vec2: list) -> float:
    """
    Calcula la similitud coseno entre dos vectores.
    
    Returns:
        Valor entre -1 y 1, donde 1 indica máxima similitud
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Ejemplo: comparar similitud de consulta con documentos
consulta = "¿Puedo devolver un producto?"
documentos = [
    "La política de devoluciones permite reembolsos en 30 días",
    "Ofrecemos envío express en 24 horas",
    "El proceso de devolución es sencillo y rápido"
]

# Generar embeddings
emb_consulta = generar_embedding(consulta)
emb_documentos = generar_embeddings_batch(documentos)

# Calcular similitudes
for doc, emb_doc in zip(documentos, emb_documentos):
    sim = similitud_coseno(emb_consulta, emb_doc)
    print(f"[{sim:.3f}] {doc[:50]}...")
