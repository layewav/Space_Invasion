# states/difficulty_state.py
# Este archivo contiene la pantalla para elegir dificultad.

import pygame
from core.state import State
from core.button import Button
from settings import WHITE, DIFFICULTIES, SCREEN_WIDTH


class DifficultyState(State):
    """
    Pantalla para elegir dificultad.

    Las dificultades vienen desde settings.py:
    - FACIL
    - NORMAL
    - DIFICIL
    """

    def __init__(self, game):
        """
        Prepara la pantalla de dificultad.
        """

        super().__init__(game)

        # Fuente grande para el titulo.
        self.title_font = pygame.font.SysFont("arial", 50, bold=True)

        # Fuente para los botones.
        self.text_font = pygame.font.SysFont("arial", 28)

        # Lista de botones.
        self.buttons = []

        # Posicion vertical inicial del primer boton.
        y = 240

        # Creamos un boton por cada dificultad.
        for difficulty in DIFFICULTIES:
            self.buttons.append(
                Button(
                    (350, y, 300, 55),
                    difficulty,
                    self.text_font,
                    lambda d=difficulty: self.select_difficulty(d)
                )
            )

            # Bajamos el siguiente boton.
            y += 80

        # Boton para regresar a la seleccion de modo.
        self.back_button = Button((20, 20, 150, 50), "Regresar", self.text_font, self.go_back)

    def select_difficulty(self, difficulty):
        """
        Guarda la dificultad elegida
        y pasa a la pantalla de seleccion de nivel.
        """

        from states.level_state import LevelState

        # Guardamos la dificultad para usarla despues en PlayState.
        self.game.data["difficulty"] = difficulty

        # Cambiamos a la pantalla de niveles.
        self.game.change_state(LevelState(self.game))

    def go_back(self):
        """
        Regresa a la seleccion de modo.
        """

        from states.mode_state import ModeState
        self.game.change_state(ModeState(self.game))

    def handle_events(self, events):
        """
        Revisa clics sobre los botones.
        """

        for event in events:
            # Revisamos los botones de dificultad.
            for button in self.buttons:
                button.handle_event(event)

            # Revisamos el boton de regresar.
            self.back_button.handle_event(event)

    def update(self, dt):
        """
        No hay movimiento en esta pantalla.
        """

        pass

    def draw(self, screen):
        """
        Dibuja la pantalla de dificultad.
        """

        # Dibujamos el titulo.
        title = self.title_font.render("Elige la dificultad", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 120))
        screen.blit(title, title_rect)

        # Dibujamos los botones.
        for button in self.buttons:
            button.draw(screen)

        # Dibujamos el boton de regresar.
        self.back_button.draw(screen)