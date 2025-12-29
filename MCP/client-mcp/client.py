import subprocess
import json
import os
from openai import OpenAI

class MCPClient:
    def __init__(self, server_command: list):
        """
        Inicializa el cliente MCP.
        
        Args:
            server_command: Comando para arrancar el servidor MCP
        """
        self.server_command = server_command
        self.process = None
        self.tools = []
        self.openai_client = OpenAI()
        self.conversation_history = []
    
    def connect(self):
        """Conecta con el servidor MCP via STDIO."""
        self.process = subprocess.Popen(
            self.server_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Descubrir herramientas disponibles
        self._discover_tools()
    
    def _send_request(self, method: str, params: dict = None) -> dict:
        """Envía una petición JSON-RPC al servidor."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }
        
        self.process.stdin.write(json.dumps(request) + "\n")
        self.process.stdin.flush()
        
        response_line = self.process.stdout.readline()
        return json.loads(response_line)
    
    def _discover_tools(self):
        """Obtiene la lista de herramientas del servidor."""
        response = self._send_request("tools/list")
        self.tools = response.get("result", {}).get("tools", [])
    
    def get_tools_for_openai(self) -> list:
        """Convierte tools al formato OpenAI."""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("inputSchema", {})
                }
            }
            for tool in self.tools
        ]
    
    def call_tool(self, name: str, arguments: dict) -> dict:
        """Invoca una herramienta en el servidor MCP."""
        response = self._send_request("tools/call", {
            "name": name,
            "arguments": arguments
        })
        return response.get("result", {})
    
    def chat(self, user_message: str) -> str:
        """
        Procesa un mensaje del usuario y devuelve la respuesta.
        """
        # Añadir mensaje del usuario al historial
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Primera llamada al LLM
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.conversation_history,
            tools=self.get_tools_for_openai() if self.tools else None
        )
        
        assistant_message = response.choices[0].message
        
        # Procesar tool calls si existen
        if assistant_message.tool_calls:
            # Añadir mensaje del asistente con las tool calls
            self.conversation_history.append(assistant_message)
            
            # Ejecutar cada tool call
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                # Invocar la herramienta
                result = self.call_tool(tool_name, arguments)
                
                # Añadir resultado al historial
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
            
            # Segunda llamada al LLM con los resultados
            final_response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.conversation_history
            )
            
            final_message = final_response.choices[0].message.content
            self.conversation_history.append({
                "role": "assistant",
                "content": final_message
            })
            
            return final_message
        
        # Sin tool calls, devolver respuesta directa
        content = assistant_message.content
        self.conversation_history.append({
            "role": "assistant",
            "content": content
        })
        
        return content
    
    def disconnect(self):
        """Cierra la conexión con el servidor."""
        if self.process:
            self.process.terminate()
            self.process = None
