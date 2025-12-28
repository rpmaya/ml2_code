import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()  # Usa OPENAI_API_KEY del entorno

def generar_embedding(texto):
    response = client.embeddings.create(
        input=texto,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def similitud_coseno(vec1, vec2):
    vec1, vec2 = np.array(vec1), np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Comparemos una consulta con varios documentos
consulta = "¿Puedo devolver un producto?"
documentos = [
    "Política de devoluciones: 30 días para reembolso",
    "Envío gratuito en pedidos de más de 50 euros",
    "El proceso de devolución es sencillo y rápido"
]

emb_consulta = generar_embedding(consulta)

for doc in documentos:
    emb_doc = generar_embedding(doc)
    sim = similitud_coseno(emb_consulta, emb_doc)
    print(f"[{sim:.3f}] {doc[:40]}...")