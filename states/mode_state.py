

# states__mode_state.py

import pygame
from core.state import State
from core.button import Button
from settings import WHITE, GAME_MODES, SCREEN_WIDTH


class ModeState(State):
    """
    pantalla para elegir el modo de juego
    """

    def __init__(self, game):
        super().__init__(game)

        self.title_font = pygame.font.SysFont("arial", 50, bold=True)
        self.text_font = pygame.font.SysFont("arial", 28)

        self.buttons = []
        y = 220

        for mode in GAME_MODES:
            self.buttons.append(
                Button((350, y, 300, 55), mode, self.text_font, lambda m=mode: self.select_mode(m))
            )
            y += 80

        self.back_button = Button((20, 20, 150, 50), "Regresar", self.text_font, self.go_back)

    def select_mode(self, mode):
        """
        Guarda el modo seleccionado y avanza a dificultad
        """
        from states.difficulty_state import DifficultyState
        self.game.data["mode"] = mode
        self.game.change_state(DifficultyState(self.game))

    def go_back(self):
        """
        Regresa al menu principal
        """
        from states.menu_state import MenuState
        self.game.change_state(MenuState(self.game))

    def handle_events(self, events):
        for event in events:
            for button in self.buttons:
                button.handle_event(event)
            self.back_button.handle_event(event)

    def update(self, dt):
        pass

    def draw(self, screen):
        title = self.title_font.render("Elige el modo", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 120))
        screen.blit(title, title_rect)

        for button in self.buttons:
            button.draw(screen)

        self.back_button.draw(screen)