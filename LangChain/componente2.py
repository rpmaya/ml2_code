from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Template básico con variables
template_basico = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto en {lenguaje}. Responde de forma {estilo}."),
    ("human", "{pregunta}")
])

# Generar prompt con valores específicos
prompt = template_basico.invoke({
    "lenguaje": "Python",
    "estilo": "concisa y con ejemplos de código",
    "pregunta": "¿Cómo uso list comprehensions?"
})

print(prompt)
# Salida: mensajes formateados listos para enviar al modelo

# Usar con el modelo
response = llm.invoke(prompt)
print(response.content)

