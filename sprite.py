import pygame, os
from configuracion import ESCALA

def obtener_frame(sprite_sheet, x, y, w, h):
    frame = pygame.Surface((w, h), pygame.SRCALPHA)
    frame.blit(sprite_sheet, (0, 0), (x, y, w, h))
    return frame

def cargar_frames():
    ruta = os.path.join(os.path.dirname(__file__), "buho.png")
    sprite_sheet = pygame.image.load(ruta).convert_alpha()

    return {
        "caminar": [pygame.transform.scale(obtener_frame(sprite_sheet, i*24,0,24,32),(24*ESCALA,32*ESCALA)) for i in range(4)],
        "reposo": [pygame.transform.scale(obtener_frame(sprite_sheet,96,0,24,32),(24*ESCALA,32*ESCALA)),
                   pygame.transform.scale(obtener_frame(sprite_sheet,120,0,24,32),(24*ESCALA,32*ESCALA))],
        "w": pygame.transform.scale(obtener_frame(sprite_sheet,144,0,24,32),(24*ESCALA,32*ESCALA)), 
        "saltar": pygame.transform.scale(obtener_frame(sprite_sheet,168,0,24,32),(24*ESCALA,32*ESCALA)), 
        "agacharse_intermedio": pygame.transform.scale(obtener_frame(sprite_sheet,192,0,24,32),(24*ESCALA,32*ESCALA)), 
        "agachado": pygame.transform.scale(obtener_frame(sprite_sheet,216,0,24,32),(24*ESCALA,32*ESCALA))  
    }