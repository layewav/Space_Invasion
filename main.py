# ESTE ES EL ARCHIVO main.py
# Este archivo es el punto de entrada del juego.
# Significa que este es el primer archivo que se ejecuta cuando abrimos el juego.

# Importamos la clase Game desde el archivo game.py.
# La clase Game es la que controla casi todo el juego:
# ventana, estados, FPS, eventos, etc.
from game import Game


def main():
    """
    Esta funcion inicia el juego.

    No ponemos toda la logica aqui porque este archivo debe ser simple.
    Su unico trabajo es:
    1. Crear el objeto principal del juego.
    2. Ejecutar el juego.
    """

    # Creamos el objeto principal del juego.
    # Al hacer esto, se inicia pygame, se crea la ventana
    # y se carga el menu principal.
    game = Game()

    # Ejecutamos el bucle principal del juego.
    # El juego se queda funcionando aqui hasta que el jugador lo cierre.
    game.run()


# Esta condicion sirve para que el juego solo arranque
# si ejecutamos directamente este archivo.
# Por ejemplo:
# py main.py
# Si otro archivo importa main.py, no se ejecuta automaticamente.
if __name__ == "__main__":
    main()