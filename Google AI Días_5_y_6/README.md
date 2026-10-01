# Google AI Studio y API de Gemini - Día 5 y Día 6

## Entorno utilizado
- Windows
- Python 3.14.7
- Google AI Studio
- API de Gemini (modelo `gemini-3.8-flash`)
- Librería `google-genai` + `Pillow` (imágenes)
- Ejecución con `py` (en este equipo `python` no está en PATH)

---

## DÍA 5 - Análisis de Sentimiento y Prueba Multimodal

### Archivos Día 5
- `gemini_sentiment.py`: **Prueba real de la API de Gemini**. Conecta vía `google-genai`, lee API Key desde `GEMINI_API_KEY`, analiza sentimiento de 10 textos (5 español + 5 inglés) en 2 peticiones.
- `sentiment_analysis.py`: **Ejemplo local solamente** (reglas de palabras clave). NO usa la API de Gemini.
- `Captura de pantalla 2026-09-28 123952.png`: Prueba multimodal en Google AI Studio (prompt: "Describe esta imagen e identifica los elementos principales").

### Ejecución Día 5
```powershell
$env:GEMINI_API_KEY = "tu_clave"
py gemini_sentiment.py
```

---

## DÍA 6 - Análisis Avanzado: Texto y Visión Multimodal

### Archivos Día 6
- `analisis_texto.py`: Análisis de 10 textos (noticias, reseñas, emails) → **idioma, entidades, sentimiento, resumen** en JSON.
- `analisis_imagenes.py`: Análisis de 5 imágenes en `imagenes_test/` → **OCR, descripción, clasificación escena, objetos**.
- `analisis_resultados.ipynb`: Notebook Jupyter para comparativa de precisión (rellenar manualmente).
- `imagenes_test/`: Carpeta para tus 5 imágenes de prueba (documentos, urbano, productos, etc.).
- `resultados_texto.json` / `resultados_imagenes.json`: Salidas generadas por los scripts.

### Requisitos adicionales
```powershell
pip install pillow
```

### Ejecución Día 6
```powershell
# 1. Pon tus 5 imágenes en imagenes_test/
# 2. Análisis de texto
$env:GEMINI_API_KEY = "tu_clave"
py analisis_texto.py

# 3. Análisis de imágenes
py analisis_imagenes.py

# 4. Abre el notebook para documentar resultados
jupyter notebook analisis_resultados.ipynb
```

### Qué hace cada script

#### `analisis_texto.py`
- Procesa 10 textos variados en **una sola petición** (ahorra cuota).
- Pide JSON estructurado por texto: `idioma`, `entidades[]`, `sentimiento`, `resumen`.
- Guarda `resultados_texto.json`.
- Incluye plantilla de comparativa manual en salida.

#### `analisis_imagenes.py`
- Procesa cada imagen con **4 prompts específicos** (OCR, descripción, clasificación, objetos).
- Guarda `resultados_imagenes.json`.
- Genera tabla comparativa para rellenar en notebook.

#### `analisis_resultados.ipynb`
- Carga ambos JSON.
- Muestra texto original vs resultado para evaluar cada campo.
- Incluye contadores para métricas de precisión.
- Espacio para observaciones de errores comunes.

### Manejo de errores (ambos scripts)
- `GEMINI_API_KEY` no configurada → mensaje claro + instrucciones.
- `429 RESOURCE_EXHAUSTED` → "Cuota agotada, espera".
- `503 UNAVAILABLE` → "Servicio no disponible, reintenta".
- Otros errores → mensaje real, **no se inventan resultados**.

### Instalación completa
```powershell
pip install google-genai pillow
```

### Configuración API Key (igual que Día 5)
```powershell
$env:GEMINI_API_KEY = "tu_clave_real"
# Obtener en: https://aistudio.google.com → Get API key
```

---

## Notas
- No hay claves hardcodeadas ni límites de cuota fijos en el código.
- Modelo usado: `gemini-3.8-flash` (actual según API).
- Prueba multimodal Día 5: documentada con captura en Google AI Studio.
- Día 6: análisis multimodal **vía Python API** + evaluación manual en notebook.