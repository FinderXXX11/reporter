import requests
import json
import os
import sys
import time

CACHE_FILE = "translation_cache.json"

# Lista endpointów LibreTranslate do przetestowania w kolejności
ENDPOINTS = [
    "https://translate.argosopentech.com/translate",
    "https://libretranslate.de/translate",
    "https://libretranslate.com/translate"
]

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

def try_translate_with_endpoint(text, url):
    payload = {
        "q": text,
        "source": "ru",
        "target": "pl",
        "format": "text"
    }
    for attempt in range(3):
        try:
            response = requests.post(url, data=payload, timeout=10)
            if response.status_code == 200 and response.text.strip().startswith("{"):
                return response.json().get("translatedText", "")
            else:
                time.sleep(1)
        except Exception:
            time.sleep(2)
    return None

def translate_to_polish(text):
    if text in cache:
        return cache[text]

    translated = "[BŁĄD TŁUMACZENIA]"

    for endpoint in ENDPOINTS:
        result = try_translate_with_endpoint(text, endpoint)
        if result:
            translated = result
            break

    cache[text] = translated
    save_cache()
    return translated

# Uruchomienie: python translate_titles.py clear
if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "clear":
    clear_cache()