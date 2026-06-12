# core/state.py
# Este archivo contiene la clase State.
# State significa "estado" o "pantalla".
# En este proyecto, cada pantalla del juego es un estado.
# Ejemplos de estados:
# - Menu principal
# - Seleccion de modo
# - Seleccion de dificultad
# - Seleccion de nivel
# - Pantalla de juego


class State:
    """
    Clase base para todas las pantallas del juego.

    Esta clase sirve como molde.
    Las demas pantallas heredan de esta clase para tener
    la misma estructura.
    """

    def __init__(self, game):
        """
        Guarda una referencia al juego principal.

        game es el objeto principal del juego.
        Desde aqui podemos cambiar de pantalla, cerrar el juego
        o consultar datos guardados como modo, dificultad y nivel.
        """

        self.game = game

    def handle_events(self, events):
        """
        Procesa eventos del usuario.

        Un evento puede ser:
        - Presionar una tecla.
        - Hacer clic con el mouse.
        - Mover el mouse.
        - Cerrar la ventana.

        Este metodo se deja vacio aqui porque cada pantalla
        decide que hacer con sus propios eventos.
        """

        pass

    def update(self, dt):
        """
        Actualiza la logica del estado.

        dt significa "delta time".
        Es el tiempo que paso entre un frame y otro.

        Sirve para que movimientos como enemigos, balas o estrellas
        no dependan directamente de la velocidad de la computadora.
        """

        pass

    def draw(self, screen):
        """
        Dibuja el estado en pantalla.

        screen es la ventana donde se dibujan textos, botones,
        imagenes, enemigos, balas y otros elementos.

        Este metodo se deja vacio aqui porque cada pantalla
        dibuja cosas diferentes.
        """

        pass