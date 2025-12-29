from fastmcp import FastMCP

mcp = FastMCP("Asistente de Email")

@mcp.prompt()
def redactar_email_profesional(
    destinatario: str,
    asunto: str,
    puntos_clave: str
) -> str:
    """
    Genera un prompt para redactar un email profesional.
    
    Args:
        destinatario: A quién va dirigido el email
        asunto: Tema principal del email
        puntos_clave: Puntos que debe incluir el email
    """
    return f"""Redacta un email profesional con las siguientes características:

DESTINATARIO: {destinatario}
ASUNTO: {asunto}

PUNTOS A INCLUIR:
{puntos_clave}

INSTRUCCIONES:
- Usa un tono formal pero cercano
- Incluye saludo y despedida apropiados
- Sé conciso pero completo
- Estructura el contenido en párrafos claros
"""


@mcp.prompt()
def analizar_codigo(lenguaje: str, enfoque: str = "general") -> str:
    """
    Genera un prompt para análisis de código.
    
    Args:
        lenguaje: Lenguaje de programación del código
        enfoque: Tipo de análisis (general, seguridad, rendimiento)
    """
    enfoques = {
        "general": "calidad general, legibilidad y buenas prácticas",
        "seguridad": "vulnerabilidades, validación de entradas y manejo de datos sensibles",
        "rendimiento": "eficiencia, complejidad algorítmica y uso de recursos"
    }
    
    descripcion_enfoque = enfoques.get(enfoque, enfoques["general"])
    
    return f"""Analiza el siguiente código {lenguaje} enfocándote en {descripcion_enfoque}.

Proporciona:
1. Resumen general del código
2. Puntos positivos
3. Áreas de mejora
4. Sugerencias específicas con ejemplos de código

Código a analizar:
"""


if __name__ == "__main__":
    mcp.run()
