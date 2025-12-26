# config.py
LLM_CONFIG = {
    "default_provider": "openai",
    "models": {
        "openai": "gpt-4o-mini",
        "anthropic": "claude-3-sonnet-20240229",
        "google": "gemini-pro"
    },
    "defaults": {
        "temperature": 0.7,
        "max_tokens": 1024,
        "timeout": 30
    },
    "retry": {
        "max_attempts": 3,
        "backoff_factor": 2,
        "retry_on": ["rate_limit", "timeout", "server_error"]
    },
    "fallback_chain": ["openai", "anthropic", "google"]  # Orden de fallback
}

# Cargar desde variables de entorno en producción
import os
LLM_CONFIG["default_provider"] = os.getenv("LLM_PROVIDER", LLM_CONFIG["default_provider"])
