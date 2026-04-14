import pygame
from configuracion import ESCALA
from sprite import cargar_frames

class Buho:
    def __init__(self):
        self.rect = pygame.Rect(225, 500, 24*ESCALA, 32*ESCALA)
        self.vel_y = 0
        self.vel_x = 0
        self.en_suelo = False
        self.mirando_derecha = True

        self.frames = cargar_frames()

        self.frame_actual = 0
        self.tiempo_animacion = 0
        self.estado = "reposo"
        self.agachado = False 

    def actualizar(self, teclas):
        self.vel_x = 0
        moviendo = False
        self.estado = "reposo"

        if teclas[pygame.K_a]:
            self.vel_x = -5
            moviendo = True
            self.mirando_derecha = False
        if teclas[pygame.K_d]:
            self.vel_x = 5
            moviendo = True
            self.mirando_derecha = True

        if teclas[pygame.K_w]:
            self.estado = "w"

        if teclas[pygame.K_s]:
            if not self.agachado:
                self.estado = "agacharse_intermedio"
            else:
                self.estado = "agachado"
            self.agachado = True
        else:
            self.agachado = False

        if self.vel_y != 0:
            self.estado = "saltar"

        if moviendo and self.vel_y == 0 and not teclas[pygame.K_w] and not teclas[pygame.K_s]:
            self.estado = "caminar"

        self.vel_y += 0.8

        self.tiempo_animacion += 1
        if self.tiempo_animacion > 10:
            self.frame_actual = (self.frame_actual + 1) % 2
            self.tiempo_animacion = 0

    def saltar(self):
        if self.en_suelo:
            self.vel_y = -15
            self.en_suelo = False