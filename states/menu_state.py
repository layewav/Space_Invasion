# states/menu_state.py
# Este archivo contiene la pantalla del menu principal.

import pygame

# State es la clase base que usan todas las pantallas del juego.
from core.state import State

# Button es nuestra clase para crear botones.
from core.button import Button

# Importamos colores y tamaño de pantalla.
from settings import WHITE, YELLOW, SCREEN_WIDTH


class MenuState(State):
    """
    Esta clase representa el menu principal del juego.

    Desde aqui el jugador puede:
    1. Empezar a jugar.
    2. Ver instrucciones.
    3. Ver creditos.
    4. Salir del juego.
    """

    def __init__(self, game):
        """
        Este metodo se ejecuta cuando se crea el menu.
        Aqui preparamos fuentes, botones y variables.
        """

        # Llamamos al constructor de la clase State.
        # Esto guarda la referencia al juego principal.
        super().__init__(game)

        # Fuente grande para el titulo.
        self.title_font = pygame.font.SysFont("arial", 60, bold=True)

        # Fuente normal para botones y subtitulo.
        self.text_font = pygame.font.SysFont("arial", 28)

        # Fuente pequeña para instrucciones y creditos.
        self.small_font = pygame.font.SysFont("arial", 20)

        # Estas variables sirven para saber si se deben mostrar
        # las instrucciones o los creditos.
        self.showing_credits = False
        self.showing_instructions = False

        # Lista de botones del menu.
        # Cada boton tiene:
        # posicion, texto, fuente y funcion que ejecuta al hacer clic.
        self.buttons = [
            Button((350, 230, 300, 55), "Jugar", self.text_font, self.start_game),
            Button((350, 300, 300, 55), "Instrucciones", self.text_font, self.show_instructions),
            Button((350, 370, 300, 55), "Creditos", self.text_font, self.show_credits),
            Button((350, 440, 300, 55), "Salir", self.text_font, self.exit_game),
        ]

    def start_game(self):
        """
        Esta funcion se ejecuta cuando el jugador presiona "Jugar".
        Cambia del menu principal a la pantalla para elegir modo.
        """

        # Importamos aqui para evitar errores de importacion circular.
        from states.mode_state import ModeState

        # Cambiamos la pantalla actual por la pantalla de modos.
        self.game.change_state(ModeState(self.game))

    def show_credits(self):
        """
        Muestra u oculta los creditos.
        Tambien apaga las instrucciones para que no se encimen.
        """

        # Si estaba en False, pasa a True.
        # Si estaba en True, pasa a False.
        self.showing_credits = not self.showing_credits

        # Apagamos instrucciones para que no aparezcan las dos cosas juntas.
        self.showing_instructions = False

    def show_instructions(self):
        """
        Muestra u oculta las instrucciones.
        Tambien apaga los creditos para que no se encimen.
        """

        # Si estaba en False, pasa a True.
        # Si estaba en True, pasa a False.
        self.showing_instructions = not self.showing_instructions

        # Apagamos creditos para que no aparezcan las dos cosas juntas.
        self.showing_credits = False

    def exit_game(self):
        """
        Cierra el juego.
        """

        # Le avisamos al objeto Game que debe cerrar el juego.
        self.game.quit()

    def handle_events(self, events):
        """
        Revisa los eventos del menu.
        Por ejemplo, clics del mouse sobre los botones.
        """

        for event in events:
            # Mandamos cada evento a cada boton.
            # Asi los botones pueden saber si les hicieron clic.
            for button in self.buttons:
                button.handle_event(event)

    def update(self, dt):
        """
        En el menu no hay movimiento ni enemigos.
        Por eso este metodo queda vacio.
        """

        pass

    def draw(self, screen):
        """
        Dibuja el menu principal en la pantalla.
        """

        # Dibujamos el titulo principal.
        title_surface = self.title_font.render("SPACE INVASION", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        # Dibujamos el subtitulo del proyecto.
        subtitle_surface = self.text_font.render("Proyecto de Programacion II", True, YELLOW)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(subtitle_surface, subtitle_rect)

        # Dibujamos todos los botones.
        for button in self.buttons:
            button.draw(screen)

        # Si el jugador presiono "Instrucciones", mostramos los controles.
        if self.showing_instructions:
            instructions = [
                "CONTROLES:",
                "A / Flecha izquierda = mover a la izquierda",
                "D / Flecha derecha = mover a la derecha",
                "ESPACIO = disparar",
                "P = pausar",
                "ENTER = comenzar el nivel",
                "R = reiniciar cuando pierdes o ganas",
                "M = volver al menu cuando pierdes o ganas",
                "ESC = volver al menu en cualquier momento",
            ]

            # Posicion inicial del texto.
            y = 500

            # Dibujamos cada linea de instrucciones.
            for line in instructions:
                text = self.small_font.render(line, True, WHITE)
                rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
                screen.blit(text, rect)

                # Bajamos para que la siguiente linea no se encime.
                y += 20

        # Si el jugador presiono "Creditos", mostramos los creditos.
        if self.showing_credits:
            credits = [
                "Proyecto hecho por:",
                "Garcia Guzman Victor Manuel",
                "Aqui van ustedes xD",
            ]

            y = 540

            for line in credits:
                text = self.small_font.render(line, True, WHITE)
                rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
                screen.blit(text, rect)
                y += 30