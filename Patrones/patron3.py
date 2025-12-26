import logging
import json
from datetime import datetime
from functools import wraps

# Configurar logging estructurado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("llm_client")

def log_llm_call(func):
    """Decorador para loggear llamadas a LLM con métricas."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        
        try:
            result = func(*args, **kwargs)
            duration = (datetime.now() - start_time).total_seconds()
            
            # Log estructurado
            log_data = {
                "function": func.__name__,
                "duration_seconds": duration,
                "success": True,
                "timestamp": start_time.isoformat()
            }
            
            # Extraer métricas de uso si están disponibles
            if hasattr(result, 'usage'):
                log_data["tokens"] = {
                    "prompt": result.usage.prompt_tokens,
                    "completion": result.usage.completion_tokens,
                    "total": result.usage.total_tokens
                }
            
            logger.info(f"LLM call: {json.dumps(log_data)}")
            return result
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"LLM error: {json.dumps({
                'function': func.__name__,
                'error': str(e),
                'duration_seconds': duration,
                'timestamp': start_time.isoformat()
            })}")
            raise
    
    return wrapper


# Uso del decorador
from openai import OpenAI
client = OpenAI()

@log_llm_call
def llamar_llm(messages, **kwargs):
    return client.chat.completions.create(
        model=kwargs.get("model", "gpt-4o-mini"),
        messages=messages,
        **kwargs
    )

# Cada llamada se loggea automáticamente
response = llamar_llm([{"role": "user", "content": "Hola"}])
