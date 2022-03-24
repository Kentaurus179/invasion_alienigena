import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """sirve para representar a un solo alien en la flota"""
    def __init__(self, ai_configuraciones, pantalla):
        super(Alien, self).__init__()

        self.pantalla = pantalla
        self.ai_configuraciones = ai_configuraciones

        #carga la imagen del alien y establece su atributo rect
        self.image = pygame.image.load("imagenes/alien.bmp")
        self.rect = self.image.get_rect()

        #inicia cada nuevo alien cerca de la parte superior izquierda de la pantalla
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #almacena la posicion exacta del alien
        self.x = float(self.rect.x)

    def blitme(self):
        """dibuja el alien en su ubicacion actual"""
        self.pantalla.blit(self.image, self.rect)
    
    def check_edges(self):
        """devuelve verdadero si el alien esta en el borde de la pantalla"""
        screen_rect = self.pantalla.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """mueve el alien a la derecha"""
        self.x += (self.ai_configuraciones.alien_speed_factor * self.ai_configuraciones.fleet_direction)
        self.rect.x = self.x
