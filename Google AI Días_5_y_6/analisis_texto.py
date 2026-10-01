import os
import sys
import json
from google import genai

texts = [
    "Google presentó ayer su nuevo modelo Gemini 3.8 Flash en Mountain View, California. El CEO Sundar Pichai destacó que es un 40% más rápido que la versión anterior.",
    "La película 'Oppenheimer' de Christopher Nolan ha recibido críticas excelentes. Cillian Murphy ofrece una actuación magistral como el físico teórico.",
    "El clima en Madrid hoy será soleado con temperaturas máximas de 28°C. No se esperan lluvias hasta el fin de semana según la AEMET.",
    "Amazon anunció despidos masivos en su división de Alexa. Más de 10.000 empleados serán afectados en los próximos meses.",
    "El Barcelona ganó 3-1 al Real Madrid en el Camp Nou. Lewandowski marcó dos goles y dio una asistencia en el clásico.",
    "Microsoft lanzó Copilot Pro por 22€/mes. Integra GPT-4 Turbo en Office 365 y ofrece prioridad en horas punta.",
    "La inflación en la zona euro bajó al 2.4% en noviembre. El BCE podría recortar tipos en primavera según analistas.",
    "Taylor Swift batió récords con 'The Eras Tour'. La gira recaudó más de 1.000 millones de dólares en taquilla.",
    "SpaceX lanzó 23 satélites Starlink desde Cabo Cañaveral. El cohete Falcon 9 aterrizó exitosamente en el dron 'Just Read the Instructions'.",
    "El nuevo iPhone 16 Pro incluirá botón de acción personalizable y chip A18 Pro según filtraciones recientes de Ming-Chi Kuo."
]

def get_api_key():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: Variable de entorno GEMINI_API_KEY no encontrada.")
        print("Configúrala en PowerShell: $env:GEMINI_API_KEY = 'tu_clave'")
        sys.exit(1)
    return api_key

def build_prompt(texts):
    texts_block = "\n".join(f'TEXTO {i+1}: "{t}"' for i, t in enumerate(texts))
    return f"""Analiza los siguientes {len(texts)} textos. Para CADA texto devuelve SOLO un objeto JSON en una línea con esta estructura exacta:

{{
  "texto_id": N,
  "idioma": "es|en|otro",
  "entidades": ["entidad1", "entidad2", ...],
  "sentimiento": "positivo|negativo|neutro",
  "resumen": "resumen en una frase (máx 20 palabras)"
}}

TEXTOS:
{texts_block}

RESPONDE SOLO con {len(texts)} líneas JSON, una por texto, sin texto adicional ni markdown."""

def parse_responses(response_text, expected_count):
    results = []
    for line in response_text.strip().split("\n"):
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            data = json.loads(line)
            if "texto_id" in data and "idioma" in data:
                results.append(data)
        except json.JSONDecodeError:
            continue
    return results

def analyze_texts(client, texts):
    prompt = build_prompt(texts)
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        return parse_responses(response.text, len(texts))
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            print("ERROR: Cuota agotada (429). Espera y reintenta.")
        elif "503" in error_msg or "UNAVAILABLE" in error_msg:
            print("ERROR: Servicio no disponible (503). Reintenta luego.")
        else:
            print(f"ERROR en llamada a Gemini: {error_msg}")
        return None

def print_results(results):
    if not results:
        return
    print(f"\n{'='*80}")
    print(f"RESULTADOS ANÁLISIS DE TEXTO ({len(results)} textos)")
    print(f"{'='*80}")
    for r in results:
        print(f"\n--- Texto {r['texto_id']} ---")
        print(f"Idioma:      {r['idioma']}")
        print(f"Entidades:   {', '.join(r['entidades']) if r['entidades'] else 'Ninguna'}")
        print(f"Sentimiento: {r['sentimiento']}")
        print(f"Resumen:     {r['resumen']}")

def save_json(results, filename="resultados_texto.json"):
    if not results:
        return
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nResultados guardados en {filename}")

def main():
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)

    print("=" * 80)
    print("ANÁLISIS AVANZADO DE TEXTO CON GEMINI API")
    print("=" * 80)
    print(f"Procesando {len(texts)} textos...")

    results = analyze_texts(client, texts)
    print_results(results)
    save_json(results)

    print("\n" + "=" * 80)
    print("COMPARATIVA DE PRECISIÓN (revisión manual)")
    print("=" * 80)
    print("Compara cada campo con el texto original y anota aciertos/fallos.")
    print("Campos a evaluar: idioma, entidades, sentimiento, resumen.")

if __name__ == "__main__":
    main()