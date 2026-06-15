import pygame
from configuracion import ESCALA
from sprite import cargar_frames

class Buho:
    def __init__(self):
        self.rect = pygame.Rect(225, 500, 50, 32 * ESCALA)

        self.vel_y = 0
        self.vel_x = 0
        self.en_suelo = False
        self.mirando_derecha = True

        self.frames = cargar_frames()

        self.frame_actual = 0
        self.tiempo_animacion = 0

        self.estado = "reposo"
        self.agachado = False

        self.potencia_extra = 0
        self.plumas = 0

        self.tiempo_agachado = 0

        # 🎧 SONIDO SALTO
        try:
            self.sonido_salto = pygame.mixer.Sound("salto.wav")
            self.sonido_salto.set_volume(0.5)
        except:
            self.sonido_salto = None

        # 🎧 SONIDO PLUMA
        try:
            self.sonido_pluma = pygame.mixer.Sound("pluma.wav")
            self.sonido_pluma.set_volume(0.5)
        except:
            self.sonido_pluma = None

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

        # Agachado y carga de salto
        if teclas[pygame.K_s]:
            self.agachado = True
            self.tiempo_agachado += 1

            if self.potencia_extra < 5:
                self.potencia_extra += 0.1

            if self.tiempo_agachado < 15:
                self.estado = "agacharse_intermedio"

            elif self.tiempo_agachado < 30:
                self.estado = "agachado"

            else:
                self.estado = "cargado"

        else:
            self.agachado = False
            self.tiempo_agachado = 0

            if self.potencia_extra > 0:
                self.potencia_extra -= 0.2

            if teclas[pygame.K_w]:
                self.estado = "w"

        # Salto
        if self.vel_y != 0:
            self.estado = "saltar"

        elif moviendo and not teclas[pygame.K_s]:
            self.estado = "caminar"

        # Gravedad
        self.vel_y += 0.8

        # Animación
        self.tiempo_animacion += 1

        if self.tiempo_animacion > 10:
            self.frame_actual += 1
            self.tiempo_animacion = 0

            estado_actual = self.frames.get(self.estado)

            if isinstance(estado_actual, list):
                self.frame_actual %= len(estado_actual)
            else:
                self.frame_actual = 0

    def saltar(self):
        # Salto normal
        if self.en_suelo:

            if self.sonido_salto:
                self.sonido_salto.play()

            self.vel_y = -15 - self.potencia_extra
            self.potencia_extra = 0
            self.en_suelo = False
            self.tiempo_agachado = 0

        # Doble salto
        elif self.plumas > 0:

            if self.sonido_salto:
                self.sonido_salto.play()

            self.vel_y = -15
            self.plumas -= 1
            self.potencia_extra = 0
            self.tiempo_agachado = 0