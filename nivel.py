import pygame
import random

class Plataformas:
    def __init__(self,ancho,alto):
        self.ancho = ancho
        self.alto = alto
        self.muros = []
        #suelo del inicio
        self.suelo = pygame.Rect(0, alto - 118, ancho, 200)
        self.generar_iniciales()

    def generar_iniciales(self):
        self.muros.append(self.suelo)
        y = self.alto - 250
        while y > -self.alto:
            self.generar_fila(y)
            y -= random.randint(120, 180)
            
    def generar_fila(self,y):
        ancho_plataform = random.randint(100, 250)
        x = random.randint(0, self.ancho - ancho_plataform)
        self.muros.append(pygame.Rect(x, y, ancho_plataform, 30))
        
    def actualizar(self, cam_y):
        # Limpiar plataformas que ya quedaron muy abajo
        self.muros = [m for m in self.muros if m.y - cam_y < self.alto + 200]
        
        # Genera nuevas plataformas arriba si el jugador va subiendo
        if self.muros:
            min_y = min(m.y for m in self.muros)
            if min_y - cam_y > -self.alto:
                self.generar_fila(min_y - random.randint(120, 180))

    def dibujar(self, pantalla, cam_y):
        for m in self.muros:
            if m == self.suelo:
                pygame.draw.rect(pantalla, (34, 139, 34), (m.x, m.y - cam_y, m.width, m.height))
            else:
                pygame.draw.rect(pantalla, (101, 65, 33), (m.x, m.y - cam_y, m.width, m.height))
                pygame.draw.rect(pantalla, (139, 90, 43), (m.x, m.y - cam_y, m.width, 5))
