@echo off
echo Instalacja modelu Argos Translate: rosyjski -> polski

REM Krok 1: Instalacja biblioteki argostranslate
pip install argostranslate

REM Krok 2: Pobranie i instalacja modelu językowego RU->PL
argospm install translate-ru_pl

pause