import pygame, sys, os

pygame.init() 

ANCHO, ALTO = 1366, 768
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

pantalla_completa = False
ESCALA = 3

ruta = os.path.join(os.path.dirname(__file__), "buho.png")
sprite_sheet = pygame.image.load(ruta).convert_alpha()

def obtener_frame(x, y, w, h):
    frame = pygame.Surface((w, h), pygame.SRCALPHA)
    frame.blit(sprite_sheet, (0, 0), (x, y, w, h))
    return frame

class Buho:
    def __init__(self):
        self.rect = pygame.Rect(225, 500, 24*ESCALA, 32*ESCALA)
        self.vel_y = 0
        self.en_suelo = False
        self.mirando_derecha = True

        self.frames = {
            "caminar": [pygame.transform.scale(obtener_frame(i*24,0,24,32),(24*ESCALA,32*ESCALA)) for i in range(4)],
            "reposo": [pygame.transform.scale(obtener_frame(96,0,24,32),(24*ESCALA,32*ESCALA)),
                       pygame.transform.scale(obtener_frame(120,0,24,32),(24*ESCALA,32*ESCALA))],
            "w": pygame.transform.scale(obtener_frame(144,0,24,32),(24*ESCALA,32*ESCALA)), 
            "saltar": pygame.transform.scale(obtener_frame(168,0,24,32),(24*ESCALA,32*ESCALA)), 
            "agacharse_intermedio": pygame.transform.scale(obtener_frame(192,0,24,32),(24*ESCALA,32*ESCALA)), 
            "agachado": pygame.transform.scale(obtener_frame(216,0,24,32),(24*ESCALA,32*ESCALA))  
        }

        self.frame_actual = 0
        self.tiempo_animacion = 0
        self.estado = "reposo"
        self.agachado = False 

    def actualizar(self, teclas):
        moviendo = False
        self.estado = "reposo"

        if teclas[pygame.K_a]:
            self.rect.x -= 5
            moviendo = True
            self.mirando_derecha = False
        if teclas[pygame.K_d]:
            self.rect.x += 5
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

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > pantalla.get_width(): self.rect.right = pantalla.get_width()

        self.vel_y += 0.8
        self.rect.y += self.vel_y

        self.tiempo_animacion += 1
        if self.tiempo_animacion > 10:
            self.frame_actual = (self.frame_actual + 1) % 2
            self.tiempo_animacion = 0

    def saltar(self):
        if self.en_suelo:
            self.vel_y = -15
            self.en_suelo = False

    def dibujar(self, pantalla):
        if self.estado == "caminar":
            imagen = self.frames["caminar"][self.frame_actual % len(self.frames["caminar"])]
        elif self.estado == "reposo":
            imagen = self.frames["reposo"][self.frame_actual % len(self.frames["reposo"])]
        elif self.estado == "w":
            imagen = self.frames["w"]
        elif self.estado == "saltar":
            imagen = self.frames["saltar"]
        elif self.estado == "agacharse_intermedio":
            imagen = self.frames["agacharse_intermedio"]
        elif self.estado == "agachado":
            imagen = self.frames["agachado"]

        if not self.mirando_derecha:
            imagen = pygame.transform.flip(imagen, True, False)

        offset_y = 24
        pantalla.blit(imagen, (self.rect.x, self.rect.y + offset_y))

def fase1():
    global pantalla, pantalla_completa

    jugador = Buho()

    while True:
        suelo = pygame.Rect(
            0,
            pantalla.get_height() - 118,
            pantalla.get_width(),
            200
        )

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jugador.saltar()
                if evento.key == pygame.K_F11:
                    pantalla_completa = not pantalla_completa
                    if pantalla_completa:
                        info = pygame.display.Info()
                        pantalla = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
                    else:
                        pantalla = pygame.display.set_mode((ANCHO, ALTO))

        teclas = pygame.key.get_pressed()
        jugador.actualizar(teclas)
        jugador.en_suelo = False

        if jugador.rect.colliderect(suelo) and jugador.vel_y > 0:
            jugador.rect.bottom = suelo.top
            jugador.vel_y = 0
            jugador.en_suelo = True

        pantalla.fill((0, 0, 50))
        pygame.draw.rect(pantalla, (20, 100, 34), suelo)

        jugador.dibujar(pantalla)

        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    fase1()