from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import trim_messages

class ChatbotLangChain:
    """Chatbot completo usando LangChain."""
    
    def __init__(self, system_prompt: str = "Eres un asistente útil.",
                 model: str = "gpt-4o-mini",
                 max_history_tokens: int = 2000):
        
        self.llm = ChatOpenAI(model=model, temperature=0.7, streaming=True)
        self.max_history_tokens = max_history_tokens
        self.store = {}
        
        # Template con historial
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # Chain con memoria
        chain = self.prompt | self.llm | StrOutputParser()
        
        self.chain = RunnableWithMessageHistory(
            chain,
            self._get_history,
            input_messages_key="input",
            history_messages_key="history"
        )
    
    def _get_history(self, session_id: str) -> ChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]
    
    def chat(self, message: str, session_id: str = "default") -> str:
        """Envía un mensaje y obtiene respuesta."""
        config = {"configurable": {"session_id": session_id}}
        return self.chain.invoke({"input": message}, config=config)
    
    def chat_stream(self, message: str, session_id: str = "default"):
        """Envía un mensaje con streaming."""
        config = {"configurable": {"session_id": session_id}}
        for chunk in self.chain.stream({"input": message}, config=config):
            yield chunk
    
    def get_history(self, session_id: str = "default") -> list:
        """Obtiene el historial de una sesión."""
        if session_id in self.store:
            return [(m.type, m.content) for m in self.store[session_id].messages]
        return []
    
    def clear_history(self, session_id: str = "default"):
        """Limpia el historial de una sesión."""
        if session_id in self.store:
            self.store[session_id].clear()


# Uso
bot = ChatbotLangChain(
    system_prompt="Eres un tutor de Python amigable. Explicas conceptos con ejemplos prácticos."
)

# Conversación normal
print("Bot:", bot.chat("Hola, quiero aprender sobre funciones", session_id="alumno_1"))
print("Bot:", bot.chat("¿Cómo les paso argumentos?", session_id="alumno_1"))
print("Bot:", bot.chat("¿Y qué son los *args?", session_id="alumno_1"))

# Conversación con streaming
print("\nBot (streaming): ", end="")
for chunk in bot.chat_stream("Dame un ejemplo completo", session_id="alumno_1"):
    print(chunk, end="", flush=True)
print()

# Ver historial
print("\n--- Historial ---")
for tipo, contenido in bot.get_history("alumno_1"):
    print(f"{tipo}: {contenido[:60]}...")
