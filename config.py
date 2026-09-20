import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

if not OLLAMA_URL or not MODEL_NAME: 
    raise ValueError(
            "OLLAMA_URL and MODEL_NAME must be set in the .env file."
    )