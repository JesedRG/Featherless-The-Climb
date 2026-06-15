import pygame, sys, os
import tkinter as tk
from tkinter import ttk 
from configuracion import ANCHO, ALTO
from mecanicas import Buho
from nivel import Plataformas

BLANCO = (255, 255, 255)
VERDE_BOTON = (34, 177, 76)
COLOR_TEXTO = (50, 50, 50)
ROJO_BOTON = (200, 50, 50)
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

def iniciar_musica():
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    if not pygame.mixer.music.get_busy(): 
        try:
            pygame.mixer.music.load("musica_fondo.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
        except Exception as e:
            print(f"No se pudo cargar la música: {e}")

# ==========================================
# LA VENTANA DEL JUEGO (Pygame)
# ==========================================
# NOTA: Ahora recibe 'pantalla' como parámetro, ¡ya no la crea adentro!
def ejecutar_juego(pantalla):
    reloj = pygame.time.Clock()
    
    jugador = Buho()
    gestor_plataformas = Plataformas(ANCHO, ALTO)
    
    try:
        fondo_cielo = pygame.image.load("FOND-VERD.png").convert()
        fondo_cielo = pygame.transform.scale(fondo_cielo, (ANCHO, ALTO))
    except:
        fondo_cielo = pygame.Surface((ANCHO, ALTO))
        fondo_cielo.fill((135, 206, 235))

    fuente_titulo = pygame.font.SysFont("Arial", 64, bold=True)
    fuente_botones = pygame.font.SysFont("Arial", 32, bold=True)
    fuente_ui = pygame.font.SysFont("Arial", 28)
    
    boton_reintentar = pygame.Rect(ANCHO // 2 - 175, ALTO // 2 + 10, 350, 60)
    boton_menu = pygame.Rect(ANCHO // 2 - 175, ALTO // 2 + 90, 350, 60)
    
    cam_y = 0
    puntuacion = 0
    en_gameover = False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return 'SALIR'
            
            if en_gameover and evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if boton_reintentar.collidepoint(evento.pos):
                        return 'REINTENTAR'
                    elif boton_menu.collidepoint(evento.pos):
                        return 'MENU'

            if evento.type == pygame.KEYDOWN and not en_gameover:
                if evento.key == pygame.K_SPACE:
                    jugador.saltar()

        if not en_gameover:
            teclas = pygame.key.get_pressed()
            jugador.actualizar(teclas)
            
            jugador.rect.x += jugador.vel_x
            if jugador.rect.left < 0: jugador.rect.left = 0
            if jugador.rect.right > ANCHO: jugador.rect.right = ANCHO

            jugador.rect.y += jugador.vel_y
            jugador.en_suelo = False
            
            # Chequeo de colisiones con los muros
            for m in gestor_plataformas.muros:
                if jugador.rect.colliderect(m):
                    if jugador.vel_y > 0 and jugador.rect.bottom <= m.bottom + 15:
                        jugador.rect.bottom = m.top
                        jugador.vel_y = 0
                        jugador.en_suelo = True

            # Chequeo de recolección de las plumas (cuadritos)
            for pluma in gestor_plataformas.objetos_pluma[:]:
                if jugador.rect.colliderect(pluma):
                    gestor_plataformas.objetos_pluma.remove(pluma)

                    if jugador.plumas < 3:
                        jugador.plumas += 1

                    if jugador.sonido_pluma:
                        jugador.sonido_pluma.play()

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
            
            pantalla.blit(img, (jugador.rect.x, jugador.rect.y - cam_y + 25))
            
            texto_puntos = fuente_ui.render(f"Altura: {puntuacion}m", True, (255, 255, 255))
            pantalla.blit(texto_puntos, (20, 20))
            
            texto_plumas = fuente_ui.render(f"Plumas: {jugador.plumas}", True, (200, 150, 0))
            pantalla.blit(texto_plumas, (20, 55))
            
        else:
            texto_go = fuente_titulo.render("¡TE CAÍSTE!", True, (200, 40, 40))
            pantalla.blit(texto_go, (ANCHO//2 - texto_go.get_width()//2, ALTO//4))
            
            texto_puntos = fuente_botones.render(f"Llegaste a: {puntuacion}m", True, (255, 255, 255))
            pantalla.blit(texto_puntos, (ANCHO//2 - texto_puntos.get_width()//2, ALTO//2 - 50))
            
            pygame.draw.rect(pantalla, VERDE_BOTON, boton_reintentar, border_radius=15)
            texto_play = fuente_botones.render("INTENTAR DE NUEVO", True, BLANCO)
            pantalla.blit(texto_play, (boton_reintentar.centerx - texto_play.get_width()//2, boton_reintentar.centery - texto_play.get_height()//2))

            pygame.draw.rect(pantalla, ROJO_BOTON, boton_menu, border_radius=15)
            texto_menu = fuente_botones.render("VOLVER AL MENÚ", True, BLANCO)
            pantalla.blit(texto_menu, (boton_menu.centerx - texto_menu.get_width()//2, boton_menu.centery - texto_menu.get_height()//2))

        pygame.display.flip()
        reloj.tick(60)


# ==========================================
# CONTROLADOR PRINCIPAL Y TKINTER
# ==========================================
def fase1():
    pygame.init()
    iniciar_musica()

    raiz = tk.Tk()
    raiz.title("Featherless: Launcher")
    ancho_menu, alto_menu = 400, 450 
    pos_x = (raiz.winfo_screenwidth() // 2) - (ancho_menu // 2)
    pos_y = (raiz.winfo_screenheight() // 2) - (alto_menu // 2)
    raiz.geometry(f"{ancho_menu}x{alto_menu}+{pos_x}+{pos_y}")
    raiz.configure(bg="#1e1e2e")
    raiz.resizable(False, False)

    estado_app = {"accion": "NADA"}

    def cambiar_volumen(val):
        pygame.mixer.music.set_volume(float(val) / 100)

    def mostrar_opciones():
        frame_principal.pack_forget()
        frame_opciones.pack(fill="both", expand=True)

    def volver_al_menu():
        frame_opciones.pack_forget()
        frame_principal.pack(fill="both", expand=True)

    def presionar_jugar():
        estado_app["accion"] = "JUGAR"
        raiz.quit()

    def on_cerrar_ventana():
        estado_app["accion"] = "SALIR"
        raiz.quit()

    raiz.protocol("WM_DELETE_WINDOW", on_cerrar_ventana)

    frame_principal = tk.Frame(raiz, bg="#1e1e2e")
    frame_opciones = tk.Frame(raiz, bg="#1e1e2e")

    lbl_titulo = tk.Label(frame_principal, text="FEATHERLESS\nTHE CLIMB", font=("Arial", 24, "bold"), bg="#1e1e2e", fg="#cdd6f4")
    lbl_titulo.pack(pady=30)

    lbl_record = tk.Label(frame_principal, text="", font=("Arial", 14), bg="#1e1e2e", fg="#a6adc8")
    lbl_record.pack(pady=10)

    btn_jugar = tk.Button(frame_principal, text="JUGAR", font=("Arial", 14, "bold"), bg="#22b14c", fg="white", 
                          activebackground="#1b8a3b", activeforeground="white", width=15, height=2, 
                          bd=0, cursor="hand2", command=presionar_jugar)
    btn_jugar.pack(pady=15)

    btn_ir_opc = tk.Button(frame_principal, text="OPCIONES", font=("Arial", 12, "bold"), bg="#4c4f69", fg="white", 
                          activebackground="#313244", activeforeground="white", width=15, height=1, 
                          bd=0, cursor="hand2", command=mostrar_opciones)
    btn_ir_opc.pack(pady=10)

    lbl_titulo_opc = tk.Label(frame_opciones, text="OPCIONES", font=("Arial", 20, "bold"), bg="#1e1e2e", fg="#cdd6f4")
    lbl_titulo_opc.pack(pady=40)

    lbl_volumen = tk.Label(frame_opciones, text="Volumen de la Música:", font=("Arial", 12), bg="#1e1e2e", fg="#cdd6f4")
    lbl_volumen.pack(pady=(10, 5))
    
    slider_volumen = ttk.Scale(frame_opciones, from_=0, to=100, orient="horizontal", command=cambiar_volumen)
    slider_volumen.set(50) 
    slider_volumen.pack(padx=50, fill="x", pady=15)

    btn_volver = tk.Button(frame_opciones, text="VOLVER", font=("Arial", 12, "bold"), bg="#e06c75", fg="white", 
                          activebackground="#be5046", activeforeground="white", width=15, height=1, 
                          bd=0, cursor="hand2", command=volver_al_menu)
    btn_volver.pack(pady=40)

    frame_principal.pack(fill="both", expand=True)

    while True:
        lbl_record.config(text=f"Récord Actual: {obtener_mejor_puntuacion()}m")
        
        raiz.deiconify() 
        estado_app["accion"] = "NADA"
        raiz.mainloop()

        if estado_app["accion"] == "SALIR":
            break

        if estado_app["accion"] == "JUGAR":
            raiz.withdraw() 
            raiz.update() # Asegura que Tkinter se esconda completamente antes de arrancar Pygame
            
            pygame.display.init()
            pygame.font.init()
            pantalla = pygame.display.set_mode((ANCHO, ALTO))
            pygame.display.set_caption("Featherless: The Climb - ¡Jugando!")
            
            intentando = True
            while intentando:
                resultado = ejecutar_juego(pantalla)
                
                if resultado == 'MENU':
                    intentando = False
                elif resultado == 'SALIR':
                    estado_app["accion"] = "SALIR"
                    intentando = False

            pygame.display.quit() 
            
            if estado_app["accion"] == "SALIR":
                break

    raiz.destroy()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    fase1()