from numpy import dot
from numpy.linalg import norm

def similitud_coseno(vec1: list[float], vec2: list[float]) -> float:
    """
    Calcula la similitud coseno entre dos vectores.
    Resultado: -1 (opuestos) a 1 (idénticos)
    """
    return dot(vec1, vec2) / (norm(vec1) * norm(vec2))


def encontrar_mas_similares(query: str, documentos: list[str], top_k: int = 3) -> list[tuple[str, float]]:
    """
    Encuentra los documentos más similares a una consulta.
    
    Args:
        query: Texto de búsqueda
        documentos: Lista de documentos donde buscar
        top_k: Número de resultados a devolver
        
    Returns:
        Lista de tuplas (documento, score) ordenadas por similitud
    """
    # Obtener embeddings (más eficiente en batch)
    todos_textos = [query] + documentos
    embeddings = obtener_embeddings_batch(todos_textos)
    
    query_emb = embeddings[0]
    docs_emb = embeddings[1:]
    
    # Calcular similitudes
    similitudes = []
    for i, doc_emb in enumerate(docs_emb):
        score = similitud_coseno(query_emb, doc_emb)
        similitudes.append((documentos[i], score))
    
    # Ordenar por similitud descendente
    similitudes.sort(key=lambda x: x[1], reverse=True)
    
    return similitudes[:top_k]


# Ejemplo: búsqueda semántica simple
documentos = [
    "Cómo instalar Python en Windows paso a paso",
    "Tutorial de machine learning con PyTorch",
    "Guía completa de desarrollo web con React",
    "Introducción a redes neuronales profundas",
    "Recetas de cocina italiana tradicional",
    "Configuración de Docker para desarrollo",
    "Aprende JavaScript desde cero",
    "Deep learning para procesamiento de imágenes"
]

query = "quiero aprender inteligencia artificial"

print(f"Búsqueda: '{query}'\n")
print("Documentos más relevantes:")
print("-" * 50)

for doc, score in encontrar_mas_similares(query, documentos):
    print(f"[{score:.3f}] {doc}")
