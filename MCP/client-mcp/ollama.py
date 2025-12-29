import ollama

class MCPClientOllama(MCPClient):
    def __init__(self, server_command: list, model: str = "qwen3:8b"):
        super().__init__(server_command)
        self.model = model
    
    def chat(self, user_message: str) -> str:
        """
        Procesa un mensaje usando Ollama en lugar de OpenAI.
        """
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Llamada a Ollama
        response = ollama.chat(
            model=self.model,
            messages=self.conversation_history,
            tools=self.get_tools_for_openai() if self.tools else None
        )
        
        assistant_message = response["message"]
        
        # Procesar tool calls
        if "tool_calls" in assistant_message:
            self.conversation_history.append(assistant_message)
            
            for tool_call in assistant_message["tool_calls"]:
                tool_name = tool_call["function"]["name"]
                arguments = tool_call["function"]["arguments"]
                
                result = self.call_tool(tool_name, arguments)
                
                self.conversation_history.append({
                    "role": "tool",
                    "content": json.dumps(result)
                })
            
            # Segunda llamada con resultados
            final_response = ollama.chat(
                model=self.model,
                messages=self.conversation_history
            )
            
            final_content = final_response["message"]["content"]
            self.conversation_history.append({
                "role": "assistant",
                "content": final_content
            })
            
            return final_content
        
        content = assistant_message["content"]
        self.conversation_history.append({
            "role": "assistant",
            "content": content
        })
        
        return content
