import chromadb

# Crear cliente - ¡Sin configuración!
client = chromadb.Client()

# Crear colección
collection = client.create_collection("mis_docs")

# Añadir documentos (genera embeddings automáticamente)
collection.add(
    documents=["Política de devoluciones...", "Tiempos de envío..."],
    ids=["doc1", "doc2"]
)

# Buscar
results = collection.query(query_texts=["devoluciones"], n_results=2)
print(f"Resultados: {results}")