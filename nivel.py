import pygame
import random

class Plataformas:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.muros = []
        self.suelo = pygame.Rect(0, alto - 118, ancho, 200)
        
        # --- CARGA DE IMÁGENES ---
        # Asegúrate de que los archivos estén en la carpeta raíz del proyecto
        try:
            img_suelo_orig = pygame.image.load("suelo.png").convert_alpha()
            self.img_suelo = pygame.transform.scale(img_suelo_orig, (200, 200))
        except Exception as e:
            print(f"Error cargando suelo.png: {e}")
            self.img_suelo = None

        try:
            self.img_rama = pygame.image.load("rama.png").convert_alpha()
        except Exception as e:
            print(f"Error cargando rama.png: {e}")
            self.img_rama = None
            
        self.generar_iniciales()

    def generar_iniciales(self):
        self.muros.append(self.suelo)
        y = self.alto - 250
        while y > -self.alto:
            self.generar_fila(y)
            y -= random.randint(70, 100) 
            
    def actualizar(self, cam_y):
        # 1. Eliminar plataformas que quedan muy abajo (fuera de pantalla)
        self.muros = [m for m in self.muros if m.y - cam_y < self.alto + 200]
        
        # 2. Generar nuevas arriba (limpiamos el código para que solo ocurra una vez)
        if self.muros:
            min_y = min(m.y for m in self.muros)
            if min_y - cam_y > -self.alto:
                self.generar_fila(min_y - random.randint(70, 100))

    def generar_fila(self, y):
        ancho_plataform = 128
        margen = 50
        x = random.randint(margen, self.ancho - ancho_plataform - margen)
        self.muros.append(pygame.Rect(x, y, ancho_plataform, 30))

    def dibujar(self, pantalla, cam_y):
        for m in self.muros:
            if m == self.suelo:
                if self.img_suelo:
                    for x in range(m.x, m.x + m.width, self.img_suelo.get_width()):
                        pantalla.blit(self.img_suelo, (x, m.y - cam_y))
                else:
                    pygame.draw.rect(pantalla, (34, 139, 34), (m.x, m.y - cam_y, m.width, m.height))
            else:
                # Dibujado de ramas
                if self.img_rama:
                    es_izq = (m.x + m.width // 2) < (self.ancho // 2)
                    rama = self.img_rama if es_izq else pygame.transform.flip(self.img_rama, True, False)
                    pantalla.blit(rama, (m.x, m.y - cam_y))
                else:
                    # Si ves este color naranja, es que 'rama.png' NO ESTÁ en la carpeta
                    pygame.draw.rect(pantalla, (255, 165, 0), (m.x, m.y - cam_y, m.width, m.height))