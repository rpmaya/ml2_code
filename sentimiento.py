from openai import OpenAI
import json

client = OpenAI()

def analizar_sentimiento_batch(textos: list[str]) -> list[dict]:
    """
    Analiza el sentimiento de múltiples textos en una sola llamada.
    
    Args:
        textos: Lista de textos a analizar
        
    Returns:
        Lista de diccionarios con sentimiento, confianza y keywords
    """
    system_prompt = """Analiza el sentimiento de cada texto.
Responde SOLO con un JSON array válido con este formato:
[{"texto_id": 0, "sentimiento": "POSITIVO|NEGATIVO|NEUTRO", "confianza": 0.95, "keywords": ["palabra1", "palabra2"]}]

Reglas:
- sentimiento: POSITIVO, NEGATIVO o NEUTRO
- confianza: valor entre 0 y 1
- keywords: 2-4 palabras clave que justifican el sentimiento
- No incluyas explicaciones, solo el JSON."""

    # Preparar textos numerados para referencia
    textos_numerados = "\n".join([f"{i}: {t}" for i, t in enumerate(textos)])
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analiza estos textos:\n{textos_numerados}"}
        ],
        temperature=0.1  # Baja para consistencia en clasificación
    )
    
    try:
        resultados = json.loads(response.choices[0].message.content)
        # Añadir texto original para referencia
        for r in resultados:
            r["texto_original"] = textos[r["texto_id"]]
        return resultados
    except json.JSONDecodeError as e:
        return [{"error": f"No se pudo parsear la respuesta: {e}"}]

# Ejemplo de uso
textos = [
    "¡Este producto es increíble! Lo recomiendo totalmente.",
    "Muy decepcionado, no funciona como prometían.",
    "El paquete llegó el martes a las 3pm.",
    "Podría ser mejor, pero cumple su función básica.",
    "Excelente atención al cliente, resolvieron mi problema en minutos."
]

resultados = analizar_sentimiento_batch(textos)

for r in resultados:
    if "error" not in r:
        print(f"Sentimiento: {r['sentimiento']} ({r['confianza']:.0%})")
        print(f"Keywords: {', '.join(r['keywords'])}")
        print(f"Texto: {r['texto_original'][:60]}...")
        print("---")
