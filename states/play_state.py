

# states/play_state.py

import pygame
from core.state import State
from core.button import Button
from settings import WHITE, YELLOW, GREEN


class PlayState(State):
    """
    Este estado representa la base del juego

    Todavia no tiene enemigos, disparos ni sistema de oleadas
    Pero ya sirve como base para que luego agreguen:
    1. nave del jugador
    2. enemigos
    3. balas
    4. colisiones
    5. vidas
    6. puntaje
    7. power-ups
    8. sonidos
    """

    def __init__(self, game):
        super().__init__(game)

        self.title_font = pygame.font.SysFont("arial", 40, bold=True)
        self.text_font = pygame.font.SysFont("arial", 28)

        self.back_button = Button((20, 20, 180, 50), "Volver al menú", self.text_font, self.go_menu)

        self.time_left = 120.0
        self.score = 0

    def go_menu(self):
        """
        Regresa al menu principal
        """
        from states.menu_state import MenuState
        self.game.change_state(MenuState(self.game))

    def handle_events(self, events):
        for event in events:
            self.back_button.handle_event(event)

    def update(self, dt):
        if self.time_left > 0:
            self.time_left -= dt
            if self.time_left < 0:
                self.time_left = 0

    def draw(self, screen):
        mode_text = self.text_font.render(f"Modo: {self.game.data['mode']}", True, WHITE)
        difficulty_text = self.text_font.render(f"Dificultad: {self.game.data['difficulty']}", True, WHITE)
        level_text = self.text_font.render(f"Nivel: {self.game.data['level']}", True, WHITE)

        screen.blit(mode_text, (40, 100))
        screen.blit(difficulty_text, (40, 140))
        screen.blit(level_text, (40, 180))

        timer_text = self.title_font.render(f"Tiempo: {int(self.time_left)}", True, YELLOW)
        screen.blit(timer_text, (700, 40))

        score_text = self.title_font.render(f"Puntaje: {self.score}", True, GREEN)
        screen.blit(score_text, (40, 240))

        placeholder_lines = [
            "AQUI VA LA BASE DEL NIVEL",
            "Despues aqui pueden agregar:",
            "1. nave del jugador",
            "2. enemigos",
            "3. disparos",
            "4. colisiones",
            "5. oleadas",
            "6. sonidos",
            "7. skins",
            "8. mapa personalizable",
        ]

        y = 320
        for line in placeholder_lines:
            text = self.text_font.render(line, True, WHITE)
            screen.blit(text, (40, y))
            y += 35

        self.back_button.draw(screen)