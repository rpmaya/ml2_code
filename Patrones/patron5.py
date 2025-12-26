import json
from jsonschema import validate, ValidationError

def llamar_con_validacion_json(prompt: str, schema: dict, max_intentos: int = 2) -> dict:
    """
    Llama al modelo esperando JSON y valida contra un schema.
    Reintenta si el JSON es inválido.
    """
    system_prompt = f"""Responde ÚNICAMENTE con JSON válido que cumpla este schema:
{json.dumps(schema, indent=2)}

No incluyas markdown, explicaciones ni texto adicional. Solo JSON."""

    for intento in range(max_intentos):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        
        try:
            data = json.loads(content)
            validate(instance=data, schema=schema)
            return data
            
        except json.JSONDecodeError as e:
            logger.warning(f"JSON inválido (intento {intento + 1}): {e}")
            
        except ValidationError as e:
            logger.warning(f"Schema no cumplido (intento {intento + 1}): {e.message}")
    
    raise ValueError(f"No se pudo obtener JSON válido después de {max_intentos} intentos")
