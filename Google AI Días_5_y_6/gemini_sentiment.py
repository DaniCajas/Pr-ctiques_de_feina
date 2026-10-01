import os
import sys
from google import genai

texts_spanish = [
    "Me encanta este producto, es increíble y superó mis expectativas.",
    "El servicio fue terrible, muy lento y el personal grosero.",
    "El clima hoy está nublado, ni frío ni calor.",
    "¡Qué película tan maravillosa! La recomiendo totalmente.",
    "No me gustó la comida, estaba fría y sin sabor."
]

texts_english = [
    "I absolutely love this product, it's amazing and exceeded my expectations.",
    "The service was terrible, very slow and the staff was rude.",
    "The weather today is cloudy, neither hot nor cold.",
    "What a wonderful movie! I totally recommend it.",
    "I didn't like the food, it was cold and tasteless."
]

def get_api_key():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: Variable de entorno GEMINI_API_KEY no encontrada.")
        print()
        print("Para configurarla:")
        print("  1. Ve a https://aistudio.google.com")
        print("  2. Inicia sesión y haz clic en 'Get API key'")
        print("  3. Crea una clave y cópiala")
        print("  4. En PowerShell:")
        print("     $env:GEMINI_API_KEY = 'tu_clave_aqui'")
        print("  5. Ejecuta de nuevo: py gemini_sentiment.py")
        sys.exit(1)
    return api_key

def build_prompt(texts, language):
    if language == "español":
        return (
            "Analiza el sentimiento de cada uno de los siguientes textos en español. "
            "Para cada texto, responde SOLO con una línea en formato: "
            "TEXTO N: positivo|negativo|neutro\n\n"
            + "\n".join(f"TEXTO {i+1}: {t}" for i, t in enumerate(texts))
        )
    else:
        return (
            "Analyze the sentiment of each of the following English texts. "
            "For each text, respond ONLY with one line in format: "
            "TEXT N: positive|negative|neutral\n\n"
            + "\n".join(f"TEXT {i+1}: {t}" for i, t in enumerate(texts))
        )

def parse_response(response_text, language, texts):
    results = []
    lines = response_text.strip().split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if language == "español" and line.startswith("TEXTO "):
            try:
                parts = line.split(": ", 1)
                if len(parts) == 2:
                    sentiment = parts[1].strip().lower()
                    if sentiment in ("positivo", "negativo", "neutro"):
                        results.append(sentiment)
            except:
                pass
        elif language == "inglés" and line.startswith("TEXT "):
            try:
                parts = line.split(": ", 1)
                if len(parts) == 2:
                    sentiment = parts[1].strip().lower()
                    if sentiment in ("positive", "negative", "neutral"):
                        es_map = {"positive": "positivo", "negative": "negativo", "neutral": "neutro"}
                        results.append(es_map[sentiment])
            except:
                pass
    return results

def analyze_with_gemini(client, texts, language):
    prompt = build_prompt(texts, language)
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        return parse_response(response.text, language, texts)
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            print("ERROR: Cuota de API agotada (429 RESOURCE_EXHAUSTED).")
            print("Espera unos minutos y vuelve a intentarlo.")
        else:
            print(f"ERROR en la llamada a Gemini: {error_msg}")
        return None

def main():
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)

    print("=" * 60)
    print("ANÁLISIS DE SENTIMIENTO CON GEMINI API")
    print("=" * 60)

    print("\n--- Español ---")
    results_es = analyze_with_gemini(client, texts_spanish, "español")
    if results_es:
        for i, (text, sentiment) in enumerate(zip(texts_spanish, results_es), 1):
            print(f"\nTexto {i}: {text}")
            print(f"Sentimiento: {sentiment}")
    else:
        print("No se pudo obtener análisis para español.")

    print("\n--- Inglés ---")
    results_en = analyze_with_gemini(client, texts_english, "inglés")
    if results_en:
        for i, (text, sentiment) in enumerate(zip(texts_english, results_en), 1):
            print(f"\nTexto {i}: {text}")
            print(f"Sentimiento: {sentiment}")
    else:
        print("No se pudo obtener análisis para inglés.")

    print("\n" + "=" * 60)
    print("PRUEBA MULTIMODAL")
    print("=" * 60)
    print("La prueba multimodal se realizó en Google AI Studio.")
    print("Ver captura: 'Captura de pantalla 2026-09-28 123952.png'")
    print("Prompt usado: 'Describe esta imagen e identifica los elementos principales.'")
    print("Gemini analizó correctamente la imagen identificando la interfaz de Google AI Studio.")

if __name__ == "__main__":
    main()