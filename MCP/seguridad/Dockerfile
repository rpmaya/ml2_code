FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Puerto que expondrá el servidor
EXPOSE 8000

# Comando de inicio
CMD ["python", "mcp_server.py"]
