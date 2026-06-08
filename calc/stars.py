from settings import HEIGHT, WIDTH, STAR_NUMBER
import random

def generate_star_surface():
    from index import pygame
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) # make transparent surface so i can draw stars

    for i in range(STAR_NUMBER):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)

        luminosity = random.randint(200, 255)
        radius = random.randint(1, 3)
        pygame.draw.circle(surface, (luminosity, luminosity, luminosity), (x, y), radius)
    
    return surface
        