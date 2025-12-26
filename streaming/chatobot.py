from openai import OpenAI
from typing import Generator

client = OpenAI()

class ChatbotStreaming:
    """Chatbot con soporte para streaming y memoria."""
    
    def __init__(self, system_prompt="Eres un asistente útil.", max_history=20):
        self.system_prompt = system_prompt
        self.history = []
        self.max_history = max_history
    
    def chat_stream(self, user_message: str) -> Generator[str, None, str]:
        """
        Chat con streaming. Genera tokens y devuelve respuesta completa.
        
        Yields:
            Cada token generado
            
        Returns:
            Respuesta completa (accesible via .send(None) o al final)
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": user_message})
        
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True
        )
        
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                yield content
        
        # Actualizar historial
        self.history.append({"role": "user", "content": user_message})
        self.history.append({"role": "assistant", "content": full_response})
        
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        return full_response

# Uso
bot = ChatbotStreaming("Eres un tutor de Python.")

print("Bot: ", end="")
for token in bot.chat_stream("¿Qué son los decoradores?"):
    print(token, end="", flush=True)
print("\n")

print("Bot: ", end="")
for token in bot.chat_stream("Dame un ejemplo práctico"):  # Mantiene contexto
    print(token, end="", flush=True)
print()
