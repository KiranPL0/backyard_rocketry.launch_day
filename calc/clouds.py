import random
from settings import LOW_BAND, MEDIUM_BAND, HIGH_BAND, LOW_ALT_CLOUDS, MEDIUM_ALT_CLOUDS, HIGH_ALT_CLOUDS
from classes.cloud import Cloud
def generate_clouds(quantity):
    from index import pygame
    clouds = []
    for i in range(quantity):
        band = random.choice([LOW_BAND, MEDIUM_BAND, HIGH_BAND])
        if band == LOW_BAND:
            img = pygame.image.load(random.choice(LOW_ALT_CLOUDS)).convert_alpha()
            img = pygame.transform.scale_by(img, max(random.random()*2, 0.5))
            clouds.append(Cloud(img, LOW_BAND))
        elif band == MEDIUM_BAND:
            img = pygame.image.load(random.choice(MEDIUM_ALT_CLOUDS)).convert_alpha()
            img = pygame.transform.scale_by(img, max(random.random()*2, 0.5))
            clouds.append(Cloud(img, MEDIUM_BAND))
        else:
            img = pygame.image.load(random.choice(HIGH_ALT_CLOUDS)).convert_alpha()
            img = pygame.transform.scale_by(img, max(random.random()*2, 0.5))
            clouds.append(Cloud(img, HIGH_BAND))
    return clouds

def draw_clouds(clouds, screen, camera):
    for cloud in clouds:
        cloud.draw(screen, camera)