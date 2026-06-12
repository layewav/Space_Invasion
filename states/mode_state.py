# states/mode_state.py
# Este archivo contiene la pantalla para elegir el modo de juego.

import pygame
from core.state import State
from core.button import Button
from settings import WHITE, GAME_MODES, SCREEN_WIDTH


class ModeState(State):
    """
    Pantalla para elegir el modo de juego.

    Los modos vienen desde settings.py:
    - MODO CLASICO
    - SUPERVIVENCIA
    - CONTRARRELOJ
    """

    def __init__(self, game):
        """
        Prepara la pantalla de modos.
        Crea el titulo, la fuente y los botones.
        """

        super().__init__(game)

        # Fuente grande para el titulo.
        self.title_font = pygame.font.SysFont("arial", 50, bold=True)

        # Fuente para los botones.
        self.text_font = pygame.font.SysFont("arial", 28)

        # Lista donde guardaremos los botones de los modos.
        self.buttons = []

        # Posicion vertical inicial del primer boton.
        y = 220

        # Creamos un boton por cada modo que exista en GAME_MODES.
        for mode in GAME_MODES:
            self.buttons.append(
                Button(
                    (350, y, 300, 55),
                    mode,
                    self.text_font,
                    lambda m=mode: self.select_mode(m)
                )
            )

            # Bajamos la posicion para el siguiente boton.
            y += 80

        # Boton para regresar al menu principal.
        self.back_button = Button((20, 20, 150, 50), "Regresar", self.text_font, self.go_back)

    def select_mode(self, mode):
        """
        Guarda el modo que eligio el jugador
        y luego avanza a la pantalla de dificultad.
        """

        from states.difficulty_state import DifficultyState

        # Guardamos el modo en game.data para usarlo despues en PlayState.
        self.game.data["mode"] = mode

        # Cambiamos a la pantalla de dificultad.
        self.game.change_state(DifficultyState(self.game))

    def go_back(self):
        """
        Regresa al menu principal.
        """

        from states.menu_state import MenuState
        self.game.change_state(MenuState(self.game))

    def handle_events(self, events):
        """
        Revisa clics sobre los botones.
        """

        for event in events:
            # Revisamos los botones de modo.
            for button in self.buttons:
                button.handle_event(event)

            # Revisamos el boton de regresar.
            self.back_button.handle_event(event)

    def update(self, dt):
        """
        Esta pantalla no necesita actualizar movimiento.
        """

        pass

    def draw(self, screen):
        """
        Dibuja la pantalla de seleccion de modo.
        """

        # Dibujamos el titulo.
        title = self.title_font.render("Elige el modo", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 120))
        screen.blit(title, title_rect)

        # Dibujamos los botones de modo.
        for button in self.buttons:
            button.draw(screen)

        # Dibujamos el boton para regresar.
        self.back_button.draw(screen)