# states/play_state.py

import pygame
from core.state import State
from core.button import Button
from settings import WHITE, YELLOW, GREEN, SCREEN_WIDTH, SCREEN_HEIGHT, LIGHT_BLUE


class PlayState(State):
    def __init__(self, game):
        super().__init__(game)

        self.title_font = pygame.font.SysFont("arial", 40, bold=True)
        self.text_font = pygame.font.SysFont("arial", 28)

        self.back_button = Button((20, 20, 180, 50), "Volver al menú", self.text_font, self.go_menu)

        self.time_left = 120.0
        self.score = 0
        self.game = game
        
        # CARGA DE NAVE
        try:
            self.player_img = pygame.image.load("assets/nave.jpg").convert_alpha()
            self.player_img = pygame.transform.scale(self.player_img, (50, 50))
            self.player_rect = self.player_img.get_rect()
        except:
            print("No se encontró assets/nave.jpg, usando cuadro temporal")
            self.player_img = None
            self.player_rect = pygame.Rect(0, 0, 50, 50)

        #Posición inicial de la nave
        self.player_rect.centerx = SCREEN_WIDTH // 2
        self.player_rect.bottom = SCREEN_HEIGHT - 20
        self.speed = 450 

        #

    def go_menu(self):
        from states.menu_state import MenuState
        self.game.change_state(MenuState(self.game))

    def handle_events(self, events):
        for event in events:
            self.back_button.handle_event(event)

    def update(self, dt):
        # Actualizar cronómetro
        if self.time_left > 0:
            self.time_left -= dt
            if self.time_left < 0:
                self.time_left = 0

        # LÓGICA DE MOVIMIENTO ---
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_rect.x -= self.speed * dt
            
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_rect.x += self.speed * dt

        # Limitar bordes
        if self.player_rect.left < 0:
            self.player_rect.left = 0
        if self.player_rect.right > SCREEN_WIDTH:
            self.player_rect.right = SCREEN_WIDTH

    def draw(self, screen):
        # Dibujar info del juego (Texto)
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

        #DIBUJAR LA NAVE ---
        if self.player_img:
            screen.blit(self.player_img, self.player_rect)
        else:
            # Cuadro azul de respaldo si falla la imagen
            pygame.draw.rect(screen, LIGHT_BLUE, self.player_rect)

        self.back_button.draw(screen)