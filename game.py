# archivo game.py
# Este archivo contiene la clase principal del juego.
# Aqui se crea la ventana, se controlan los FPS
# y se cambia entre pantallas del juego.

import pygame

# Importamos configuraciones generales desde settings.py.
# Asi no tenemos numeros sueltos por todo el codigo.
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, FPS, DARK_BLUE

# Importamos el menu principal.
# Este sera el primer estado/pantalla que vera el jugador.
from states.menu_state import MenuState


class Game:
    """
    Clase principal del juego.

    Esta clase se encarga de:
    1. Iniciar pygame.
    2. Crear la ventana.
    3. Controlar el tiempo/FPS.
    4. Guardar datos importantes del juego.
    5. Cambiar entre pantallas.
    6. Mantener el juego corriendo.
    """

    def __init__(self):
        """
        Constructor de la clase Game.
        Se ejecuta automaticamente cuando hacemos:

        game = Game()
        """

        # Iniciamos pygame.
        # Esto es obligatorio antes de usar pantalla, eventos, fuentes, imagenes, etc.
        pygame.init()

        # Creamos la ventana principal del juego.
        # SCREEN_WIDTH y SCREEN_HEIGHT vienen de settings.py.
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Ponemos el titulo que aparece arriba en la ventana.
        pygame.display.set_caption(GAME_TITLE)

        # Creamos un reloj.
        # Esto sirve para controlar los FPS y que el juego no vaya demasiado rapido.
        self.clock = pygame.time.Clock()

        # Esta variable indica si el juego sigue abierto.
        # Si cambia a False, el juego se cierra.
        self.running = True

        # Diccionario con datos globales del juego.
        # Aqui guardamos lo que el jugador va eligiendo en los menus.
        self.data = {
            # Modo elegido:
            # MODO CLASICO, SUPERVIVENCIA o CONTRARRELOJ.
            "mode": None,

            # Dificultad elegida:
            # FACIL, NORMAL o DIFICIL.
            "difficulty": None,

            # Nivel elegido:
            # Nivel 1, Nivel 2, etc.
            "level": None,

            # Nivel maximo desbloqueado.
            # Empieza en 1 porque el Nivel 1 siempre debe estar disponible.
            "unlocked_level": 1,

            # Esto sirve para pruebas.
            # Si es True, todos los niveles aparecen desbloqueados.
            "all_levels_unlocked": False
        }

        # Pantalla inicial del juego.
        # Cuando el juego abre, primero muestra el menu principal.
        self.current_state = MenuState(self)

    def change_state(self, new_state):
        """
        Cambia de una pantalla a otra.

        Ejemplos:
        menu -> seleccion de modo
        modo -> seleccion de dificultad
        dificultad -> seleccion de nivel
        nivel -> juego
        """

        # Guardamos el nuevo estado como estado actual.
        # Desde este momento, el juego actualiza y dibuja esa nueva pantalla.
        self.current_state = new_state

    def quit(self):
        """
        Cierra el juego.
        """

        # Cuando running se vuelve False, el bucle principal termina.
        self.running = False

    def run(self):
        """
        Bucle principal del juego.

        Este while se repite muchas veces por segundo.
        En cada vuelta hace:
        1. Controlar FPS.
        2. Leer eventos.
        3. Actualizar la pantalla actual.
        4. Dibujar la pantalla actual.
        5. Actualizar la ventana.
        """

        while self.running:
            # Controlamos los FPS.
            # FPS viene de settings.py.
            # dt significa "delta time".
            # Sirve para que el movimiento sea mas estable.
            dt = self.clock.tick(FPS) / 1000.0

            # Obtenemos todos los eventos del momento.
            # Ejemplos:
            # cerrar ventana, presionar teclas, mover mouse, hacer clic, etc.
            events = pygame.event.get()

            # Revisamos si el jugador cerro la ventana.
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit()

            # Mandamos los eventos a la pantalla actual.
            # Por ejemplo, si estamos en el menu, el menu revisa los clics.
            self.current_state.handle_events(events)

            # Actualizamos la logica de la pantalla actual.
            # Por ejemplo, movimiento, enemigos, tiempo, balas, etc.
            self.current_state.update(dt)

            # Pintamos el fondo base.
            self.screen.fill(DARK_BLUE)

            # Dibujamos la pantalla actual encima del fondo.
            self.current_state.draw(self.screen)

            # Actualizamos la ventana para que se vea lo que dibujamos.
            pygame.display.flip()

        # Cuando el bucle termina, cerramos pygame correctamente.
        pygame.quit()