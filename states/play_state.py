# states/play_state.py
# Este archivo contiene la pantalla donde realmente se juega.
# Aqui esta la nave, enemigos, disparos, vidas, tiempo, modos y victoria/derrota.

import pygame
import random
import os

from core.state import State
from core.button import Button

from settings import (
    WHITE,
    YELLOW,
    GREEN,
    RED,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    LIGHT_BLUE,
    LEVELS
)


class Enemy:
    """
    Esta clase representa a un enemigo.

    Cada enemigo tiene:
    - Un rectangulo para posicion y colisiones.
    - Velocidad de movimiento.
    - Tiempo entre disparos.
    """

    def __init__(self, x, y, speed, shoot_delay):
        """
        Crea un enemigo.

        x: posicion horizontal.
        y: posicion vertical.
        speed: velocidad con la que baja.
        shoot_delay: tiempo que espera antes de disparar otra vez.
        """

        # Rectangulo del enemigo.
        # Tambien sirve para detectar choques.
        self.rect = pygame.Rect(x, y, 40, 40)

        # Velocidad con la que baja el enemigo.
        self.speed = speed

        # Tiempo que tarda en volver a disparar.
        self.shoot_delay = shoot_delay

        # Guardamos el momento del ultimo disparo.
        self.last_shot = pygame.time.get_ticks()

    def update(self, dt):
        """
        Mueve el enemigo hacia abajo.
        """

        self.rect.y += self.speed * dt

    def can_shoot(self):
        """
        Revisa si el enemigo ya puede disparar otra vez.
        """

        # Tiempo actual en milisegundos.
        now = pygame.time.get_ticks()

        # Si ya paso suficiente tiempo desde el ultimo disparo,
        # el enemigo puede disparar.
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            return True

        return False


class PlayState(State):
    """
    Esta clase es la pantalla de juego.

    Aqui se controla:
    - Movimiento del jugador.
    - Disparos del jugador.
    - Disparos enemigos.
    - Enemigos.
    - Vidas.
    - Puntaje.
    - Tiempo.
    - Pausa.
    - Game Over.
    - Nivel completado.
    - Desbloqueo de niveles.
    - Efectos de Sonido
    """

    def __init__(self, game):
        """
        Prepara todo lo necesario para iniciar el nivel.
        """

        super().__init__(game)
        self.game = game

        # Variables de estado.
        # Sirven para saber si el juego esta pausado, perdido,
        # esperando inicio o completado.
        self.is_paused = False
        self.game_over = False
        self.waiting_start = True
        self.level_complete = False

        # Inicializar el mezclador de Pygame para el audio.
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(32)

        # Fuentes para textos.
        self.title_font = pygame.font.SysFont("arial", 40, bold=True)
        self.text_font = pygame.font.SysFont("arial", 28)

        # Boton para volver al menu.
        self.back_button = Button((40, 20, 200, 50), "Volver al menú", self.text_font, self.go_menu)

        # Puntaje inicial.
        self.score = 0

        # Sacamos el numero del nivel elegido.
        # Ejemplo:
        # "Nivel 3" -> 3
        self.level = int(self.game.data["level"].split()[-1])

        # Guardamos el modo elegido en el menu.
        self.mode = self.game.data["mode"]

        # Dependiendo del modo, cambiamos las reglas del juego.
        if self.mode == "MODO CLASICO":
            # En clasico se gana sobreviviendo 60 segundos.
            self.time_left = 60.0
            self.target_score = 0

        elif self.mode == "SUPERVIVENCIA":
            # En supervivencia no hay tiempo.
            # Se juega hasta perder todas las vidas.
            self.time_left = None
            self.target_score = 0

        elif self.mode == "CONTRARRELOJ":
            # En contrarreloj hay que llegar a cierto puntaje antes de que acabe el tiempo.
            self.time_left = 45.0
            self.target_score = 100 + (self.level * 50)

        # Guardamos la dificultad elegida.
        self.difficulty = self.game.data["difficulty"]

        # La dificultad cambia vidas, velocidad de enemigos,
        # disparos enemigos y aparicion de enemigos.
        if self.difficulty == "FACIL":
            self.lives = 9
            self.enemy_speed_extra = 0
            self.enemy_shoot_extra = 0
            self.spawn_extra = 0.4

        elif self.difficulty == "NORMAL":
            self.lives = 6
            self.enemy_speed_extra = 40
            self.enemy_shoot_extra = 400
            self.spawn_extra = 0

        elif self.difficulty == "DIFICIL":
            self.lives = 3
            self.enemy_speed_extra = 90
            self.enemy_shoot_extra = 900
            self.spawn_extra = -0.3

        # Sacamos la ruta principal del proyecto.
        # Esto ayuda a que las imagenes carguen aunque el juego
        # se ejecute desde otra carpeta.
        base_path = os.path.dirname(os.path.dirname(__file__))

        # Cargamos la imagen del jugador.
        try:
            nave_path = os.path.join(base_path, "assets", "nave.png")

            self.player_img = pygame.image.load(nave_path).convert_alpha()
            self.player_img = pygame.transform.scale(self.player_img, (50, 50))
            self.player_rect = self.player_img.get_rect()

        except Exception as error:
            # Si falla la imagen, mostramos el error en la terminal.
            print("No se pudo cargar la imagen de la nave:", error)

            # Si no carga, usamos un cuadro azul como respaldo.
            self.player_img = None
            self.player_rect = pygame.Rect(0, 0, 50, 50)

        # Cargamos la imagen del enemigo.
        try:
            enemy_path = os.path.join(base_path, "assets", "nave_enemiga.png")

            self.enemy_img = pygame.image.load(enemy_path).convert_alpha()
            self.enemy_img = pygame.transform.scale(self.enemy_img, (50, 35))

        except Exception as error:
            # Si falla, mostramos el error.
            print("No se pudo cargar la imagen del enemigo:", error)

            # Si no carga, los enemigos se dibujan como cuadros rojos.
            self.enemy_img = None

        # --- CARGA DE EFECTOS DE SONIDO ---
        try:
            self.snd_laser = pygame.mixer.Sound(os.path.join(base_path, "assets", "urlaser.wav"))
            self.snd_explosion = pygame.mixer.Sound(os.path.join(base_path, "assets", "explosion.mp3"))
            self.snd_hurt = pygame.mixer.Sound(os.path.join(base_path, "assets", "golpe.wav"))
            self.snd_gameover = pygame.mixer.Sound(os.path.join(base_path, "assets", "gameover.wav"))

            # Ajustes de volúmenes por defecto (valores entre 0.0 y 1.0)
            self.snd_laser.set_volume(0.37)
            self.snd_explosion.set_volume(0.05)
            self.snd_hurt.set_volume(0.37)
            self.snd_gameover.set_volume(0.5)
        except Exception as error:
            print("No se pudieron cargar los efectos de sonido:", error)
            self.snd_laser = None
            self.snd_explosion = None
            self.snd_hurt = None
            self.snd_gameover = None
            self.snd_victory = None

        # Posicion inicial de la nave.
        self.player_rect.centerx = SCREEN_WIDTH // 2
        self.player_rect.bottom = SCREEN_HEIGHT - 20

        # Velocidad de movimiento del jugador.
        self.speed = 450

        # Listas del juego.
        # Aqui se guardan balas, balas enemigas y enemigos.
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []

        # Velocidad de las balas.
        self.bullet_speed = 600

        # Estrellas del fondo.
        # Cada estrella guarda:
        # x, y, velocidad.
        self.stars = []

        for i in range(60):
            star_x = random.randint(0, SCREEN_WIDTH)
            star_y = random.randint(0, SCREEN_HEIGHT)
            star_speed = random.randint(20, 80)
            self.stars.append([star_x, star_y, star_speed])

        # Temporizador para controlar cada cuanto aparecen enemigos.
        self.spawn_timer = 0

        # Mientras menor sea este numero, mas rapido aparecen enemigos.
        self.spawn_rate = max(0.4, 2.0 - (self.level * 0.2) + self.spawn_extra)

    def go_menu(self):
        """
        Regresa al menu principal.
        """

        from states.menu_state import MenuState
        self.game.change_state(MenuState(self.game))

    def shoot(self):
        """
        Crea una bala del jugador.
        """

        # La bala aparece arriba de la nave.
        new_bullet = pygame.Rect(self.player_rect.centerx - 2, self.player_rect.top, 5, 10)
        self.bullets.append(new_bullet)

        # Sonido de disparo del jugador
        if self.snd_laser:
            self.snd_laser.play()

    def enemy_shoot(self, enemy):
        """
        Crea una bala enemiga.
        """

        # La bala enemiga aparece debajo del enemigo.
        new_bullet = pygame.Rect(enemy.rect.centerx - 2, enemy.rect.bottom, 5, 10)
        self.enemy_bullets.append(new_bullet)

    def trigger_game_over(self):
        """
        Activa el Game Over y reproduce el sonido correspondiente.
        """
        self.game_over = True
        if self.snd_gameover:
            self.snd_gameover.play()

    def handle_events(self, events):
        """
        Revisa teclas y eventos del juego.
        """

        for event in events:
            # Revisamos el boton de volver al menu.
            self.back_button.handle_event(event)

            if event.type == pygame.KEYDOWN:

                # ESC vuelve al menu en cualquier momento.
                if event.key == pygame.K_ESCAPE:
                    self.go_menu()
                    return

                # Antes de empezar, ENTER inicia el nivel.
                if self.waiting_start:
                    if event.key == pygame.K_RETURN:
                        self.waiting_start = False
                    return

                # Si ya ganaste o perdiste:
                # R reinicia.
                # M vuelve al menu.
                if self.level_complete or self.game_over:
                    if event.key == pygame.K_r:
                        self.game.change_state(PlayState(self.game))

                    if event.key == pygame.K_m:
                        self.go_menu()

                    return

                # P pausa o reanuda.
                if event.key == pygame.K_p:
                    self.is_paused = not self.is_paused

                # ESPACIO dispara si no esta pausado.
                if event.key == pygame.K_SPACE and not self.is_paused:
                    self.shoot()

    def update(self, dt):
        """
        Actualiza la logica del juego.

        Aqui se mueven:
        - estrellas
        - jugador
        - enemigos
        - balas
        """

        # Si el juego esta esperando, pausado, perdido o completado,
        # no actualizamos la logica.
        if self.waiting_start or self.is_paused or self.game_over or self.level_complete:
            return

        # Control del tiempo.
        if self.mode != "SUPERVIVENCIA":
            self.time_left -= dt

            if self.time_left <= 0:
                self.time_left = 0

                # En modo clasico se gana sobreviviendo hasta que termine el tiempo.
                if self.mode == "MODO CLASICO":
                    self.complete_level()
                    return

                # En contrarreloj se revisa si alcanzaste el puntaje.
                if self.mode == "CONTRARRELOJ":
                    if self.score >= self.target_score:
                        self.complete_level()
                    else:
                        self.trigger_game_over()
                    return

        # Mover estrellas del fondo.
        for star in self.stars:
            star[1] += star[2] * dt

            # Si una estrella sale por abajo, vuelve a aparecer arriba.
            if star[1] > SCREEN_HEIGHT:
                star[0] = random.randint(0, SCREEN_WIDTH)
                star[1] = 0
                star[2] = random.randint(20, 80)

        # Movimiento del jugador.
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_rect.x -= self.speed * dt

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_rect.x += self.speed * dt

        # Evita que la nave se salga de la pantalla.
        self.player_rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Generar enemigos.
        self.spawn_timer += dt

        if self.spawn_timer >= self.spawn_rate:
            # Velocidad del enemigo segun nivel y dificultad.
            enemy_speed = 100 + (self.level * 20) + self.enemy_speed_extra

            # Tiempo que tarda el enemigo en disparar.
            # Mientras menor sea el numero, mas rapido dispara.
            shoot_delay = max(700, 3000 - (self.level * 300) - self.enemy_shoot_extra)

            # Margen para que los enemigos no aparezcan demasiado pegados a los bordes.
            margen = 100
            area_inicio = margen
            area_fin = SCREEN_WIDTH - margen - 40

            # Creamos enemigo nuevo.
            new_enemy = Enemy(random.randint(area_inicio, area_fin), -40, enemy_speed, shoot_delay)
            self.enemies.append(new_enemy)

            # Reiniciamos el contador de aparicion.
            self.spawn_timer = 0

        # Actualizar enemigos.
        for e in self.enemies[:]:
            e.update(dt)

            # Si el enemigo puede disparar, dispara.
            if e.can_shoot():
                self.enemy_shoot(e)

            # Si el enemigo llega abajo o choca con el jugador,
            # el jugador pierde una vida.
            if e.rect.top > SCREEN_HEIGHT or e.rect.colliderect(self.player_rect):
                self.lives -= 1
                self.enemies.remove(e)

                if self.lives <= 0:
                    self.trigger_game_over()
                elif self.snd_hurt:
                    self.snd_hurt.play()

        # Actualizar balas del jugador.
        for b in self.bullets[:]:
            # La bala sube.
            b.y -= self.bullet_speed * dt

            # Si sale de la pantalla, se borra.
            if b.bottom < 0:
                self.bullets.remove(b)
                continue

            # Revisamos si la bala toca algun enemigo.
            for e in self.enemies[:]:
                if b.colliderect(e.rect):
                    if b in self.bullets:
                        self.bullets.remove(b)

                    if e in self.enemies:
                        self.enemies.remove(e)

                    # Sonido de explosión del enemigo al morir
                    if self.snd_explosion:
                        self.snd_explosion.play()

                    # Sumamos puntos al destruir un enemigo.
                    self.score += 10
                    break

        # Actualizar balas enemigas.
        for eb in self.enemy_bullets[:]:
            # La bala enemiga baja.
            eb.y += (self.bullet_speed // 2) * dt

            # Si sale por abajo, se borra.
            if eb.top > SCREEN_HEIGHT:
                self.enemy_bullets.remove(eb)
                continue

            # Si toca al jugador, pierde una vida.
            if eb.colliderect(self.player_rect):
                self.lives -= 1
                self.enemy_bullets.remove(eb)

                if self.lives <= 0:
                    self.trigger_game_over()
                elif self.snd_hurt:
                    self.snd_hurt.play()

        # En contrarreloj, si alcanzas el puntaje antes de que termine el tiempo, ganas.
        if self.mode == "CONTRARRELOJ" and self.score >= self.target_score:
            self.complete_level()

    def complete_level(self):
        """
        Marca el nivel como completado y desbloquea el siguiente nivel.
        """

        # Si ya estaba completado, no hacemos nada otra vez.
        if self.level_complete:
            return

        # Marcamos el nivel como completado.
        self.level_complete = True

        # Si completaste el nivel mas alto desbloqueado,
        # desbloqueamos el siguiente.
        if self.level >= self.game.data["unlocked_level"]:
            self.game.data["unlocked_level"] = min(self.level + 1, len(LEVELS))

    def draw_center_text(self, screen, text, font, color, y):
        """
        Dibuja texto centrado en pantalla.
        """

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y))
        screen.blit(text_surface, text_rect)

    def draw_lives(self, screen):
        """
        Dibuja las vidas del jugador.
        """

        # Texto "Vidas:"
        vidas_text = self.text_font.render("Vidas:", True, WHITE)
        screen.blit(vidas_text, (40, 255))

        # Dibujamos las vidas como cuadritos rojos, no puse los corazones xD.
        for i in range(self.lives):
            pygame.draw.rect(screen, RED, (125 + (i * 35), 260, 25, 25))

    def draw(self, screen):
        """
        Dibuja todo lo que aparece en pantalla durante el juego.
        """

        # Dibujar estrellas del fondo.
        for star in self.stars:
            pygame.draw.circle(screen, WHITE, (int(star[0]), int(star[1])), 2)

        # Dibujar balas del jugador.
        for bullet in self.bullets:
            pygame.draw.rect(screen, YELLOW, bullet)

        # Dibujar balas enemigas.
        for e_bullet in self.enemy_bullets:
            pygame.draw.rect(screen, RED, e_bullet)

        # Dibujar enemigos.
        for e in self.enemies:
            if self.enemy_img:
                screen.blit(self.enemy_img, e.rect)
            else:
                pygame.draw.rect(screen, RED, e.rect)

        # Dibujar nave del jugador.
        if self.player_img:
            screen.blit(self.player_img, self.player_rect)
        else:
            pygame.draw.rect(screen, LIGHT_BLUE, self.player_rect)

        # Dibujar vidas.
        self.draw_lives(screen)

        # Dibujar tiempo.
        if self.mode == "SUPERVIVENCIA":
            timer_text = self.text_font.render("Tiempo: Sin limite", True, YELLOW)
        else:
            timer_text = self.text_font.render(f"Tiempo: {int(self.time_left)}s", True, YELLOW)

        screen.blit(timer_text, (SCREEN_WIDTH - 230, 40))

        # Dibujar puntaje.
        score_text = self.text_font.render(f"Score: {self.score}", True, GREEN)
        screen.blit(score_text, (40, 80))

        # Dibujar dificultad.
        difficulty_text = self.text_font.render(f"Dificultad: {self.difficulty}", True, WHITE)
        screen.blit(difficulty_text, (40, 115))

        # Dibujar nivel.
        level_text = self.text_font.render(f"Nivel: {self.level}", True, WHITE)
        screen.blit(level_text, (40, 150))

        # Dibujar modo.
        mode_text = self.text_font.render(f"Modo: {self.mode}", True, WHITE)
        screen.blit(mode_text, (40, 185))

        # Dibujar objetivo dependiendo del modo.
        if self.mode == "MODO CLASICO":
            objective_text = self.text_font.render(
                "Objetivo: Sobrevive hasta que acabe el tiempo",
                True,
                YELLOW
            )

        elif self.mode == "SUPERVIVENCIA":
            objective_text = self.text_font.render(
                "Objetivo: Aguanta lo mas que puedas",
                True,
                YELLOW
            )

        elif self.mode == "CONTRARRELOJ":
            objective_text = self.text_font.render(
                f"Objetivo: Llega a {self.target_score} puntos",
                True,
                YELLOW
            )

        screen.blit(objective_text, (40, 220))

        # Pantalla antes de iniciar el nivel.
        if self.waiting_start:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            self.draw_center_text(screen, "PREPARADO", self.title_font, YELLOW, SCREEN_HEIGHT // 2 - 130)
            self.draw_center_text(screen, f"Modo: {self.mode}", self.text_font, WHITE, SCREEN_HEIGHT // 2 - 70)
            self.draw_center_text(screen, f"Dificultad: {self.difficulty}", self.text_font, WHITE, SCREEN_HEIGHT // 2 - 30)
            self.draw_center_text(screen, f"Nivel: {self.level}", self.text_font, WHITE, SCREEN_HEIGHT // 2 + 10)
            self.draw_center_text(screen, "Presiona ENTER para comenzar", self.text_font, GREEN, SCREEN_HEIGHT // 2 + 80)

        # Pantalla de pausa.
        if self.is_paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            self.draw_center_text(screen, "PAUSA", self.title_font, WHITE, SCREEN_HEIGHT // 2 - 50)
            self.draw_center_text(screen, "Presiona P para continuar", self.text_font, YELLOW, SCREEN_HEIGHT // 2 + 10)

        # Pantalla de Game Over.
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            self.draw_center_text(screen, "GAME OVER", self.title_font, RED, SCREEN_HEIGHT // 2 - 110)
            self.draw_center_text(screen, f"Puntaje final: {self.score}", self.text_font, GREEN, SCREEN_HEIGHT // 2 - 50)
            self.draw_center_text(screen, "Presiona R para reintentar", self.text_font, WHITE, SCREEN_HEIGHT // 2 + 10)
            self.draw_center_text(screen, "Presiona M para volver al menu", self.text_font, WHITE, SCREEN_HEIGHT // 2 + 50)

        # Pantalla de nivel completado.
        if self.level_complete:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            self.draw_center_text(screen, "NIVEL COMPLETADO", self.title_font, GREEN, SCREEN_HEIGHT // 2 - 110)
            self.draw_center_text(screen, f"Puntaje final: {self.score}", self.text_font, YELLOW, SCREEN_HEIGHT // 2 - 50)
            self.draw_center_text(screen, "Presiona R para jugar otra vez", self.text_font, WHITE, SCREEN_HEIGHT // 2 + 10)
            self.draw_center_text(screen, "Presiona M para volver al menu", self.text_font, WHITE, SCREEN_HEIGHT // 2 + 50)

        # Dibujamos el boton de volver al menu al final
        # para que siempre quede visible encima de todo.
        self.back_button.draw(screen)