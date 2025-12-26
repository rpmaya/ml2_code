from langchain_core.runnables import RunnableBranch

# Diferentes templates según el tipo de pregunta
template_tecnico = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto técnico. Responde con precisión y ejemplos de código."),
    ("human", "{pregunta}")
])

template_conceptual = ChatPromptTemplate.from_messages([
    ("system", "Eres un profesor. Explica conceptos de forma simple con analogías."),
    ("human", "{pregunta}")
])

template_default = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente general."),
    ("human", "{pregunta}")
])

# Función para clasificar la pregunta
def es_tecnica(input_dict):
    pregunta = input_dict["pregunta"].lower()
    palabras_tecnicas = ["código", "implementar", "función", "error", "bug", "api"]
    return any(palabra in pregunta for palabra in palabras_tecnicas)

def es_conceptual(input_dict):
    pregunta = input_dict["pregunta"].lower()
    palabras_conceptuales = ["qué es", "explica", "concepto", "diferencia entre"]
    return any(palabra in pregunta for palabra in palabras_conceptuales)

# Branch que selecciona el template apropiado
branch = RunnableBranch(
    (es_tecnica, template_tecnico | llm | StrOutputParser()),
    (es_conceptual, template_conceptual | llm | StrOutputParser()),
    template_default | llm | StrOutputParser()  # Default
)

# Uso
print(branch.invoke({"pregunta": "Implementa una función de ordenamiento"}))  # Técnico
print(branch.invoke({"pregunta": "¿Qué es la recursión?"}))  # Conceptual

