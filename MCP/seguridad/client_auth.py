class MCPClientAuthenticated:
    def __init__(self, server_url: str, token: str):
        self.server_url = server_url
        self.token = token
    
    def _load_token(self, token_file: str) -> str:
        """Carga el token desde un archivo."""
        with open(token_file, "r") as f:
            return f.read().strip()
    
    def send_request(self, method: str, params: dict = None) -> dict:
        """Envía una petición autenticada al servidor."""
        import requests
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }
        
        response = requests.post(
            self.server_url,
            json=payload,
            headers=headers
        )
        
        return response.json()
