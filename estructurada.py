from openai import OpenAI
import json

client = OpenAI()

def extraer_datos_estructurados(texto: str, schema: dict) -> dict:
    """
    Extrae información estructurada de un texto según un schema definido.
    
    Args:
        texto: Texto del cual extraer información
        schema: Diccionario que define la estructura esperada
        
    Returns:
        Diccionario con los datos extraídos
    """
    schema_str = json.dumps(schema, indent=2, ensure_ascii=False)
    
    system_prompt = f"""Extrae información del texto según este schema JSON:
{schema_str}

Reglas:
- Responde SOLO con JSON válido
- Si un campo no está presente en el texto, usa null
- Mantén exactamente la estructura del schema
- No añadas campos extra
- Extrae la información tal como aparece, sin interpretar"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": texto}
        ],
        temperature=0.1,
        response_format={"type": "json_object"}  # Fuerza JSON válido
    )
    
    return json.loads(response.choices[0].message.content)

# Ejemplo 1: Extraer datos de un email
email = """
De: carlos.garcia@empresa.com
Para: maria.lopez@cliente.com
Asunto: Propuesta de proyecto Q1 2024

Hola María,

Adjunto la propuesta para el proyecto de modernización de infraestructura.
El presupuesto estimado es de €45,000 con una duración de 3 meses.
Fecha de inicio propuesta: 15 de enero de 2024
Equipo asignado: 2 desarrolladores senior + 1 PM

Por favor confirma disponibilidad para una llamada el próximo martes.

Saludos,
Carlos García
Director de Proyectos
Tel: +34 612 345 678
"""

schema_email = {
    "remitente": {
        "nombre": "string",
        "email": "string",
        "cargo": "string",
        "telefono": "string"
    },
    "destinatario": {
        "nombre": "string", 
        "email": "string"
    },
    "proyecto": {
        "nombre": "string",
        "presupuesto": "number",
        "moneda": "string",
        "duracion_meses": "number",
        "fecha_inicio": "string (ISO format)",
        "equipo": ["string"]
    },
    "accion_requerida": "string"
}

resultado = extraer_datos_estructurados(email, schema_email)
print(json.dumps(resultado, indent=2, ensure_ascii=False))

# Ejemplo 2: Extraer datos de un CV/currículum
cv_texto = """
Juan Pérez Martínez
Desarrollador Full Stack Senior

Experiencia:
- Tech Solutions (2020-presente): Lead Developer, Python, React
- StartupXYZ (2018-2020): Backend Developer, Node.js, MongoDB
- Freelance (2016-2018): Desarrollo web

Educación:
- Máster en Ingeniería de Software, Universidad Politécnica, 2018
- Grado en Informática, Universidad Complutense, 2016

Skills: Python, JavaScript, React, Node.js, Docker, AWS, PostgreSQL

Contacto: juan.perez@email.com | LinkedIn: /in/juanperez | GitHub: @jperez
"""

schema_cv = {
    "nombre_completo": "string",
    "titulo_profesional": "string",
    "experiencia": [{
        "empresa": "string",
        "periodo": "string",
        "cargo": "string",
        "tecnologias": ["string"]
    }],
    "educacion": [{
        "titulo": "string",
        "institucion": "string",
        "año": "number"
    }],
    "skills": ["string"],
    "contacto": {
        "email": "string",
        "linkedin": "string",
        "github": "string"
    }
}

resultado_cv = extraer_datos_estructurados(cv_texto, schema_cv)
print(json.dumps(resultado_cv, indent=2, ensure_ascii=False))
