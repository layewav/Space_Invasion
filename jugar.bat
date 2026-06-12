@echo off
echo Preparando el entorno de Space Invasion...

if not exist .venv (
    echo Creando entorno virtual nuevo...
    python -m venv .venv
)

echo Activando entorno virtual...
call .venv\Scripts\activate

echo Instalando dependencias necesarias...
call pip install -r requirements.txt

echo Arrancando el juego...
python main.py

pause