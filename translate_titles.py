import os
import json
import sys

CACHE_FILE = "translation_cache.json"

try:
    import argostranslate.package, argostranslate.translate
    argostranslate_installed = True
except ImportError:
    argostranslate_installed = False

# Wczytaj cache
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

    if not argostranslate_installed:
        translated = "[Brak tłumaczenia: brak biblioteki argostranslate]"
    else:
        installed_languages = argostranslate.translate.get_installed_languages()
        try:
            from_lang = next(lang for lang in installed_languages if lang.code == "ru")
            to_lang = next(lang for lang in installed_languages if lang.code == "pl")
            translation = from_lang.get_translation(to_lang)
            translated = translation.translate(text)
        except StopIteration:
            translated = "[Brak tłumaczenia: zainstaluj model RU→PL: `argospm install translate-ru_pl`]"

    cache[text] = translated
    save_cache()
    return translated

if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "clear":
    clear_cache()