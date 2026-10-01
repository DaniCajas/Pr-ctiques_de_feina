import os
from google import genai
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
if not api_key:
    raise ValueError("No se encontró GEMINI_API_KEY")
textos = [
    "Me encanta este producto, funciona perfectamente.",
    "El servicio fue muy lento y decepcionante.",
    "Microsoft anunció nuevas funciones de inteligencia artificial."
]