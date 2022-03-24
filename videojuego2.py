import pygame
from pygame.sprite import Group

from configuraciones import Configuraciones
from estadisticas import Estadisticas
from marcador import Marcador
from button import Button
from nave import Nave

import funciones_juego as fj

def run_game():
    # iniciar el juego, las configuraciones y crear objeto de pantalla 
    pygame.init()
    ai_configuraciones = Configuraciones()
    pantalla = pygame.display.set_mode((ai_configuraciones.screen_width, ai_configuraciones.screen_height))
    pygame.display.set_caption("Invasion alienigena (Por David Garcia)")

    #crea el boton Play
    play_button = Button(ai_configuraciones, pantalla, "Play")

    #crea una instancia para almacenar estadistias del juego y crea un marcador
    estadisticas = Estadisticas(ai_configuraciones)
    marcador = Marcador(ai_configuraciones, pantalla, estadisticas)
    # crea una nave, un grupo de balas y un grupo de aliens
    nave = Nave(ai_configuraciones, pantalla)
    balas = Group()
    aliens = Group()

    # crea la flota de alienigenas
    fj.crear_flota(ai_configuraciones, pantalla, nave, aliens)

    

    # iniciar el bucle principal del juego
    while True:

        # escuchar eventos de teclado o raton
        fj.verificar_eventos(ai_configuraciones, pantalla, estadisticas, marcador, play_button, nave, aliens, balas)
        
        if estadisticas.game_active:
            nave.update()       
            fj.update_balas(ai_configuraciones, pantalla, estadisticas, marcador, nave, aliens, balas)
            fj.update_aliens(ai_configuraciones, estadisticas, pantalla, marcador, nave, aliens, balas)
        
        fj.actualizar_pantalla(ai_configuraciones, pantalla, estadisticas, marcador, nave, aliens, balas, play_button)
  
run_game()