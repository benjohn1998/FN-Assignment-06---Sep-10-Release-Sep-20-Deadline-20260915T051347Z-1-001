import requests
from config import MODEL_NAME, OLLAMA_URL

def chat(messages, temperature=0.0, json_mode=False):
    """Send messages to Ollama and return the response content."""
    
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "think": False,
        "options": {
            "temperature": temperature,
        },
    }

    if json_mode:
        payload["format"] = "json"

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300,
    )

    response.raise_for_status()

    return response.json()["message"]["content"]