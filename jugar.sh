#!/bin/bash
echo "Preparando el entorno de Space Invasion..."

# Revisa si la carpeta .venv NO existe para crear una nueva
if [ ! -d ".venv" ]; then
    echo "Creando entorno virtual nuevo para Linux/Mac..."
    python3 -m venv .venv
fi

echo "Activando entorno virtual..."
source .venv/bin/activate

echo "Instalando dependencias necesarias..."
pip install -r requirements.txt

echo "Arrancando el juego..."
python3 main.py