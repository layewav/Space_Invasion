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
        
        # ESTADO DE PAUSA
        self.is_paused = False
        
        # CARGA DE NAVE
        try:
            # Se intenta cargar nave.jpg (asegúrate de que la extensión sea correcta)
            self.player_img = pygame.image.load("assets/nave.jpg").convert_alpha()
            self.player_img = pygame.transform.scale(self.player_img, (50, 50))
            self.player_rect = self.player_img.get_rect()
        except:
            print("No se encontró assets/nave.jpg, usando cuadro temporal")
            self.player_img = None
            self.player_rect = pygame.Rect(0, 0, 50, 50)

        # Posición inicial de la nave
        self.player_rect.centerx = SCREEN_WIDTH // 2
        self.player_rect.bottom = SCREEN_HEIGHT - 20
        self.speed = 450 

        # SISTEMA DE DISPAROS
        self.bullets = []
        self.bullet_speed = 600

    def go_menu(self):
        from states.menu_state import MenuState
        self.game.change_state(MenuState(self.game))

    def shoot(self):
        """Crea un proyectil que sale de la nave"""
        new_bullet = pygame.Rect(self.player_rect.centerx - 2, self.player_rect.top, 5, 10)
        self.bullets.append(new_bullet)

    def handle_events(self, events):
        for event in events:
            self.back_button.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.is_paused = not self.is_paused
                
                # Disparar con ESPACIO (solo si no está pausado)
                if event.key == pygame.K_SPACE and not self.is_paused:
                    self.shoot()

    def update(self, dt):
        # Si el juego está pausado, no actualizamos nada
        if self.is_paused:
            return

        # Actualizar cronómetro
        if self.time_left > 0:
            self.time_left -= dt
            if self.time_left < 0:
                self.time_left = 0

        # LÓGICA DE MOVIMIENTO NAVE
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_rect.x -= self.speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_rect.x += self.speed * dt

        # Limitar bordes de la pantalla
        if self.player_rect.left < 0:
            self.player_rect.left = 0
        if self.player_rect.right > SCREEN_WIDTH:
            self.player_rect.right = SCREEN_WIDTH

        # ACTUALIZAR BALAS
        for bullet in self.bullets[:]: 
            bullet.y -= self.bullet_speed * dt
            # Eliminar bala si sale de la pantalla (ahora correctamente dentro del bucle)
            if bullet.bottom < 0:
                self.bullets.remove(bullet)

    def draw(self, screen):
        # Dibujar info del juego (Texto)
        mode_text = self.text_font.render(f"Modo: {self.game.data['mode']}", True, WHITE)
        difficulty_text = self.text_font.render(f"Dificultad: {self.game.data['difficulty']}", True, WHITE)
        level_text = self.text_font.render(f"Nivel: {self.game.data['level']}", True, WHITE)

        screen.blit(mode_text, (40, 10))
        screen.blit(difficulty_text, (40, 40))
        screen.blit(level_text, (40, 70))
        # Dibujar cronómetro
        timer_text = self.text_font.render(f"Tiempo: {int(self.time_left)}s", True, YELLOW)
        screen.blit(timer_text, (SCREEN_WIDTH - 200, 10))
        # Dibujar puntuación
        score_text = self.text_font.render(f"Puntuación: {self.score}", True, GREEN)
        screen.blit(score_text, (SCREEN_WIDTH - 200, 40))
        # Dibujar botón de volver al menú
        self.back_button.draw(screen)
        # Dibujar estado de pausa
        if self.is_paused:
            pause_text = self.title_font.render("PAUSA", True, LIGHT_BLUE)
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(pause_text, pause_rect)
        # Dibujar balas
        for bullet in self.bullets:
            pygame.draw.rect(screen, WHITE, bullet)
        # Dibujar la nave (si la imagen cargó)
        if self.player_img:
            screen.blit(self.player_img, self.player_rect)
        else:
            # Si no se cargó la imagen, dibujar un rectángulo temporal
            pygame.draw.rect(screen, WHITE, self.player_rect)
        