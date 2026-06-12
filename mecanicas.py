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
        
        # --- NUEVA FUNCIONALIDAD: CARGA DE SALTO ---
        self.potencia_extra = 0 

    def actualizar(self, teclas):
        self.vel_x = 0
        moviendo = False
        self.estado = "reposo"

        # Movimiento horizontal
        if teclas[pygame.K_a]:
            self.vel_x = -5
            moviendo = True
            self.mirando_derecha = False
        if teclas[pygame.K_d]:
            self.vel_x = 5
            moviendo = True
            self.mirando_derecha = True

        # Lógica de agacharse y carga de potencia
        if teclas[pygame.K_s]:
            self.agachado = True
            # Acumulamos potencia extra mientras mantiene S (máximo 5)
            if self.potencia_extra < 5:
                self.potencia_extra += 0.1
            self.estado = "agachado"
        else:
            self.agachado = False
            # Si suelta la S, la potencia se disipa poco a poco
            if self.potencia_extra > 0:
                self.potencia_extra -= 0.2
            
            # Si presiona W mientras no está agachado
            if teclas[pygame.K_w]:
                self.estado = "w"

        # Estados de animación
        if self.vel_y != 0:
            self.estado = "saltar"
        elif moviendo and self.vel_y == 0 and not teclas[pygame.K_s]:
            self.estado = "caminar"

        # Gravedad
        self.vel_y += 0.8

        # Animación
        self.tiempo_animacion += 1
        if self.tiempo_animacion > 10:
            self.frame_actual = (self.frame_actual + 1) % 2
            self.tiempo_animacion = 0

    def saltar(self):
        if self.en_suelo:
            # Salto base (-15) + la potencia extra acumulada
            self.vel_y = -15 - self.potencia_extra
            self.potencia_extra = 0 # Reiniciamos la carga tras saltar
            self.en_suelo = False