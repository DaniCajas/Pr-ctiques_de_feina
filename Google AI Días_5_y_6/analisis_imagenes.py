import os
import sys
import json
from pathlib import Path
from google import genai
from PIL import Image

IMAGE_DIR = Path("imagenes_test")
SUPPORTED_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

PROMPTS = {
    "ocr": "Extrae TODO el texto visible en esta imagen. Si no hay texto, responde 'SIN TEXTO'. Devuelve solo el texto extraído, sin explicaciones.",
    "descripcion": "Describe detalladamente el contenido visual de esta imagen: objetos, personas, escena, colores, composición, texto visible. Máximo 3 frases.",
    "clasificacion": "Clasifica la escena de esta imagen en UNA sola categoría: documento, urbano, naturaleza, interior, producto, persona, vehículo, arte, otro. Responde solo con la categoría.",
    "objetos": "Lista los objetos principales detectados en la imagen (máx 10), uno por línea, formato: 'objeto: confianza_alta/media/baja'. Sin texto adicional."
}

def get_api_key():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: Variable de entorno GEMINI_API_KEY no encontrada.")
        print("Configúrala en PowerShell: $env:GEMINI_API_KEY = 'tu_clave'")
        sys.exit(1)
    return api_key

def get_image_files():
    if not IMAGE_DIR.exists():
        print(f"ERROR: Carpeta '{IMAGE_DIR}' no existe. Créala y pon ahí 5 imágenes de test.")
        sys.exit(1)
    files = [f for f in IMAGE_DIR.iterdir() if f.suffix.lower() in SUPPORTED_EXTS]
    if not files:
        print(f"ERROR: No hay imágenes en '{IMAGE_DIR}'. Añade 5 archivos (png, jpg, jpeg, webp, bmp).")
        sys.exit(1)
    print(f"Encontradas {len(files)} imágenes en {IMAGE_DIR}")
    return files

def analyze_image(client, image_path, task_name, prompt):
    try:
        image = Image.open(image_path)
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=[prompt, image]
        )
        return response.text.strip()
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            return "ERROR: Cuota agotada (429)"
        elif "503" in error_msg or "UNAVAILABLE" in error_msg:
            return "ERROR: Servicio no disponible (503)"
        else:
            return f"ERROR: {error_msg}"

def process_all_images(client, image_files):
    results = []
    for img_path in image_files:
        print(f"\nProcesando: {img_path.name}")
        img_result = {"archivo": img_path.name}
        for task, prompt in PROMPTS.items():
            print(f"  - {task}...", end=" ", flush=True)
            result = analyze_image(client, img_path, task, prompt)
            img_result[task] = result
            print("OK")
        results.append(img_result)
    return results

def print_results(results):
    print(f"\n{'='*80}")
    print(f"RESULTADOS ANÁLISIS DE IMÁGENES ({len(results)} imágenes)")
    print(f"{'='*80}")
    for r in results:
        print(f"\n--- {r['archivo']} ---")
        for task in PROMPTS.keys():
            val = r[task]
            display = val[:120] + "..." if len(val) > 120 else val
            print(f"  {task:12}: {display}")

def save_json(results, filename="resultados_imagenes.json"):
    if not results:
        return
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nResultados guardados en {filename}")

def generate_comparison_table(results):
    print(f"\n{'='*80}")
    print("TABLA COMPARATIVA DE PRECISIÓN (rellena manualmente)")
    print(f"{'='*80}")
    print(f"{'Archivo':<25} {'OCR':<10} {'Descripción':<12} {'Clasificación':<14} {'Objetos':<10}")
    print("-" * 80)
    for r in results:
        name = r['archivo'][:24]
        print(f"{name:<25} {'✓/✗':<10} {'✓/✗':<12} {'✓/✗':<14} {'✓/✗':<10}")
    print("\nMarca ✓ si el resultado es correcto, ✗ si falla. Anota detalles en el notebook.")

def main():
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)

    print("=" * 80)
    print("ANÁLISIS MULTIMODAL DE IMÁGENES CON GEMINI API")
    print("=" * 80)

    image_files = get_image_files()
    results = process_all_images(client, image_files)
    print_results(results)
    save_json(results)
    generate_comparison_table(results)

    print("\nPróximo paso: abre 'analisis_resultados.ipynb' para documentar la comparativa.")

if __name__ == "__main__":
    main()