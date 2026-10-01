import re

POSITIVE_ES = {
    'encanta', 'increíble', 'superó', 'expectativas', 'maravillosa', 'recomiendo',
    'excelente', 'bueno', 'genial', 'fantástico', 'perfecto', 'mejor', 'feliz',
    'contento', 'satisfecho', 'agradable', 'bonito', 'hermoso', 'gusto', 'amo',
    'adoro', 'fascinante', 'espectacular', 'magnífico', 'espléndido', 'divino'
}

NEGATIVE_ES = {
    'terrible', 'lento', 'grosero', 'fría', 'sabor', 'no gustó', 'malo', 'horrible',
    'pésimo', 'decepcionante', 'frustrado', 'enojado', 'molesto', 'insatisfecho',
    'feo', 'horrible', 'detesto', 'odio', 'aburrido', 'inútil', 'basura', 'asqueroso'
}

POSITIVE_EN = {
    'love', 'amazing', 'exceeded', 'expectations', 'wonderful', 'recommend',
    'excellent', 'great', 'fantastic', 'perfect', 'best', 'happy', 'satisfied',
    'pleased', 'enjoy', 'adore', 'fascinating', 'spectacular', 'magnificent',
    'brilliant', 'awesome', 'outstanding', 'superb', 'delightful'
}

NEGATIVE_EN = {
    'terrible', 'slow', 'rude', 'cold', 'tasteless', "didn't like", 'bad', 'horrible',
    'awful', 'disappointing', 'frustrated', 'angry', 'annoyed', 'unsatisfied',
    'ugly', 'hate', 'boring', 'useless', 'trash', 'worst', 'poor', 'unacceptable'
}

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

def analyze_text(text, pos_words, neg_words):
    text_lower = text.lower()
    pos_count = sum(1 for w in pos_words if w in text_lower)
    neg_count = sum(1 for w in neg_words if w in text_lower)

    if pos_count > neg_count:
        return "positivo", pos_count / max(pos_count + neg_count, 1)
    elif neg_count > pos_count:
        return "negativo", neg_count / max(pos_count + neg_count, 1)
    return "neutro", 0.5

def extract_entities(text):
    entities = []
    stopwords = {'el', 'la', 'los', 'las', 'un', 'una', 'es', 'muy', 'ni', 'qué', 'tan', 'totalmente', 'hoy', 'está', 'estaba', 'fue', 'era', 'servicio', 'producto', 'comida', 'película', 'clima', 'personal', 'the', 'and', 'was', 'very', 'it', 'what', 'a', 'i', 'to', 'my', 'today', 'is', 'neither', 'nor', 'totally', 'this', 'that', 'with', 'for', 'from', 'have', 'has', 'had', 'were', 'are', 'been', 'being', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall', 'do', 'does', 'did', 'done', 'say', 'said', 'says', 'see', 'saw', 'seen', 'know', 'knew', 'known', 'think', 'thought', 'thinking', 'take', 'took', 'taken', 'give', 'gave', 'given', 'get', 'got', 'gotten', 'make', 'made', 'making', 'go', 'went', 'gone', 'come', 'came', 'come', 'want', 'wanted', 'wanting', 'use', 'used', 'using', 'find', 'found', 'finding', 'tell', 'told', 'telling', 'ask', 'asked', 'asking', 'work', 'worked', 'working', 'seem', 'seemed', 'seeming', 'feel', 'felt', 'feeling', 'try', 'tried', 'trying', 'leave', 'left', 'leaving', 'call', 'called', 'calling'}
    words = re.findall(r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\b', text)
    for word in words:
        if len(word) > 2 and word.lower() not in stopwords:
            entities.append(word)
    words_en = re.findall(r'\b[A-Z][a-z]+\b', text)
    for word in words_en:
        if len(word) > 2 and word.lower() not in stopwords:
            entities.append(word)
    return list(set(entities))

def analyze_sentiment(texts, language, pos_words, neg_words, lang_name):
    print(f"\n{'='*60}")
    print(f"ANÁLISIS LOCAL (REGLAS DE PALABRAS CLAVE) - {lang_name.upper()}")
    print(f"{'='*60}")
    print("ADVERTENCIA: Este script NO usa la API de Gemini.")
    print("Es solo un ejemplo local de análisis por palabras clave.\n")

    for i, text in enumerate(texts, 1):
        sentiment, confidence = analyze_text(text, pos_words, neg_words)
        entities = extract_entities(text)

        print(f"\n--- Texto {i} ---")
        print(f"Texto: {text}")
        print(f"Sentimiento: {sentiment}")
        print(f"Confianza: {confidence:.0%}")
        print(f"Entidades: {entities if entities else 'Ninguna detectada'}")

analyze_sentiment(texts_spanish, "español", POSITIVE_ES, NEGATIVE_ES, "español")
analyze_sentiment(texts_english, "inglés", POSITIVE_EN, NEGATIVE_EN, "inglés")

print(f"\n{'='*60}")
print("NOTA IMPORTANTE")
print(f"{'='*60}")
print("Para usar la API real de Gemini, ejecuta:")
print("  py gemini_sentiment.py")
print("(Requiere variable de entorno GEMINI_API_KEY configurada)")