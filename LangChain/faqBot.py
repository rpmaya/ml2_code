"""
FAQ Bot con RAG usando LangChain
================================
Sistema completo de preguntas y respuestas sobre documentación empresarial.
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

load_dotenv()
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class FAQBot:
    """Bot de preguntas frecuentes basado en RAG."""
    
    def __init__(self, docs_path: str, db_path: str = "./chroma_db"):
        self.docs_path = docs_path
        self.db_path = db_path
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        self.vectorstore = None
        self.chain = None
    
    def cargar_documentos(self) -> list:
        """Carga documentos desde el directorio especificado."""
        loader = DirectoryLoader(
            self.docs_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
            show_progress=True
        )
        return loader.load()
    
    def procesar_documentos(self, documentos: list) -> list:
        """Divide documentos en chunks."""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        return splitter.split_documents(documentos)
    
    def crear_indice(self, force_rebuild: bool = False):
        """Crea o carga el índice vectorial."""
        if os.path.exists(self.db_path) and not force_rebuild:
            print("Cargando índice existente...")
            self.vectorstore = Chroma(
                persist_directory=self.db_path,
                embedding_function=self.embeddings
            )
        else:
            print("Construyendo nuevo índice...")
            documentos = self.cargar_documentos()
            chunks = self.procesar_documentos(documentos)
            self.vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=self.db_path
            )
        print(f"Índice listo con {self.vectorstore._collection.count()} chunks")
    
    def construir_chain(self):
        """Construye la chain RAG."""
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 4}
        )
        
        template = """Eres un asistente de FAQ que responde preguntas basándose
        ÚNICAMENTE en el contexto proporcionado.
        
        Contexto:
        {context}
        
        Pregunta: {question}
        
        Respuesta (sé conciso y preciso):"""
        
        prompt = ChatPromptTemplate.from_template(template)
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        self.chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
    
    def preguntar(self, pregunta: str) -> str:
        """Realiza una pregunta al sistema RAG."""
        if not self.chain:
            self.construir_chain()
        return self.chain.invoke(pregunta)
    
    def iniciar_chat(self):
        """Inicia un loop de chat interactivo."""
        print("\n=== FAQ Bot ===")
        print("Escribe 'salir' para terminar\n")
        
        while True:
            pregunta = input("Tú: ").strip()
            if pregunta.lower() in ['salir', 'exit', 'quit']:
                print("¡Hasta luego!")
                break
            if not pregunta:
                continue
            
            respuesta = self.preguntar(pregunta)
            print(f"\nBot: {respuesta}\n")


# Uso del bot
if __name__ == "__main__":
    bot = FAQBot(docs_path="./documentos/")
    bot.crear_indice()
    bot.iniciar_chat()
