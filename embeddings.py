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

texto = "¿Cuál es la política de devoluciones?"
embedding = generar_embedding(texto)

print(f"Dimensiones: {len(embedding)}")
print(f"Primeros valores: {embedding[:5]}")