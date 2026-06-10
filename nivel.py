import pygame

def obtener_muros(nivel, ancho, alto):
    muros = []
    if nivel == 1:
        muros.append(pygame.Rect(ancho - 350, alto - 200, 80, 120))
        muros.append(pygame.Rect(ancho - 150, alto - 350, 100, 250))


        ancho_plataforma = 200
        x_centrada = (ancho // 2) - (ancho_plataforma // 2)
        
        muros.append(pygame.Rect(x_centrada, alto - 210, ancho_plataforma, 30))
        
        muros.append(pygame.Rect(265, alto - 320, 150, 30))

        muros.append(pygame.Rect(ancho - 365, alto - 250, 150, 30))

        muros.append(pygame.Rect(x_centrada, alto - 410, ancho_plataforma, 30))



    return muros

def dibujar_nivel(pantalla, nivel, base_x, ancho, alto):
    suelo = pygame.Rect(base_x, alto - 118, ancho, 200)
    pygame.draw.rect(pantalla, (20,100,34), suelo)

    if nivel == 1:
        muro1 = pygame.Rect(base_x + ancho - 350, alto - 200, 80, 120)
        muro2 = pygame.Rect(base_x + ancho - 150, alto - 350, 100, 250)
        pygame.draw.rect(pantalla, (20,100,34), muro1)
        pygame.draw.rect(pantalla, (20,100,34), muro2)

        ancho_plataforma = 200
        x_centrada = (ancho // 2) - (ancho_plataforma // 2)

        plat_flotante = pygame.Rect(base_x + x_centrada, alto - 210, ancho_plataforma, 30)
        pygame.draw.rect(pantalla, (101,65,33), plat_flotante)

        pygame.draw.rect(pantalla, (101,65,33), pygame.Rect(base_x + 265, alto - 320, 150, 30))

        pygame.draw.rect(pantalla, (101,65,33), pygame.Rect(base_x + ancho - 365, alto - 250, 150, 30))

        plat_flotante = pygame.Rect(base_x + x_centrada, alto - 410, ancho_plataforma, 30)
        pygame.draw.rect(pantalla, (101,65,33), plat_flotante)

