from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# Definir estructura de salida esperada
class AnalisisSentimiento(BaseModel):
    sentimiento: str = Field(description="POSITIVO, NEGATIVO o NEUTRO")
    confianza: float = Field(description="Valor entre 0 y 1")
    palabras_clave: list[str] = Field(description="Palabras que justifican el análisis")

# Parser que valida contra el modelo Pydantic
parser = JsonOutputParser(pydantic_object=AnalisisSentimiento)

template = ChatPromptTemplate.from_messages([
    ("system", """Analiza el sentimiento del texto.
{format_instructions}"""),
    ("human", "{texto}")
])

chain = template | llm | parser

resultado = chain.invoke({
    "texto": "Este producto superó todas mis expectativas, ¡lo recomiendo!",
    "format_instructions": parser.get_format_instructions()
})

print(resultado)
# {'sentimiento': 'POSITIVO', 'confianza': 0.95, 'palabras_clave': ['superó', 'expectativas', 'recomiendo']}
print(type(resultado))  # <class 'dict'>
