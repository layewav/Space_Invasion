@echo off

REM Este archivo sirve para iniciar el juego mas facil.
REM El profesor o cualquier persona solo debe dar doble clic aqui.

title SPACE INVASION

echo ================================
echo          SPACE INVASION
echo ================================
echo.

REM Entramos a la carpeta donde esta este archivo .bat.
REM Esto es importante porque asi el juego encuentra main.py,
REM assets, states, core y todos los archivos aunque la carpeta
REM este en Descargas, Escritorio u otra ubicacion.
cd /d "%~dp0"

echo Revisando librerias necesarias...
echo.

REM Instalamos las librerias que aparecen en requirements.txt.
REM En este proyecto principalmente se necesita pygame.
py -m pip install -r requirements.txt

echo.
echo Iniciando el juego...
echo.

REM Ejecutamos el archivo principal del juego.
py main.py

echo.
echo El juego se cerro.
echo.

REM Pausamos la terminal para que, si hubo un error,
REM la ventana no se cierre inmediatamente y podamos leerlo.
pause