from langchain_core.runnables import RunnablePassthrough

# Chain 1: Generar código
template_codigo = ChatPromptTemplate.from_messages([
    ("system", "Eres un programador experto. Genera solo código Python, sin explicaciones."),
    ("human", "Escribe una función que {tarea}")
])

chain_codigo = template_codigo | llm | StrOutputParser()

# Chain 2: Analizar el código generado
template_analisis = ChatPromptTemplate.from_messages([
    ("system", "Eres un revisor de código. Analiza el código y sugiere mejoras."),
    ("human", "Analiza este código:\n```python\n{codigo}\n```")
])

chain_analisis = template_analisis | llm | StrOutputParser()

# Chain combinada: generar → analizar
chain_completa = (
    {"tarea": RunnablePassthrough()}  # Pasar input original
    | chain_codigo  # Genera código
    | {"codigo": RunnablePassthrough()}  # El resultado pasa como 'codigo'
    | chain_analisis  # Analiza el código
)

# Una sola llamada ejecuta todo el pipeline
resultado = chain_completa.invoke("calcule el factorial de un número")
print(resultado)
