

# core_button.py 

import pygame
from settings import WHITE, LIGHT_BLUE, DARK_GRAY, YELLOW

class Button:
    """
    clase para crear botones reutilizables 

    """
    def __init__(self, rect, text, font, callback, bg_color=DARK_GRAY, text_color=WHITE):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback
        self.bg_color = bg_color
        self.text_color = text_color

        # indica si el maus esta encima del boton 
        self.hovered = False 

    def handle_event(self, event):
        """
        detecta si el maus da clik en el boton 
        """
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def draw(self, screen):
        """
        intente que se dibuje el boton xD 
        """
        color = LIGHT_BLUE if self.hovered else self.bg_color
        pygame.draw.rect(screen, color, self.rect, border_radius=12)

        #Borde 
        pygame.draw.rect(screen, YELLOW, self.rect, 3, border_radius=12)

        #texto centrado
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)






