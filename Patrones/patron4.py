import time
from openai import OpenAI, RateLimitError, APITimeoutError, APIError

client = OpenAI()

def llamar_con_retry(messages, max_intentos=3, backoff_base=2):
    """
    Llama a la API con reintentos automáticos en caso de error.
    
    Errores que se reintentan:
    - RateLimitError: Límite de rate alcanzado
    - APITimeoutError: Timeout de la API
    - APIError (5xx): Errores del servidor
    """
    ultimo_error = None
    
    for intento in range(max_intentos):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return response.choices[0].message.content
            
        except RateLimitError as e:
            ultimo_error = e
            wait_time = backoff_base ** intento
            logger.warning(f"Rate limit alcanzado. Esperando {wait_time}s...")
            time.sleep(wait_time)
            
        except APITimeoutError as e:
            ultimo_error = e
            wait_time = backoff_base ** intento
            logger.warning(f"Timeout. Reintentando en {wait_time}s...")
            time.sleep(wait_time)
            
        except APIError as e:
            if e.status_code and e.status_code >= 500:
                ultimo_error = e
                wait_time = backoff_base ** intento
                logger.warning(f"Error del servidor ({e.status_code}). Esperando {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise  # No reintentar errores 4xx
    
    raise ultimo_error  # Todos los intentos fallaron
