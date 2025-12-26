from langchain_core.messages import trim_messages

# Función para limitar el historial
def get_trimmed_history(session_id: str) -> BaseChatMessageHistory:
    history = get_session_history(session_id)
    # Mantener solo los últimos 10 mensajes
    if len(history.messages) > 10:
        history.messages = history.messages[-10:]
    return history

# O usar trim_messages directamente en el chain
chain_con_trim = (
    RunnablePassthrough.assign(
        history=lambda x: trim_messages(
            x["history"],
            max_tokens=1000,  # Límite por tokens
            token_counter=llm,  # Usa el modelo para contar
            strategy="last"  # Mantener los últimos
        )
    )
    | template
    | llm
    | StrOutputParser()
)

