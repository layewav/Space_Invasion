# archivo settings.py
# Este archivo guarda configuraciones generales del juego.
# La idea de este archivo es tener valores importantes en un solo lugar.
# Asi, si queremos cambiar el tamaño de pantalla, colores, FPS, modos,
# dificultades o niveles, no tenemos que buscar por todo el codigo.


# CONFIGURACION DE PANTALLA

# Ancho de la ventana del juego.
SCREEN_WIDTH = 1000

# Alto de la ventana del juego.
SCREEN_HEIGHT = 700

# Titulo que aparece arriba en la ventana.
GAME_TITLE = "SPACE INVASION"

# FPS o los "frames por segundo".
# Mientras mas alto, mas fluido puede verse el juego.
# 60 FPS es un valor normal para juegos sencillos.
FPS = 60



# COLORES DEL JUEGO
# Los colores estan en formato RGB.
# RGB significa:
# R = rojo
# G = verde
# B = azul
#
# Cada numero va de 0 a 255.
# Ejemplo:
# (255, 255, 255) es blanco.
# (0, 0, 0) es negro.

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Color principal del fondo del juego.
DARK_BLUE = (10, 20, 40)

# Color de respaldo para la nave si no carga la imagen.
LIGHT_BLUE = (80, 180, 255)

# Colores usados para enemigos, vidas, textos y balas.
RED = (220, 70, 70)
GREEN = (70, 220, 120)
YELLOW = (255, 220, 70)
GRAY = (180, 180, 180)
DARK_GRAY = (70, 70, 70)



# MODOS DE JUEGO
# Estos textos aparecen en la pantalla de seleccion de modo.
# Tambien se usan en play_state.py para cambiar las reglas del juego.

GAME_MODES = [
    "MODO CLASICO",    # Sobrevivir hasta que termine el tiempo.
    "SUPERVIVENCIA",   # Jugar sin limite de tiempo hasta perder.
    "CONTRARRELOJ"     # Conseguir puntos antes de que acabe el tiempo.
]



# DIFICULTADES
# Estas opciones cambian cosas como vidas, velocidad de enemigos
# y frecuencia de disparos enemigos.

DIFFICULTIES = [
    "FACIL",
    "NORMAL",
    "DIFICIL"
]



# NIVELES
# Lista de niveles disponibles.
# En el juego se pueden bloquear o desbloquear segun el progreso.

LEVELS = [
    "Nivel 1",
    "Nivel 2",
    "Nivel 3",
    "Nivel 4",
    "Nivel 5",
    "Nivel 6",
    "Nivel 7"
]