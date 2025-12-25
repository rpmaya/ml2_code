from openai import OpenAI

client = OpenAI()

class Chatbot:
    """Chatbot con memoria de conversación y gestión de contexto."""
    
    def __init__(self, system_prompt="Eres un asistente amigable y útil.", 
                 max_history=20):
        self.system_prompt = system_prompt
        self.history = []
        self.max_history = max_history
    
    def chat(self, user_message):
        """Procesa un mensaje del usuario y devuelve la respuesta."""
        # Construir mensajes con historial
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": user_message})
        
        # Llamar a la API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7
        )
        
        assistant_message = response.choices[0].message.content
        
        # Guardar en historial
        self.history.append({"role": "user", "content": user_message})
        self.history.append({"role": "assistant", "content": assistant_message})
        
        # Limitar historial para no exceder contexto
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        return assistant_message
    
    def reset(self):
        """Reinicia el historial de conversación."""
        self.history = []
    
    def get_token_estimate(self):
        """Estima tokens usados en el historial (aproximación)."""
        total_chars = sum(len(m["content"]) for m in self.history)
        return total_chars // 4  # Aproximación: 1 token ≈ 4 caracteres

# Uso
bot = Chatbot("Eres un experto en cocina italiana. Responde de forma concisa.")

print(bot.chat("¿Cómo hago pasta fresca?"))
print("---")
print(bot.chat("¿Y qué salsa recomiendas?"))  # Recuerda el contexto
print("---")
print(bot.chat("Dame los pasos detallados"))  # Sigue el hilo de conversación
