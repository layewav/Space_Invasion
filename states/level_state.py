# states/level_state.py
# Este archivo contiene la pantalla para elegir nivel.
# Aqui tambien se controla si un nivel esta bloqueado o desbloqueado.

import pygame
from core.state import State
from core.button import Button
from settings import WHITE, YELLOW, GREEN, LEVELS, SCREEN_WIDTH


class LevelState(State):
    """
    Pantalla para elegir nivel.

    El Nivel 1 inicia desbloqueado.
    Los demas niveles se van desbloqueando conforme el jugador completa niveles.
    """

    def __init__(self, game):
        """
        Prepara la pantalla de niveles.
        """

        super().__init__(game)

        # Fuente grande para el titulo.
        self.title_font = pygame.font.SysFont("arial", 50, bold=True)

        # Fuente para los botones.
        self.text_font = pygame.font.SysFont("arial", 25)

        # Fuente pequeña para textos de ayuda.
        self.small_font = pygame.font.SysFont("arial", 22)

        # Lista donde guardaremos los botones de niveles.
        self.buttons = []

        # Creamos los botones dependiendo de los niveles desbloqueados.
        self.create_buttons()

        # Boton para regresar a dificultad.
        self.back_button = Button((20, 20, 150, 50), "Regresar", self.text_font, self.go_back)

    def create_buttons(self):
        """
        Crea los botones de los niveles.

        Si un nivel esta desbloqueado:
        aparece normal.

        Si un nivel esta bloqueado:
        aparece con el texto "BLOQUEADO".
        """

        # Limpiamos la lista para reconstruir los botones.
        self.buttons = []

        # Posicion vertical inicial.
        y = 160

        # Recorremos todos los niveles configurados en settings.py.
        for level in LEVELS:
            # Sacamos el numero del nivel.
            # Ejemplo:
            # "Nivel 3" -> 3
            level_number = int(level.split()[-1])

            # Revisamos si el nivel esta desbloqueado.
            if self.is_level_unlocked(level_number):
                text = level
            else:
                text = level + "  BLOQUEADO"

            # Creamos el boton.
            self.buttons.append(
                Button(
                    (330, y, 340, 50),
                    text,
                    self.text_font,
                    lambda l=level: self.select_level(l)
                )
            )

            # Bajamos el siguiente boton.
            y += 65

    def is_level_unlocked(self, level_number):
        """
        Revisa si un nivel esta desbloqueado.

        Un nivel esta desbloqueado si:
        1. all_levels_unlocked es True.
        2. O el numero del nivel es menor o igual al nivel desbloqueado actual.
        """

        # Si se activo el truco de pruebas, todos los niveles se desbloquean.
        if self.game.data["all_levels_unlocked"]:
            return True

        # Si no esta activado el truco, solo se desbloquean
        # los niveles menores o iguales al progreso actual.
        return level_number <= self.game.data["unlocked_level"]

    def select_level(self, level):
        """
        Intenta entrar al nivel seleccionado.

        Si el nivel esta bloqueado, no hace nada.
        Si el nivel esta desbloqueado, guarda el nivel y entra al juego.
        """

        # Sacamos el numero del nivel.
        level_number = int(level.split()[-1])

        # Si esta bloqueado, no entramos.
        if not self.is_level_unlocked(level_number):
            return

        from states.play_state import PlayState

        # Guardamos el nivel elegido.
        self.game.data["level"] = level

        # Cambiamos a la pantalla de juego.
        self.game.change_state(PlayState(self.game))

    def unlock_all_levels(self):
        """
        Desbloquea todos los niveles.

        Esto es para hacer pruebas sin tener que completar
        nivel por nivel.
        """

        # Activamos la variable de prueba.
        self.game.data["all_levels_unlocked"] = True

        # Ponemos como desbloqueado el ultimo nivel.
        self.game.data["unlocked_level"] = len(LEVELS)

        # Volvemos a crear los botones para que ya aparezcan desbloqueados.
        self.create_buttons()

    def go_back(self):
        """
        Regresa a la pantalla de dificultad.
        """

        from states.difficulty_state import DifficultyState
        self.game.change_state(DifficultyState(self.game))

    def handle_events(self, events):
        """
        Revisa clics en botones y tambien la combinacion secreta.
        """

        for event in events:
            # Revisamos botones de niveles.
            for button in self.buttons:
                button.handle_event(event)

            # Revisamos boton de regresar.
            self.back_button.handle_event(event)

            # Revisamos teclas.
            if event.type == pygame.KEYDOWN:
                # Obtenemos las teclas especiales presionadas.
                # Ejemplo: CTRL, SHIFT, ALT.
                mods = pygame.key.get_mods()

                # Revisamos si CTRL esta presionado.
                ctrl_pressed = mods & pygame.KMOD_CTRL

                # Revisamos si SHIFT esta presionado.
                shift_pressed = mods & pygame.KMOD_SHIFT

                # Combinacion secreta:
                # CTRL + SHIFT + U desbloquea todos los niveles.
                if event.key == pygame.K_u and ctrl_pressed and shift_pressed:
                    self.unlock_all_levels()

    def update(self, dt):
        """
        No hay movimiento en esta pantalla.
        """

        pass

    def draw(self, screen):
        """
        Dibuja la pantalla de seleccion de nivel.
        """

        # Dibujamos el titulo.
        title = self.title_font.render("Elige el nivel", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 90))
        screen.blit(title, title_rect)

        # Mostramos cual es el nivel maximo desbloqueado.
        unlocked_text = self.small_font.render(
            f"Nivel desbloqueado: {self.game.data['unlocked_level']}",
            True,
            GREEN
        )
        unlocked_rect = unlocked_text.get_rect(center=(SCREEN_WIDTH // 2, 125))
        screen.blit(unlocked_text, unlocked_rect)

        # Dibujamos los botones de niveles.
        for button in self.buttons:
            button.draw(screen)

        # Texto de ayuda.
        help_text = self.small_font.render(
            "Completa un nivel para desbloquear el siguiente",
            True,
            YELLOW
        )
        help_rect = help_text.get_rect(center=(SCREEN_WIDTH // 2, 640))
        screen.blit(help_text, help_rect)

        # Dibujamos boton de regresar.
        self.back_button.draw(screen)