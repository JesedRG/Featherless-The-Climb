import pygame, sys, os
from configuracion import ANCHO, ALTO
from mecanicas import Buho
from nivel import Plataformas

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

BLANCO = (255, 255, 255)
VERDE_BOTON = (34, 177, 76)
COLOR_TEXTO = (50, 50, 50)

MENU = 0
JUGANDO = 1
GAMEOVER = 2

ARCHIVO_PUNTUACION = "puntuacion.txt"

def obtener_mejor_puntuacion():
    if os.path.exists(ARCHIVO_PUNTUACION):
        with open(ARCHIVO_PUNTUACION, "r") as f:
            try: return int(f.read())
            except: return 0
    return 0

def guardar_puntuacion(puntos):
    mejor = obtener_mejor_puntuacion()
    if puntos > mejor:
        with open(ARCHIVO_PUNTUACION, "w") as f:
            f.write(str(puntos))

def fase1():
    estado_actual = MENU
    jugador = Buho()
    gestor_plataformas = Plataformas(ANCHO, ALTO)
    
    try:
        fondo_cielo = pygame.image.load("FOND-VERD.png").convert()
        fondo_cielo = pygame.transform.scale(fondo_cielo, (ANCHO, ALTO))
    except:
        fondo_cielo = pygame.Surface((ANCHO, ALTO))
        fondo_cielo.fill((135, 206, 235))

    boton_jugar = pygame.Rect(ANCHO // 2 - 125, ALTO // 2 - 40, 250, 80)
    fuente_titulo = pygame.font.SysFont("Arial", 64, bold=True)
    fuente_botones = pygame.font.SysFont("Arial", 36, bold=True)
    fuente_ui = pygame.font.SysFont("Arial", 28)
    
    cam_y = 0
    puntuacion = 0
    mejor_puntuacion = obtener_mejor_puntuacion()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if estado_actual in [MENU, GAMEOVER]:
                    if boton_jugar.collidepoint(evento.pos):
                        estado_actual = JUGANDO
                        jugador = Buho()
                        gestor_plataformas = Plataformas(ANCHO, ALTO)
                        cam_y = 0
                        puntuacion = 0
            
            if evento.type == pygame.KEYDOWN:
                if estado_actual == JUGANDO and evento.key == pygame.K_SPACE:
                    jugador.saltar()

        if estado_actual == JUGANDO:
            teclas = pygame.key.get_pressed()
            jugador.actualizar(teclas)
            
            jugador.rect.x += jugador.vel_x
            if jugador.rect.left < 0: jugador.rect.left = 0
            if jugador.rect.right > ANCHO: jugador.rect.right = ANCHO

            jugador.rect.y += jugador.vel_y
            jugador.en_suelo = False
            
            for m in gestor_plataformas.muros:
                if jugador.rect.colliderect(m):
                    if jugador.vel_y > 0 and jugador.rect.bottom <= m.bottom + 20:
                        jugador.rect.bottom = m.top
                        jugador.vel_y = 0
                        jugador.en_suelo = True

            umbral_camara = ALTO // 2
            if jugador.rect.y - cam_y < umbral_camara:
                cam_y = jugador.rect.y - umbral_camara
                
            altura_actual = int((500 - jugador.rect.y) / 10)
            if altura_actual > puntuacion:
                puntuacion = altura_actual

            gestor_plataformas.actualizar(cam_y)
            
            if jugador.rect.y - cam_y > ALTO:
                estado_actual = GAMEOVER
                guardar_puntuacion(puntuacion)
                mejor_puntuacion = obtener_mejor_puntuacion()

        pantalla.blit(fondo_cielo, (0, 0)) 

        if estado_actual == MENU:
            titulo = fuente_titulo.render("FEATHERLESS: THE CLIMB", True, (20, 20, 80))
            pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//4 - 50))
            pygame.draw.rect(pantalla, VERDE_BOTON, boton_jugar, border_radius=15)
            texto_play = fuente_botones.render("JUGAR", True, BLANCO)
            pantalla.blit(texto_play, (boton_jugar.centerx - texto_play.get_width()//2, boton_jugar.centery - texto_play.get_height()//2))
            record_texto = fuente_ui.render(f"Récord Actual: {mejor_puntuacion}", True, COLOR_TEXTO)
            pantalla.blit(record_texto, (ANCHO//2 - record_texto.get_width()//2, ALTO - 100))

        elif estado_actual == JUGANDO:
            gestor_plataformas.dibujar(pantalla, cam_y)
            
            img = jugador.frames[jugador.estado]
            if isinstance(img, list):
                img = img[jugador.frame_actual % len(img)]
            if not jugador.mirando_derecha:
                img = pygame.transform.flip(img, True, False)
            
            # Ajuste visual de carga de salto
            offset_visual = 10 if jugador.agachado else 0
            pantalla.blit(img, (jugador.rect.x, jugador.rect.y - cam_y + 30)) #el último cambia la posición en vertical del personaje para acomodarlo con
            
            texto_puntos = fuente_ui.render(f"Altura: {puntuacion}m", True, (0, 0, 0))
            pantalla.blit(texto_puntos, (20, 20))

        elif estado_actual == GAMEOVER:
            texto_go = fuente_titulo.render("¡TE CAISTE!", True, (200, 40, 40))
            pantalla.blit(texto_go, (ANCHO//2 - texto_go.get_width()//2, ALTO//4))
            texto_puntos = fuente_botones.render(f"Llegaste a: {puntuacion}m", True, COLOR_TEXTO)
            pantalla.blit(texto_puntos, (ANCHO//2 - texto_puntos.get_width()//2, ALTO//2 - 60))
            pygame.draw.rect(pantalla, VERDE_BOTON, boton_jugar, border_radius=15)
            texto_play = fuente_botones.render("INTENTAR DE NUEVO", True, BLANCO)
            pantalla.blit(texto_play, (boton_jugar.centerx - texto_play.get_width()//2, boton_jugar.centery - texto_play.get_height()//2))

        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    fase1()