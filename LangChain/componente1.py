from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Instanciar modelos de diferentes proveedores
llm_openai = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

llm_claude = ChatAnthropic(
    model="claude-3-sonnet-20240229",
    temperature=0.7
)

llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.7
)

# MISMO CÓDIGO para cualquier modelo
messages = [
    SystemMessage(content="Eres un experto en Python. Responde de forma concisa."),
    HumanMessage(content="¿Qué es un decorador?")
]

# Cambiar de proveedor es cambiar UNA variable
llm = llm_openai  # o llm_claude, o llm_gemini

response = llm.invoke(messages)
print(response.content)
