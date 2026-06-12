import pygame, sys, os
import tkinter as tk
from tkinter import ttk 
from configuracion import ANCHO, ALTO
from mecanicas import Buho
from nivel import Plataformas


BLANCO = (255, 255, 255)
VERDE_BOTON = (34, 177, 76)
COLOR_TEXTO = (50, 50, 50)
ARCHIVO_PUNTUACION = "puntuacion.txt"


pygame.mixer.init()


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

def iniciar_musica():
    """Carga y reproduce la música de fondo en bucle infinito"""
    try:
        
        pygame.mixer.music.load("musica_fondo.mp3")
        pygame.mixer.music.play(-1) # -1 significa que se repetirá infinitamente la mussica
        pygame.mixer.music.set_volume(0.5) # Volumen inicial con 50%
    except Exception as e:
        print(f"No se pudo cargar la música: {e}")


# INTERFAZ 1: EL MENÚ EN TKINTER 

def mostrar_menu_tkinter():
    raiz = tk.Tk()
    raiz.title("Featherless: Launcher")
    
    ancho_menu, alto_menu = 400, 450 
    pantalla_ancho = raiz.winfo_screenwidth()
    pantalla_alto = raiz.winfo_screenheight()
    pos_x = (pantalla_ancho // 2) - (ancho_menu // 2)
    pos_y = (pantalla_alto // 2) - (alto_menu // 2)
    raiz.geometry(f"{ancho_menu}x{alto_menu}+{pos_x}+{pos_y}")
    raiz.configure(bg="#1e1e2e")
    raiz.resizable(False, False)

    proceder_al_juego = {"activo": False}

    def presionar_jugar():
        proceder_al_juego["activo"] = True
        raiz.destroy()

    def cambiar_volumen(val):
        """Esta función se ejecuta cada vez que mueves el deslizador"""
        volumen = float(val) / 100 # Tkinter da valores de 0 a 100, Pygame usa de 0.0 a 1.0
        pygame.mixer.music.set_volume(volumen)

    # Título
    lbl_titulo = tk.Label(raiz, text="FEATHERLESS\nTHE CLIMB", font=("Arial", 24, "bold"), bg="#1e1e2e", fg="#cdd6f4")
    lbl_titulo.pack(pady=20)

    # Récord
    record = obtener_mejor_puntuacion()
    lbl_record = tk.Label(raiz, text=f"Récord Actual: {record}m", font=("Arial", 14), bg="#1e1e2e", fg="#a6adc8")
    lbl_record.pack(pady=5)

    # volumen
    lbl_volumen = tk.Label(raiz, text="Volumen de la Música:", font=("Arial", 12), bg="#1e1e2e", fg="#cdd6f4")
    lbl_volumen.pack(pady=(20, 5))

    # Deslizador del volumen
    volumen_actual = pygame.mixer.music.get_volume() * 100
    slider_volumen = ttk.Scale(raiz, from_=0, to=100, orient="horizontal", command=cambiar_volumen)
    slider_volumen.set(volumen_actual) # Lo colocamos en la posición actual (50%)
    slider_volumen.pack(padx=50, fill="x", pady=5)

    # Botón Jugar
    btn_jugar = tk.Button(raiz, text="JUGAR", font=("Arial", 14, "bold"), bg="#22b14c", fg="white", 
                          activebackground="#1b8a3b", activeforeground="white", width=15, height=2, 
                          bd=0, cursor="hand2", command=presionar_jugar)
    btn_jugar.pack(pady=30)

    raiz.mainloop()
    return proceder_al_juego["activo"]


# INTERFAZ 2: LA VENTANA DEL JUEGO (Pygame)

def ejecutar_juego():
    
    pygame.display.init()
    pygame.font.init()
    
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Featherless: The Climb - ¡Jugando!")
    reloj = pygame.time.Clock()
    
    jugador = Buho()
    gestor_plataformas = Plataformas(ANCHO, ALTO)
    
    try:
        fondo_cielo = pygame.image.load("FOND-VERD.png").convert()
        fondo_cielo = pygame.transform.scale(fondo_cielo, (ANCHO, ALTO))
    except:
        fondo_cielo = pygame.Surface((ANCHO, ALTO))
        fondo_cielo.fill((135, 206, 235))

    boton_reintentar = pygame.Rect(ANCHO // 2 - 175, ALTO // 2 + 40, 350, 80)
    fuente_titulo = pygame.font.SysFont("Arial", 64, bold=True)
    fuente_botones = pygame.font.SysFont("Arial", 36, bold=True)
    fuente_ui = pygame.font.SysFont("Arial", 28)
    
    cam_y = 0
    puntuacion = 0
    en_gameover = False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN and en_gameover:
                if evento.button == 1 and boton_reintentar.collidepoint(evento.pos):
                    return True 
            
            if evento.type == pygame.KEYDOWN and not en_gameover:
                if evento.key == pygame.K_SPACE:
                    jugador.saltar()

        # Logica de el juego
        if not en_gameover:
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
                en_gameover = True
                guardar_puntuacion(puntuacion)

        
        pantalla.blit(fondo_cielo, (0, 0)) 

        if not en_gameover:
            gestor_plataformas.dibujar(pantalla, cam_y)
            
            img = jugador.frames[jugador.estado]
            if isinstance(img, list):
                img = img[jugador.frame_actual % len(img)]
            if not jugador.mirando_derecha:
                img = pygame.transform.flip(img, True, False)
            
            pantalla.blit(img, (jugador.rect.x, jugador.rect.y - cam_y + 30))
            
            texto_puntos = fuente_ui.render(f"Altura: {puntuacion}m", True, (0, 0, 0))
            pantalla.blit(texto_puntos, (20, 20))
        else:
            texto_go = fuente_titulo.render("¡TE CAISTE!", True, (200, 40, 40))
            pantalla.blit(texto_go, (ANCHO//2 - texto_go.get_width()//2, ALTO//4))
            
            texto_puntos = fuente_botones.render(f"Llegaste a: {puntuacion}m", True, COLOR_TEXTO)
            pantalla.blit(texto_puntos, (ANCHO//2 - texto_puntos.get_width()//2, ALTO//2 - 40))
            
            pygame.draw.rect(pantalla, VERDE_BOTON, boton_reintentar, border_radius=15)
            texto_play = fuente_botones.render("INTENTAR DE NUEVO", True, BLANCO)
            pantalla.blit(texto_play, (boton_reintentar.centerx - texto_play.get_width()//2, boton_reintentar.centery - texto_play.get_height()//2))

        pygame.display.flip()
        reloj.tick(60)


# CONTROLADOR PRINCIPAL

def fase1():
    
    iniciar_musica()
    
    # mostramos el menu con el deslizador del volumen
    if mostrar_menu_tkinter():
        jugando = True
        while jugando:
            jugando = ejecutar_juego()

if __name__ == "__main__":
    fase1()