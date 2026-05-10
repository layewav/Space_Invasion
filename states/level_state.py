

# states__level_state.py

import pygame
from core.state import State
from core.button import Button
from settings import WHITE, LEVELS, SCREEN_WIDTH


class LevelState(State):
    """
    Pantalla para elegir nivel
    Por ahora solo es seleccion base, no definitiva
    Los niveles reales todavía no se implementan
    """

    def __init__(self, game):
        super().__init__(game)

        self.title_font = pygame.font.SysFont("arial", 50, bold=True)
        self.text_font = pygame.font.SysFont("arial", 28)

        self.buttons = []
        y = 180

        for level in LEVELS:
            self.buttons.append(
                Button((350, y, 300, 50), level, self.text_font, lambda l=level: self.select_level(l))
            )
            y += 65

        self.back_button = Button((20, 20, 150, 50), "Regresar", self.text_font, self.go_back)

    def select_level(self, level):
        """
        Guarda el nivel seleccionado y entra a la base del juego
        """
        from states.play_state import PlayState
        self.game.data["level"] = level
        self.game.change_state(PlayState(self.game))

    def go_back(self):
        """
        Regresa a la dificultad
        """
        from states.difficulty_state import DifficultyState
        self.game.change_state(DifficultyState(self.game))

    def handle_events(self, events):
        for event in events:
            for button in self.buttons:
                button.handle_event(event)
            self.back_button.handle_event(event)

    def update(self, dt):
        pass

    def draw(self, screen):
        title = self.title_font.render("Elige el nivel", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        for button in self.buttons:
            button.draw(screen)

        self.back_button.draw(screen)