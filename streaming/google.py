import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

def chat_streaming_gemini(prompt: str):
    """Streaming con Gemini."""
    response = model.generate_content(prompt, stream=True)
    
    full_response = ""
    for chunk in response:
        if chunk.text:
            print(chunk.text, end="", flush=True)
            full_response += chunk.text
    
    print()
    return full_response
