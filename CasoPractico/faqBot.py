class FAQBot:
    """Bot de preguntas frecuentes usando búsqueda semántica."""
    
    def __init__(self, faqs: list[dict]):
        """
        Args:
            faqs: Lista de {"pregunta": "...", "respuesta": "..."}
        """
        self.faqs = faqs
        self.preguntas = [faq["pregunta"] for faq in faqs]
        
        # Pre-calcular embeddings de todas las preguntas
        print("Generando embeddings de FAQ...")
        self.embeddings_preguntas = obtener_embeddings_batch(self.preguntas)
        print(f"✓ {len(self.preguntas)} preguntas indexadas")
    
    def buscar(self, consulta: str, umbral: float = 0.7) -> dict | None:
        """
        Busca la FAQ más relevante para una consulta.
        
        Args:
            consulta: Pregunta del usuario
            umbral: Similitud mínima para considerar una respuesta
            
        Returns:
            FAQ más similar o None si no hay match suficiente
        """
        # Embedding de la consulta
        emb_consulta = obtener_embedding(consulta)
        
        # Encontrar más similar
        mejor_score = -1
        mejor_idx = -1
        
        for i, emb_pregunta in enumerate(self.embeddings_preguntas):
            score = similitud_coseno(emb_consulta, emb_pregunta)
            if score > mejor_score:
                mejor_score = score
                mejor_idx = i
        
        if mejor_score >= umbral:
            return {
                "pregunta_match": self.preguntas[mejor_idx],
                "respuesta": self.faqs[mejor_idx]["respuesta"],
                "confianza": mejor_score
            }
        return None


# Ejemplo de uso
faqs = [
    {
        "pregunta": "¿Cómo puedo restablecer mi contraseña?",
        "respuesta": "Ve a la página de login, haz clic en '¿Olvidaste tu contraseña?' y sigue las instrucciones enviadas a tu email."
    },
    {
        "pregunta": "¿Cuál es el horario de atención al cliente?",
        "respuesta": "Nuestro equipo está disponible de lunes a viernes de 9:00 a 18:00."
    },
    {
        "pregunta": "¿Cómo cancelo mi suscripción?",
        "respuesta": "Puedes cancelar desde tu perfil > Configuración > Suscripción > Cancelar plan."
    },
    {
        "pregunta": "¿Ofrecen reembolsos?",
        "respuesta": "Sí, ofrecemos reembolso completo dentro de los primeros 30 días."
    }
]

bot = FAQBot(faqs)

# Probar con variaciones de preguntas
consultas = [
    "olvidé mi clave",
    "quiero darme de baja",
    "¿puedo recuperar mi dinero?",
    "¿a qué hora abren?"
]

for consulta in consultas:
    print(f"\nUsuario: {consulta}")
    resultado = bot.buscar(consulta)
    if resultado:
        print(f"Bot [{resultado['confianza']:.0%}]: {resultado['respuesta']}")
    else:
        print("Bot: Lo siento, no encontré una respuesta. ¿Puedes reformular tu pregunta?")
