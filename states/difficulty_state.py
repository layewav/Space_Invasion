
# states__difficulty_state.py

import pygame
from core.state import State
from core.button import Button
from settings import WHITE, DIFFICULTIES, SCREEN_WIDTH


class DifficultyState(State):
    """
    Pantalla para elegir dificultad
    """

    def __init__(self, game):
        super().__init__(game)

        self.title_font = pygame.font.SysFont("arial", 50, bold=True)
        self.text_font = pygame.font.SysFont("arial", 28)

        self.buttons = []
        y = 240

        for difficulty in DIFFICULTIES:
            self.buttons.append(
                Button(
                    (350, y, 300, 55),
                    difficulty,
                    self.text_font,
                    lambda d=difficulty: self.select_difficulty(d)
                )
            )
            y += 80

        self.back_button = Button((20, 20, 150, 50), "Regresar", self.text_font, self.go_back)

    def select_difficulty(self, difficulty):
        """
        guarda la dificultad elegida y pasa a seleccion de nivel
        """
        from states.level_state import LevelState
        self.game.data["difficulty"] = difficulty
        self.game.change_state(LevelState(self.game))

    def go_back(self):
        """
        Regresa a la seleccion de modo
        """
        from states.mode_state import ModeState
        self.game.change_state(ModeState(self.game))

    def handle_events(self, events):
        for event in events:
            for button in self.buttons:
                button.handle_event(event)
            self.back_button.handle_event(event)

    def update(self, dt):
        pass

    def draw(self, screen):
        title = self.title_font.render("Elige la dificultad", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 120))
        screen.blit(title, title_rect)

        for button in self.buttons:
            button.draw(screen)

        self.back_button.draw(screen)