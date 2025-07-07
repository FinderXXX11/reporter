import requests
import json
import os
import sys

CACHE_FILE = "translation_cache.json"
ENDPOINT = "https://translate.argosopentech.com/translate"

# Wczytaj cache jeśli istnieje
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)
else:
    cache = {}

def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def clear_cache():
    global cache
    cache = {}
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
    print("🧹 Cache tłumaczeń został wyczyszczony.")

def translate_to_polish(text):
    if text in cache:
        return cache[text]

    payload = {
        "q": text,
        "source": "ru",
        "target": "pl",
        "format": "text"
    }

    try:
        response = requests.post(ENDPOINT, data=payload, timeout=10)
        if response.status_code == 200 and response.text.strip().startswith("{"):
            translated = response.json().get("translatedText", "")
        else:
            translated = "[BŁĄD TŁUMACZENIA]"
    except Exception as e:
        translated = f"[BŁĄD: {e}]"

    cache[text] = translated
    save_cache()
    return translated

if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "clear":
    clear_cache()