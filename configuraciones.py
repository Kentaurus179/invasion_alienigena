class Configuraciones():
    """sirve para almacenar todas las configuraciones de Invasion alienigena"""

    def __init__(self):
        """inicializa las configuraciones del juego"""
        
        self.screen_width = 990
        self.screen_height = 690
        self.bg_color = (230, 230, 230)

        # configuraciones de la nave
        self.cantidad_naves = 3

        #configuraciones de balas
        self.bala_width = 3
        self.bala_height = 15
        self.bala_color = 60, 60, 60
        self.balas_allowed = 3

        #configuraciones de alien
        self.fleet_drop_speed = 10
        #que tan rapido se acelera el juego
        self.escala_aceleracion = 1.1
        #que tan rapido aumentan los valores de puntos por alien
        self.escala_puntaje = 1.5

        self.inicializa_configuraciones_dinamicas()

    def inicializa_configuraciones_dinamicas(self):
        """inicializa la configuracion que cambia a lo largo del juego"""
        self.factor_velocidad_nave = 1.5
        self.bala_factor_velocidad = 3
        self.alien_speed_factor = 1
         #fleet_direction, si es 1 representa a la derecha; si es -1 representa a la izquierda
        self.fleet_direction = 1
        #puntuacion
        self.puntos_alien = 50
    
    def aumentar_velocidad(self):
        """aumenta la configuracion de velocidad y los valores de puntos por aliens"""
        self.factor_velocidad_nave *= self.escala_aceleracion
        self.bala_factor_velocidad *= self.escala_aceleracion
        self.alien_speed_factor *= self.escala_aceleracion

        self.puntos_alien = int(self.puntos_alien * self.escala_puntaje)
