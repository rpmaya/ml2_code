// Frontend: consumir streaming desde el navegador
const eventSource = new EventSource(`/chat/stream?prompt=${encodeURIComponent(prompt)}`);

eventSource.onmessage = (event) => {
    if (event.data === '[DONE]') {
        eventSource.close();
        return;
    }
    // Añadir texto al contenedor de respuesta
    document.getElementById('response').textContent += event.data;
};

eventSource.onerror = () => {
    eventSource.close();
};
