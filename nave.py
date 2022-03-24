import pygame
from pygame.sprite import Sprite


class Nave(Sprite):
    """sirve para gestionar el comportamiento de la nave"""
    
    def __init__(self, ai_configuraciones, pantalla):
        """inicializa la nave y establece su posicion de partida"""
        super(Nave, self).__init__()
        self.pantalla = pantalla
        self.ai_configuraciones = ai_configuraciones

        #carga la imagen de la nave y obtiene su rect
        self.image = pygame.image.load("imagenes/nave.bmp")
        self.rect = self.image.get_rect()
        self.pantalla_rect = pantalla.get_rect()

        #empieza cada nueva nave en la parte inferior central de la pantalla
        self.rect.centerx = self.pantalla_rect.centerx
        self.rect.bottom = self.pantalla_rect.bottom

        # almacena un valor decimal para el centro de la nave
        self.center = float(self.rect.centerx)

        # banderas de movimiento
        self.moving_right = False
        self.moving_left = False
        
    def update(self):
        """Actualiza la posicion de la nave segun las banderas de movimiento"""
        if self.moving_right and self.rect.right < self.pantalla_rect.right:
            self.center += self.ai_configuraciones.factor_velocidad_nave
        
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_configuraciones.factor_velocidad_nave
            
        #actualiza el objeto rect desde self.center
        self.rect.centerx = self.center

    def blitme(self):
        """dibuja la nave en su ubicacion actual"""
        self.pantalla.blit(self.image, self.rect)
    
    def centrar_nave(self):
        """centra la nave en la pantalla"""
        self.center = self.pantalla_rect.centerx