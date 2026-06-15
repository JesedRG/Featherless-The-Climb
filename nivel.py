import pygame
import random

class Plataformas:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.muros = []
        self.suelo = pygame.Rect(0, alto - 118, ancho, 200)
        self.objetos_pluma = [] 
        
        try:
            img_suelo_orig = pygame.image.load("suelo.jpg").convert_alpha()
            self.img_suelo = pygame.transform.scale(img_suelo_orig, (200, 200))
        except Exception as e:
            print(f"Error cargando suelo.png: {e}")
            self.img_suelo = None

        try:
            self.img_rama = pygame.image.load("rama.png").convert_alpha()
        except Exception as e:
            print(f"Error cargando rama.png: {e}")
            self.img_rama = None
            
        try:
            self.img_pluma = pygame.image.load("pluma.png").convert_alpha()
            self.img_pluma = pygame.transform.scale(self.img_pluma, (48, 48))
        except Exception as e:
            print(f"Error cargando pluma.png: {e}")
            self.img_pluma = None

        self.generar_iniciales()

    def generar_iniciales(self):
        self.muros.append(self.suelo)
        y = self.alto - 250
        while y > -self.alto:
            self.generar_fila(y)
            y -= random.randint(50, 80) 
            
    def actualizar(self, cam_y):
        self.muros = [m for m in self.muros if m.y - cam_y < self.alto + 200]
        # Limpiamos los objetos que ya pasaron
        self.objetos_pluma = [p for p in self.objetos_pluma if p.y - cam_y < self.alto + 200]
        
        if self.muros:
            min_y = min(m.y for m in self.muros)
            if min_y - cam_y > -self.alto:
                self.generar_fila(min_y - random.randint(50, 80))

    def generar_fila(self, y):
        ancho_plataform = 100
        margen = 25
        x = random.randint(margen, self.ancho - ancho_plataform - margen)
        plataforma = pygame.Rect(x, y, ancho_plataform, 30)
        self.muros.append(plataforma)

        if random.random() < 0.20:
            tam_pluma = 20
            px = x + (ancho_plataform // 2) - (tam_pluma // 2)
            py = y - tam_pluma - 10
            self.objetos_pluma.append(pygame.Rect(px, py, tam_pluma, tam_pluma))

    def dibujar(self, pantalla, cam_y):
        for m in self.muros:
            if m == self.suelo:
                if self.img_suelo:
                    for x in range(m.x, m.x + m.width, self.img_suelo.get_width()):
                        pantalla.blit(self.img_suelo, (x, m.y - cam_y))
                else:
                    pygame.draw.rect(pantalla, (34, 139, 34), (m.x, m.y - cam_y, m.width, m.height))
            else:
                if self.img_rama:
                    es_izq = (m.x + m.width // 2) < (self.ancho // 2)
                    rama = self.img_rama if es_izq else pygame.transform.flip(self.img_rama, True, False)
                    pantalla.blit(rama, (m.x, m.y - cam_y))
                else:
                    pygame.draw.rect(pantalla, (255, 165, 0), (m.x, m.y - cam_y, m.width, m.height))
        
        # Dibujamos las plumas
        # Dibujamos las plumas
        for p in self.objetos_pluma:
            if self.img_pluma:
                pantalla.blit(self.img_pluma, (p.x, p.y - cam_y))
            else:
                pygame.draw.rect(pantalla, (255, 215, 25), (p.x, p.y - cam_y, p.width, p.height))