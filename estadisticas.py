class Estadisticas():
    """siguimiento de las estadisticas de invasion alienigena"""
    def __init__(self, ai_configuraciones):
        """inicializa las estadisticas"""
        self.ai_configuraciones = ai_configuraciones
        self.reset_stats()

        #inicia invasion alienigena en un estado activo
        self.game_active = False

        #la puntuacion alta nunca debe restablecerse
        self.alto_puntaje = 0


    def reset_stats(self):
        """inicializa estadisticas que pueden cambiar durante el juego"""
        self.naves_restantes = self.ai_configuraciones.cantidad_naves
        self.puntaje = 0
        self.nivel = 1