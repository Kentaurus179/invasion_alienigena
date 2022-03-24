import sys
from time import sleep

import pygame
from bala import Bala

from alien import Alien

def verificar_eventos_keydown(event, ai_configuraciones, pantalla, nave, balas):
    """responde a las pulsaciones de las teclas"""
    if event.key == pygame.K_RIGHT:
        nave.moving_right = True
    elif event.key == pygame.K_LEFT:
        nave.moving_left = True
    elif event.key == pygame.K_SPACE:
        fuego_bala(ai_configuraciones, pantalla, nave, balas)
    elif event.key == pygame.K_q:
        sys.exit()



def verificar_eventos_keyup(event, nave):
    """responde a las pulsaciones de las teclas"""
    if event.key == pygame.K_RIGHT:
        nave.moving_right = False
    elif event.key == pygame.K_LEFT:
        nave.moving_left = False

def verificar_eventos(ai_configuraciones, pantalla, estadisticas, marcador, play_button, nave, aliens, balas):
    """Responde a las pulsaciones de teclas y los eventos del raton"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            verificar_eventos_keydown(event, ai_configuraciones, pantalla, nave, balas)
        elif event.type == pygame.KEYUP:
            verificar_eventos_keyup(event, nave)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_configuraciones, pantalla, estadisticas, marcador, play_button, nave, aliens, balas, mouse_x, mouse_y)

def check_play_button(ai_configuraciones, pantalla, estadisticas, marcador, play_button, nave, aliens, balas, mouse_x, mouse_y):
    """comienza un nuevo juego cuando el jugador hace click en play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not estadisticas.game_active:
        #restablece la configuracion del juego
        ai_configuraciones.inicializa_configuraciones_dinamicas()

        #ocultar el cursor del mouse
        pygame.mouse.set_visible(False)

        #restablese las estadisticas del juego
        estadisticas.reset_stats()
        estadisticas.game_active = True

        marcador.prep_puntaje()
        marcador.prep_alto_puntaje()
        marcador.prep_nivel()
        marcador.prep_naves()

        #vacia la lista de aliens y balas
        aliens.empty()
        balas.empty()

        #crea una nueva flota y centra la nave
        crear_flota(ai_configuraciones, pantalla, nave, aliens)
        nave.centrar_nave()

def actualizar_pantalla(ai_configuraciones, pantalla, estadisticas, marcador, nave, aliens, balas, play_button):
    """Actualiza las imagenes y pasa a la nueva pantalla"""

    # volver a dibujar la pantalla durante cada pasada por el bucle
    pantalla.fill(ai_configuraciones.bg_color)
    #vuelve a dibular todas las balas detras de la nave y de los extraterrestres
    for bala in balas.sprites():
        bala.draw_bala()
    nave.blitme()
    aliens.draw(pantalla)

    #dibuja la informacion de la puntuacion
    marcador.muestra_puntaje()

    #dibuja el boton de play si el juego esta inactivo
    if not estadisticas.game_active:
        play_button.draw_button()

    # hacer visible la pantalla
    pygame.display.flip()

def update_balas(ai_configuraciones, pantalla, estadisticas, marcador, nave, aliens, balas):
    """actualiza la posicion de las balas"""
    #actualiza las posiciones de las balas 
    balas.update()

    # deshace las balas que han desaparecido
    for bala in balas.copy():
        if bala.rect.bottom <= 0:
            balas.remove(bala)
    
    check_bala_alien_collisions(ai_configuraciones, pantalla, estadisticas, marcador, nave, aliens, balas)
   
def check_bala_alien_collisions(ai_configuraciones, pantalla, estadisticas, marcador, nave, aliens, balas):
    """responde a las colisiones entre aliens y balas"""
    #elimina balas y los aliens que hayan chocado
    collisions = pygame.sprite.groupcollide(balas, aliens, True, True)
    
    if collisions: 
        for aliens in collisions.values():
            estadisticas.puntaje += ai_configuraciones.puntos_alien * len(aliens)
            marcador.prep_puntaje()
        verificar_alto_puntaje(estadisticas, marcador)

    if len(aliens) == 0:
        #destruye las balas existentes y crea una nueva flota
        balas.empty()
        ai_configuraciones.aumentar_velocidad()

        #incrementa el nivel
        estadisticas.nivel += 1
        marcador.prep_nivel()

        crear_flota(ai_configuraciones, pantalla, nave, aliens)

def verificar_alto_puntaje(estadisticas, marcador):
    """verifica si existe un puntaje mas alto"""
    if estadisticas.puntaje > estadisticas.alto_puntaje:
        estadisticas.alto_puntaje = estadisticas.puntaje
        marcador.prep_alto_puntaje()
    
def fuego_bala(ai_configuraciones, pantalla, nave, balas):
    """dispara una bala si aun no ha alcanzado el limite"""
    #crea una nueva bala y agrega al grupo de balas
    if len(balas) < ai_configuraciones.balas_allowed:
        nueva_bala = Bala(ai_configuraciones, pantalla, nave)
        balas.add(nueva_bala)

def get_number_aliens_x(ai_configuraciones, alien_width):
    """determina el numero de alienigenas que caben en una fila"""
    available_space_x = ai_configuraciones.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_configuraciones, nave_height, alien_height):
    """determina el numero de filas de aliens que se ajustan en la pantalla"""
    available_space_y = (ai_configuraciones.screen_height - (3 * alien_height) - nave_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def crear_alien(ai_configuraciones, pantalla, aliens, alien_number, row_number):
    """crea un alien y lo coloca en una fila"""
    alien = Alien(ai_configuraciones, pantalla)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
def crear_flota(ai_configuraciones, pantalla, nave, aliens):
    """crea una flota completa de alienigenas"""
    #crea un alien y encuentra el numero de aliens seguidos
    #el espacion entre cada alien es igual a un ancho del alien
    alien = Alien(ai_configuraciones, pantalla)
    number_aliens_x = get_number_aliens_x(ai_configuraciones, alien.rect.width)
    number_rows = get_number_rows(ai_configuraciones, nave.rect.height, alien.rect.height)
    
    # crea la flota de aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            crear_alien(ai_configuraciones, pantalla, aliens, alien_number, row_number)

def check_fleet_edges(ai_configuraciones, aliens):
    """responde de forma apropiada si algun alien ha llegado a un borde"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_configuraciones, aliens)
            break

def change_fleet_direction(ai_configuraciones, aliens):
    """desciende toda la flota y cambia la direccion de la flota"""
    for alien in aliens.sprites():
        alien.rect.y += ai_configuraciones.fleet_drop_speed
    ai_configuraciones.fleet_direction *= -1

def nave_golpeada(ai_configuraciones, estadisticas, pantalla, marcador, nave, aliens, balas):
    """responde a una nave siendo golpeada por un alien"""

    if estadisticas.naves_restantes > 0:
        #disminuye naves_restantes
        estadisticas.naves_restantes -= 1

        #actualiza el marcador
        marcador.prep_naves()

        #vacia la lista de aliens y balas
        aliens.empty()
        balas.empty()

        #crea una nueva flota y centra la nave
        crear_flota(ai_configuraciones, pantalla, nave, aliens)
        nave.centrar_nave()

        #pausa
        sleep(0.5)

    else:
        estadisticas.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_configuraciones, estadisticas, pantalla, marcador, nave, aliens, balas):
    """comprueba si algun alien ha llegado al final de la pantalla"""
    pantalla_rect = pantalla.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= pantalla_rect.bottom:
            #trata esto de la misma forma que si la nave fuera golpeada
            nave_golpeada(ai_configuraciones, estadisticas, pantalla, marcador, nave, aliens, balas)
            break

def update_aliens(ai_configuraciones, estadisticas, pantalla, marcador, nave, aliens, balas):
    """comprueba si la flota esta al borde y actualiza las posiciones de todos los aliens de la flota"""
    check_fleet_edges(ai_configuraciones, aliens)
    aliens.update()

    #busca colisiones de alien-nave
    if pygame.sprite.spritecollideany(nave, aliens):
        nave_golpeada(ai_configuraciones, estadisticas, pantalla, marcador, nave, aliens, balas)
    
    #busca aliens que golpean la parte inferior de la pantalla
    check_aliens_bottom(ai_configuraciones, estadisticas, pantalla, marcador, nave, aliens, balas)
