
# states__menu_state.py 

import pygame
from core.state import State
from core.button import Button
from settings import WHITE, YELLOW, SCREEN_WIDTH


class MenuState(State):
    """
    menu principal del juego 
    desde aqui el jugador podra 
    1. iniciar 
    2. ver los credios 
    3. salirse
    """
    def __init__(self, game):
        super().__init__(game)

        #fuentes 
        self.title_font = pygame.font.SysFont("arial", 60, bold=True)
        self.text_font = pygame.font.SysFont("arial", 30)

        #crear botones
        self.buttons = [Button((400, 250, 200, 60), "Jugar", self.text_font, self.start_game), Button((400, 340, 200, 60), "Créditos", self.text_font, self.show_credits), Button((400, 430, 200, 60), "Salir", self.text_font, self.exit_game)]

        #texto de creditos temporal 
        self.showing_credits = False 

    

    def __init__(self, game):
        super().__init__(game)

        # fuentes
        self.title_font = pygame.font.SysFont("arial", 60, bold=True)
        self.text_font = pygame.font.SysFont("arial", 30)

        # crear botones
        self.buttons = [
            Button((400, 250, 200, 60), "Jugar", self.text_font, self.start_game),
            Button((400, 340, 200, 60), "Créditos", self.text_font, self.show_credits),
            Button((400, 430, 200, 60), "Salir", self.text_font, self.exit_game),
        ]

        # texto de creditos temporal
        self.showing_credits = False

    def start_game(self):
        """
        cambia al estado de seleccion de modo
        """
        from states.mode_state import ModeState
        self.game.change_state(ModeState(self.game))

    def show_credits(self):
        """
        Activa o desactiva los creditos
        """
        self.showing_credits = not self.showing_credits

    def exit_game(self):
        """
        Cierra el juego
        """
        self.game.quit()

    def handle_events(self, events):
        for event in events:
            for button in self.buttons:
                button.handle_event(event)

    def update(self, dt):
        pass

    def draw(self, screen):
        # Título principal
        title_surface = self.title_font.render("SPACE INVASION", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 120))
        screen.blit(title_surface, title_rect)

        subtitle_surface = self.text_font.render("Base del proyecto", True, YELLOW)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 170))
        screen.blit(subtitle_surface, subtitle_rect)

        # Dibujar botones
        for button in self.buttons:
            button.draw(screen)

        # Creditos temporales
        if self.showing_credits:
            credits = [
                "Proyecto hecho por:",
                "Garcia Guzman Victor Manuel",
                "Aqui van ustedes xD",
            ]

            y = 530
            for line in credits:
                text = self.text_font.render(line, True, WHITE)
                rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
                screen.blit(text, rect)
                y += 35
   



