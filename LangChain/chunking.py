from langchain_text_splitters import RecursiveCharacterTextSplitter

# Crear splitter con configuración
splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,           # Tamaño máximo en caracteres
    chunk_overlap=50,         # Solapamiento entre chunks
    length_function=len,      # Función para medir longitud
    separators=["\n\n", "\n", ". ", " "]  # Jerarquía de separadores
)

# Texto de ejemplo
documento = """
Política de Devoluciones

Nuestra empresa ofrece un período de devolución de 30 días naturales 
desde la fecha de entrega del producto. Durante este período, el cliente 
puede solicitar la devolución por cualquier motivo.

Condiciones para la devolución:
- El producto debe estar en su embalaje original
- No debe presentar signos de uso
- Debe incluir todos los accesorios

Proceso de devolución:
1. Contactar con atención al cliente
2. Obtener número de autorización de devolución
3. Enviar el producto a nuestra dirección
4. El reembolso se procesa en 5-7 días hábiles
"""

# Dividir documento
chunks = splitter.split_text(documento)

for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ({len(chunk)} chars) ---")
    print(chunk)
    print()
