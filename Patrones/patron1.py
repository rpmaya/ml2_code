import os
from typing import Optional, Generator

class LLMClient:
    """
    Cliente unificado para múltiples proveedores de LLM.
    Permite cambiar de proveedor con una línea de código.
    """
    
    PROVIDERS = ["openai", "anthropic", "google"]
    
    def __init__(self, provider: str = "openai", model: Optional[str] = None):
        if provider not in self.PROVIDERS:
            raise ValueError(f"Proveedor debe ser uno de: {self.PROVIDERS}")
        
        self.provider = provider
        self._setup_client(model)
    
    def _setup_client(self, model: Optional[str]):
        """Inicializa el cliente según el proveedor."""
        if self.provider == "openai":
            from openai import OpenAI
            self.client = OpenAI()
            self.model = model or "gpt-4o-mini"
            
        elif self.provider == "anthropic":
            from anthropic import Anthropic
            self.client = Anthropic()
            self.model = model or "claude-3-sonnet-20240229"
            
        elif self.provider == "google":
            import google.generativeai as genai
            genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
            self.model = model or "gemini-pro"
            self.client = genai.GenerativeModel(self.model)
    
    def chat(self, prompt: str, system: Optional[str] = None, 
             temperature: float = 0.7) -> str:
        """
        Envía un mensaje y obtiene respuesta.
        Interfaz unificada para todos los proveedores.
        """
        if self.provider == "openai":
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
            
        elif self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system or "",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
            
        elif self.provider == "google":
            # Gemini no tiene system prompt nativo, lo añadimos al prompt
            full_prompt = f"{system}\n\n{prompt}" if system else prompt
            response = self.client.generate_content(full_prompt)
            return response.text
    
    def chat_stream(self, prompt: str, system: Optional[str] = None) -> Generator[str, None, None]:
        """Streaming unificado para todos los proveedores."""
        if self.provider == "openai":
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        elif self.provider == "anthropic":
            with self.client.messages.stream(
                model=self.model,
                max_tokens=1024,
                system=system or "",
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                for text in stream.text_stream:
                    yield text
                    
        elif self.provider == "google":
            full_prompt = f"{system}\n\n{prompt}" if system else prompt
            response = self.client.generate_content(full_prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text


# Uso: cambiar de proveedor es trivial
llm = LLMClient(provider="openai")
print(llm.chat("Hola", system="Responde en español"))

llm = LLMClient(provider="anthropic")  # Mismo código, diferente modelo
print(llm.chat("Hola", system="Responde en español"))
