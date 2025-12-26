from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Almacén de historiales (en memoria, por sesión)
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Obtiene o crea el historial para una sesión."""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Template con placeholder para historial
template = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente de programación útil y amigable."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Chain base
chain = template | llm | StrOutputParser()

# Envolver con gestión de memoria
chain_con_memoria = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Configuración de sesión
config = {"configurable": {"session_id": "usuario_123"}}

# Conversación con memoria automática
print(chain_con_memoria.invoke(
    {"input": "Hola, estoy aprendiendo Python"},
    config=config
))

print(chain_con_memoria.invoke(
    {"input": "¿Qué me recomiendas empezar a estudiar?"},  # Recuerda contexto
    config=config
))

print(chain_con_memoria.invoke(
    {"input": "¿Puedes darme un ejemplo de lo primero que mencionaste?"},  # Sigue recordando
    config=config
))

# Ver historial almacenado
print("\n--- Historial de la sesión ---")
for msg in store["usuario_123"].messages:
    print(f"{msg.type}: {msg.content[:50]}...")
