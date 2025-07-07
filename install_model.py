import subprocess
import sys

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def install_translation_model():
    subprocess.check_call([sys.executable, "-m", "argostranslate.install", "translate-ru_pl"])

if __name__ == "__main__":
    print("📦 Instalacja biblioteki argostranslate...")
    install_package("argostranslate")
    print("📥 Pobieranie modelu tłumaczeń RU -> PL...")
    install_translation_model()
    print("✅ Gotowe. Możesz teraz uruchomić main.py")