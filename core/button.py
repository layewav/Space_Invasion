# core/button.py
# Este archivo contiene la clase Button.

# La clase Button sirve para crear botones reutilizables.
# Asi no tenemos que programar un boton desde cero en cada pantalla.

# Se usa en:
# - Menu principal
# - Seleccion de modo
# - Seleccion de dificultad
# - Seleccion de nivel
# - Boton para volver al menu durante el juego

import pygame

# Importamos colores desde settings.py.
# Esto ayuda a que todos los botones usen los mismos colores.
from settings import WHITE, LIGHT_BLUE, DARK_GRAY, YELLOW


class Button:
    """
    Clase para crear botones.

    Cada boton tiene:
    - Un rectangulo que indica posicion y tamaño.
    - Un texto.
    - Una fuente.
    - Una funcion que se ejecuta al hacer clic.
    - Colores para fondo y texto.
    """

    def __init__(self, rect, text, font, callback, bg_color=DARK_GRAY, text_color=WHITE):
        """
        Crea un boton nuevo.

        rect:
            Posicion y tamaño del boton.
            Ejemplo: (350, 230, 300, 55)
            Significa:
            x = 350
            y = 230
            ancho = 300
            alto = 55

        text:
            Texto que aparece dentro del boton.

        font:
            Fuente que se usa para dibujar el texto.

        callback:
            Funcion que se ejecuta cuando el usuario hace clic en el boton.

        bg_color:
            Color normal del boton.

        text_color:
            Color del texto.
        """

        # Convertimos rect en un rectangulo de pygame.
        # Este rectangulo sirve para dibujar y detectar clics.
        self.rect = pygame.Rect(rect)

        # Texto que se mostrara en el boton.
        self.text = text

        # Fuente usada para dibujar el texto.
        self.font = font

        # Funcion que se ejecuta al presionar el boton.
        self.callback = callback

        # Color normal del fondo del boton.
        self.bg_color = bg_color

        # Color del texto.
        self.text_color = text_color

        # Esta variable indica si el mouse esta encima del boton.
        # Se usa para cambiar el color cuando el usuario pasa el mouse.
        self.hovered = False

    def handle_event(self, event):
        """
        Revisa eventos relacionados con el boton.

        Este metodo detecta:
        - Si el mouse esta encima del boton.
        - Si el usuario hizo clic izquierdo sobre el boton.
        """

        # Si el mouse se mueve, revisamos si esta encima del boton.
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        # Si el usuario hace clic izquierdo.
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # Revisamos si el clic fue dentro del boton.
            if self.rect.collidepoint(event.pos):

                # Ejecutamos la funcion asignada al boton.
                self.callback()

    def draw(self, screen):
        """
        Dibuja el boton en pantalla.
        """

        # Si el mouse esta encima, usamos otro color.
        # Si no, usamos el color normal.
        color = LIGHT_BLUE if self.hovered else self.bg_color

        # Dibujamos el fondo del boton.
        # border_radius hace que las esquinas sean redondeadas.
        pygame.draw.rect(screen, color, self.rect, border_radius=12)

        # Dibujamos el borde del boton.
        pygame.draw.rect(screen, YELLOW, self.rect, 3, border_radius=12)

        # Creamos la imagen del texto.
        text_surface = self.font.render(self.text, True, self.text_color)

        # Centramos el texto dentro del boton.
        text_rect = text_surface.get_rect(center=self.rect.center)

        # Dibujamos el texto en pantalla.
        screen.blit(text_surface, text_rect)