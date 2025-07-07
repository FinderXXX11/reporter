@echo off
echo Instalacja modelu Argos Translate: rosyjski -> polski

REM Krok 1: Instalacja biblioteki argostranslate
python -m pip install argostranslate

REM Krok 2: Pobranie i instalacja modelu językowego RU->PL
python -m argostranslate.install translate-ru_pl

echo --------------------------------------
echo Gotowe. Możesz teraz uruchomić main.py
pause