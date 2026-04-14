import pygame

def obtener_muros(nivel, ancho, alto):
    muros = []
    if nivel == 1:
        muros.append(pygame.Rect(ancho - 350, alto - 200, 80, 120))
        muros.append(pygame.Rect(ancho - 150, alto - 350, 100, 250))
    return muros

def dibujar_nivel(pantalla, nivel, base_x, ancho, alto):
    suelo = pygame.Rect(base_x, alto - 118, ancho, 200)
    pygame.draw.rect(pantalla, (20,100,34), suelo)

    if nivel == 1:
        muro1 = pygame.Rect(base_x + ancho - 350, alto - 200, 80, 120)
        muro2 = pygame.Rect(base_x + ancho - 150, alto - 350, 100, 250)
        pygame.draw.rect(pantalla, (20,100,34), muro1)
        pygame.draw.rect(pantalla, (20,100,34), muro2)