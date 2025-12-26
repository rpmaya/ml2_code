from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Template que incluye historial de conversación
template_con_historial = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente de programación. Ayuda al usuario con sus dudas."),
    MessagesPlaceholder(variable_name="historial"),  # Aquí va el historial
    ("human", "{pregunta}")
])

# Simular historial previo
historial = [
    HumanMessage(content="Estoy aprendiendo Python"),
    AIMessage(content="¡Genial! Python es un excelente lenguaje para empezar. ¿En qué puedo ayudarte?"),
    HumanMessage(content="¿Qué son las funciones?"),
    AIMessage(content="Las funciones son bloques de código reutilizables que realizan una tarea específica...")
]

# Generar prompt con historial
prompt = template_con_historial.invoke({
    "historial": historial,
    "pregunta": "¿Y cómo les paso parámetros?"  # Pregunta de seguimiento
})

response = llm.invoke(prompt)
print(response.content)  # Responde en contexto del historial
