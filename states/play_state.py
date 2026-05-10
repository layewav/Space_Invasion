# states/play_state.py
import pygame
import random
from core.state import State
from core.button import Button
from settings import WHITE, YELLOW, GREEN, RED, SCREEN_WIDTH, SCREEN_HEIGHT, LIGHT_BLUE

class Enemy:
    def __init__(self, x, y, speed, shoot_delay):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = speed
        self.shoot_delay = shoot_delay
        self.last_shot = pygame.time.get_ticks()

    def update(self, dt):
        self.rect.y += self.speed * dt

    def can_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            return True
        return False

class PlayState(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.is_paused = False
        
        # Fuentes y UI
        self.title_font = pygame.font.SysFont("arial", 40, bold=True)
        self.text_font = pygame.font.SysFont("arial", 28)
        self.back_button = Button((20, 20, 180, 50), "Volver al menú", self.text_font, self.go_menu)

        # Variables de juego [cite: 3]
        self.time_left = 120.0
        self.score = 0
        self.level = int(self.game.data['level'].split()[-1]) # Extrae el número del nivel [cite: 3]
        
        # Nave Jugador
        try:
            self.player_img = pygame.image.load("assets/nave.jpg").convert_alpha()
            self.player_img = pygame.transform.scale(self.player_img, (50, 50))
            self.player_rect = self.player_img.get_rect()
        except:
            self.player_img = None
            self.player_rect = pygame.Rect(0, 0, 50, 50)
        
        self.player_rect.centerx = SCREEN_WIDTH // 2
        self.player_rect.bottom = SCREEN_HEIGHT - 20
        self.speed = 450 

        # Balas y Enemigos 
        self.bullets = []         # Balas del jugador
        self.enemy_bullets = []   # Balas de enemigos
        self.enemies = []
        self.bullet_speed = 600
        
        # Lógica de aparición (Spawn)
        self.spawn_timer = 0
        # La dificultad escala con el nivel: más nivel = spawn más rápido 
        self.spawn_rate = max(0.5, 2.0 - (self.level * 0.2)) 

    def go_menu(self):
        from states.menu_state import MenuState
        self.game.change_state(MenuState(self.game))

    def shoot(self):
        new_bullet = pygame.Rect(self.player_rect.centerx - 2, self.player_rect.top, 5, 10)
        self.bullets.append(new_bullet)

    def enemy_shoot(self, enemy):
        new_bullet = pygame.Rect(enemy.rect.centerx - 2, enemy.rect.bottom, 5, 10)
        self.enemy_bullets.append(new_bullet)

    def handle_events(self, events):
        for event in events:
            self.back_button.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.is_paused = not self.is_paused
                if event.key == pygame.K_SPACE and not self.is_paused:
                    self.shoot()

    def update(self, dt):
        if self.is_paused: return

        if self.time_left > 0:
            self.time_left -= dt

        # Movimiento Jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_rect.x -= self.speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_rect.x += self.speed * dt
        self.player_rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Generar Enemigos poco a poco
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_rate:
            enemy_speed = 100 + (self.level * 20) # Dificultad: más velocidad por nivel
            shoot_delay = max(1000, 3000 - (self.level * 300)) # Disparan más rápido
            new_enemy = Enemy(random.randint(0, SCREEN_WIDTH - 40), -40, enemy_speed, shoot_delay)
            self.enemies.append(new_enemy)
            self.spawn_timer = 0

        # Actualizar Enemigos y sus disparos 
        for e in self.enemies[:]:
            e.update(dt)
            if e.can_shoot():
                self.enemy_shoot(e)
            if e.rect.top > SCREEN_HEIGHT:
                self.enemies.remove(e)

        # Actualizar Balas Jugador y Colisiones 
        for b in self.bullets[:]:
            b.y -= self.bullet_speed * dt
            if b.bottom < 0: self.bullets.remove(b)
            
            for e in self.enemies[:]:
                if b.colliderect(e.rect):
                    if b in self.bullets: self.bullets.remove(b)
                    self.enemies.remove(e)
                    self.score += 10 # Sumar puntaje 

        # Actualizar Balas Enemigas
        for eb in self.enemy_bullets[:]:
            eb.y += (self.bullet_speed // 2) * dt
            if eb.top > SCREEN_HEIGHT: self.enemy_bullets.remove(eb)
            
            if eb.colliderect(self.player_rect):
                print("¡Jugador golpeado!") # Aquí iría la lógica de vidas 
                self.enemy_bullets.remove(eb)

    def draw(self, screen):
        # Dibujar Balas Jugador
        for bullet in self.bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        # Dibujar Balas Enemigas
        for e_bullet in self.enemy_bullets:
            pygame.draw.rect(screen, RED, e_bullet)

        # Dibujar Enemigos
        for e in self.enemies:
            pygame.draw.rect(screen, RED, e.rect) 

        # Dibujar Nave
        if self.player_img:
            screen.blit(self.player_img, self.player_rect)
        else:
            pygame.draw.rect(screen, LIGHT_BLUE, self.player_rect)

        # UI [cite: 3]
        timer_text = self.title_font.render(f"Tiempo: {int(self.time_left)}", True, YELLOW)
        screen.blit(timer_text, (SCREEN_WIDTH - 200, 40))
        
        score_text = self.text_font.render(f"Puntaje: {self.score}", True, GREEN)
        screen.blit(score_text, (40, 80))

        level_display = self.text_font.render(f"Nivel: {self.level}", True, WHITE)
        screen.blit(level_display, (40, 120))

        if self.is_paused:
            p_text = self.title_font.render("PAUSA (P)", True, WHITE)
            screen.blit(p_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2))

        self.back_button.draw(screen)