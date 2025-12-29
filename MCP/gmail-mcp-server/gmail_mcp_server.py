from fastmcp import FastMCP
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText
import os

# Permisos que solicitamos a Gmail
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

# Rutas de archivos de credenciales
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

# Crear servidor MCP
mcp = FastMCP("Gmail Manager")


def get_gmail_service():
    """
    Obtiene un cliente autenticado para la API de Gmail.
    Gestiona el flujo OAuth automáticamente.
    """
    creds = None
    
    # Verificar si ya tenemos un token guardado
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # Si no hay credenciales válidas, iniciar flujo OAuth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refrescar token expirado
            creds.refresh(Request())
        else:
            # Iniciar flujo de autorización interactivo
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Guardar token para próximas ejecuciones
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    # Construir y devolver el servicio de Gmail
    return build('gmail', 'v1', credentials=creds)


# ============== TOOLS ==============

@mcp.tool
def list_emails(max_results: int = 10, query: str = "") -> list:
    """
    Lista los emails de la bandeja de entrada.
    
    Args:
        max_results: Número máximo de emails a devolver (1-50)
        query: Filtro de búsqueda (ej: "is:unread", "from:ejemplo@gmail.com")
    
    Returns:
        Lista de emails con id, remitente, asunto y fragmento
    """
    service = get_gmail_service()
    
    # Limitar resultados para evitar respuestas muy grandes
    max_results = min(max(1, max_results), 50)
    
    # Obtener lista de mensajes
    results = service.users().messages().list(
        userId='me',
        maxResults=max_results,
        q=query
    ).execute()
    
    messages = results.get('messages', [])
    
    if not messages:
        return []
    
    emails = []
    for msg in messages:
        # Obtener detalles de cada mensaje
        message = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='metadata',
            metadataHeaders=['From', 'Subject']
        ).execute()
        
        # Extraer cabeceras
        headers = {h['name']: h['value'] for h in message['payload']['headers']}
        
        emails.append({
            'id': message['id'],
            'from': headers.get('From', 'Desconocido'),
            'subject': headers.get('Subject', 'Sin asunto'),
            'snippet': message.get('snippet', '')[:100]
        })
    
    return emails


@mcp.tool
def send_email(to: str, subject: str, body: str) -> dict:
    """
    Envía un email desde la cuenta del usuario.
    
    Args:
        to: Dirección de email del destinatario
        subject: Asunto del email
        body: Cuerpo del mensaje en texto plano
    
    Returns:
        Estado del envío con el ID del mensaje
    """
    service = get_gmail_service()
    
    # Crear el mensaje MIME
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    
    # Codificar en base64 para la API
    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode('utf-8')
    
    try:
        # Enviar el mensaje
        sent_message = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        
        return {
            'status': 'enviado',
            'message_id': sent_message['id'],
            'to': to,
            'subject': subject
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }


# ============== RESOURCES ==============

@mcp.resource("gmail://profile")
def get_profile() -> dict:
    """
    Obtiene información del perfil de Gmail del usuario.
    """
    service = get_gmail_service()
    
    profile = service.users().getProfile(userId='me').execute()
    
    return {
        'email': profile.get('emailAddress'),
        'total_messages': profile.get('messagesTotal'),
        'total_threads': profile.get('threadsTotal')
    }


# ============== PROMPTS ==============

@mcp.prompt()
def redactar_email(destinatario: str, asunto: str) -> str:
    """
    Prompt para redactar un email profesional.
    
    Args:
        destinatario: Email del destinatario
        asunto: Asunto del email
    """
    return f"""Ayúdame a redactar un email profesional.

DESTINATARIO: {destinatario}
ASUNTO: {asunto}

Por favor, redacta el cuerpo del email siguiendo estas pautas:
- Tono profesional pero cercano
- Estructura clara con saludo, cuerpo y despedida
- Conciso y directo al punto

Una vez redactado, usa la herramienta send_email para enviarlo."""


# Punto de entrada
if __name__ == "__main__":
    mcp.run()
