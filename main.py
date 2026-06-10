import pygame, sys
from configuracion import ANCHO, ALTO
from mecanicas import Buho
from nivel import obtener_muros, dibujar_nivel

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()


BLANCO = (255, 255, 255)
VERDE_BOTON = (34, 177, 76)
SOMBRA = (20, 80, 40)


MENU = 0
JUGANDO = 1

def fase1():
    estado_actual = MENU
    jugador = Buho()

    
    fondo_original = pygame.image.load("FOND-VERD.jpg").convert()
    fondo = pygame.transform.scale(fondo_original, (ANCHO, ALTO))

    
    boton_play = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 - 50, 200, 100)
    fuente = pygame.font.SysFont("Arial", 40)
    texto_play = fuente.render("PLAY", True, BLANCO)

    
    transicion = False
    direccion = 0
    offset_x = 0
    vel_transicion = 20
    pantalla_actual = 1
    pantalla_destino = 0

    
    while True:
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if estado_actual == MENU:
                    if boton_play.collidepoint(evento.pos):
                        estado_actual = JUGANDO
            
            if evento.type == pygame.KEYDOWN:
                if estado_actual == JUGANDO and evento.key == pygame.K_SPACE:
                    jugador.saltar()

        
        cam_x = 0 
        
        if estado_actual == JUGANDO:
            teclas = pygame.key.get_pressed()
            muros = obtener_muros(pantalla_actual, ANCHO, ALTO)

            if not transicion:
                jugador.actualizar(teclas)
                jugador.rect.x += jugador.vel_x

                for m in muros:
                    if jugador.rect.colliderect(m):
                        if jugador.vel_x > 0: jugador.rect.right = m.left
                        elif jugador.vel_x < 0: jugador.rect.left = m.right

                jugador.rect.y += jugador.vel_y
                jugador.en_suelo = False
                suelo_y = ALTO - 118

                if jugador.rect.bottom >= suelo_y:
                    jugador.rect.bottom = suelo_y
                    jugador.vel_y = 0
                    jugador.en_suelo = True

                for m in muros:
                    if jugador.rect.colliderect(m):
                        if jugador.vel_y > 0:
                            jugador.rect.bottom = m.top
                            jugador.vel_y = 0
                            jugador.en_suelo = True
                        elif jugador.vel_y < 0:
                            jugador.rect.top = m.bottom
                            jugador.vel_y = 0

                
                if jugador.rect.right >= ANCHO:
                    transicion = True
                    direccion = 1
                    pantalla_destino = pantalla_actual + 1
                elif jugador.rect.left <= 0:
                    transicion = True
                    direccion = -1
                    pantalla_destino = pantalla_actual - 1

            if transicion:
                offset_x += vel_transicion
                cam_x = offset_x * direccion
                if offset_x >= ANCHO:
                    transicion = False
                    offset_x = 0
                    pantalla_actual = pantalla_destino
                    if direccion == 1: jugador.rect.left = 10
                    else: jugador.rect.right = ANCHO - 10

       
        pantalla.blit(fondo, (0, 0)) 

        if estado_actual == MENU:
            pygame.draw.rect(pantalla, VERDE_BOTON, boton_play, border_radius=12)
            pantalla.blit(texto_play, (boton_play.x + 55, boton_play.y + 25))
        
        elif estado_actual == JUGANDO:
            niveles = [pantalla_actual, pantalla_destino] if transicion else [pantalla_actual, pantalla_actual]
            for i, n in enumerate(niveles):
                base_x = i * ANCHO - cam_x if transicion else 0
                dibujar_nivel(pantalla, n, base_x, ANCHO, ALTO)

            
            img = jugador.frames[jugador.estado]
            if isinstance(img, list):
                img = img[jugador.frame_actual % len(img)]
            if not jugador.mirando_derecha:
                img = pygame.transform.flip(img, True, False)
            
            pantalla.blit(img, (jugador.rect.x - cam_x, jugador.rect.y))

        pygame.display.flip()
        reloj.tick(60)
        pass
if __name__ == "__main__":
    fase1()