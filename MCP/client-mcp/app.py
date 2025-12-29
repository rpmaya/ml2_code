import streamlit as st
from client import MCPClient

# Configuración de la página
st.set_page_config(
    page_title="Cliente MCP",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Cliente MCP con Streamlit")

# Inicializar cliente en session_state
if "mcp_client" not in st.session_state:
    st.session_state.mcp_client = None
    st.session_state.messages = []
    st.session_state.connected = False

# Sidebar para configuración
with st.sidebar:
    st.header("⚙️ Configuración")
    
    server_path = st.text_input(
        "Ruta al servidor MCP",
        value="./gmail_mcp_server.py"
    )
    
    if st.button("Conectar" if not st.session_state.connected else "Desconectar"):
        if not st.session_state.connected:
            try:
                client = MCPClient(["python", server_path])
                client.connect()
                st.session_state.mcp_client = client
                st.session_state.connected = True
                st.success(f"✅ Conectado. {len(client.tools)} herramientas disponibles.")
            except Exception as e:
                st.error(f"❌ Error de conexión: {e}")
        else:
            st.session_state.mcp_client.disconnect()
            st.session_state.mcp_client = None
            st.session_state.connected = False
            st.info("Desconectado")
    
    # Mostrar herramientas disponibles
    if st.session_state.connected and st.session_state.mcp_client:
        st.header("🔧 Herramientas")
        for tool in st.session_state.mcp_client.tools:
            with st.expander(tool["name"]):
                st.write(tool.get("description", "Sin descripción"))

# Área principal de chat
st.header("💬 Chat")

# Mostrar historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("Escribe tu mensaje..."):
    if not st.session_state.connected:
        st.warning("⚠️ Conecta primero con un servidor MCP")
    else:
        # Mostrar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Obtener respuesta
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = st.session_state.mcp_client.chat(prompt)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
