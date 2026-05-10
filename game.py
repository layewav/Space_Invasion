# archivo game.py

import pygame
from settings import LIGHT_BLUE, SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, FPS, DARK_BLUE
from states.menu_state import MenuState


class Game:
    """
    Clase principal del juego
    Esta clase inicializa pygame, crea una ventana, lleva el control de reloj o los FPS
    Guarda el estado actual del juego
    corre el bucle principal 

    """
    def __init__(self):
        pygame.init()

        #crear la ventana principal 
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        #Reloj para controlar los FPS
        self.clock = pygame.time.Clock()

        # una bandera para saber si el juego sigue corriendo 
        self.running = True

        # Datos globales del juego
        # Aqui guardamos cosas que luego usaran varios estados 
        self.data = {"mode": None, "difficulty": None, "level": None}

        #Estado inicial del juego
        self.current_state = MenuState(self)

    def change_state(self, new_state):
        """
        Cambia el estado actual por otro
        esto permite pasar de menu a seleccion de modo, etc 
        """
        self.current_state = new_state

    def quit(self):
        """
        cierra el juego correctamente
        """
        self.running = False

    def run(self):
        """
        bucle principal del juego 
        mientras running sea True el juego sigue vivo
        """
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0 

            #Capturamos todos los eventos del frame actual
            events = pygame.event.get()

            #si el usuario cierra la ventana terminamos
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit()

            # actualizar el estado actual 
            self.current_state.handle_events(events)
            self.current_state.update(dt)

            #dibuja el fondo base 
            self.screen.fill(DARK_BLUE)

            # dinujar el estado actual 
            self.current_state.draw(self.screen)

            #actualizar la pantalla 
            pygame.display.flip()

        pygame.quit()
def draw(self, screen):
    # Si la imagen cargó, la dibujamos
    if self.player_img:
        screen.blit(self.player_img, self.player_rect)
    else:
        # Si no hay imagen, dibujamos un cuadro azul para probar movimiento
        pygame.draw.rect(screen, LIGHT_BLUE, self.player_rect)