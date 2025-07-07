@echo off
cd /d %~dp0

echo ======================================
echo [1/3] Dodawanie zmian do Git...
git add .

echo [2/3] Tworzenie commita...
git commit -m "Aktualizacja: nowa wersja z filtrowaniem i DuckDuckGo"

echo [3/3] Wypychanie do GitHub...
git push

echo.
echo ✅ Gotowe! Sprawdź repozytorium na GitHubie.
pause