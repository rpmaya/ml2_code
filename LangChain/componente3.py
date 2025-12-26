from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

# Chain simple: prompt → modelo → parser de string
template = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto en {tema}."),
    ("human", "{pregunta}")
])

chain = template | llm | StrOutputParser()

# Ejecutar toda la cadena con una sola llamada
resultado = chain.invoke({
    "tema": "bases de datos",
    "pregunta": "¿Cuál es la diferencia entre SQL y NoSQL?"
})

print(resultado)  # String directamente, no objeto Message
