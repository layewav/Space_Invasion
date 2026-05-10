
# core/state.py 

class State:
    """
    clase base para todos los estados del juego

    Un estado puede ser:
    1. Menu principal
    2. Sellecion de dificultad 
    3. selecion de nivel 
    4. pantalla de juego 
    5. pausa
    6. game over 
    etc

    todas las pantallas del juego deberian heredar de esta clase 

    """
    def __init__(self, game):
        self.game = game 

    def handle_events(self, events):
        """
        PROCESA EVENTOS DEL TECLADO, MAUSE, ETC
        """
        pass

    def update(self, dt):
        """
        actualiza la logica del estado 
        dt = delta time (tiempo entre frames) 
        """
        pass 

    def draw(self, screen):
        """
        dibuja el estado en pantalla
        """
        pass