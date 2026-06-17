from settings import GROUND_TILE_WIDTH, WIDTH


def init_texture(pygame):
    global ground_texture
    ground_texture = pygame.image.load('./assets/textures/ground.png')
    ground_texture = pygame.transform.scale(ground_texture, (GROUND_TILE_WIDTH, GROUND_TILE_WIDTH))

def draw_ground(pygame, screen, camera):
    ground_surface = pygame.Surface((10000, GROUND_TILE_WIDTH*3))
    for i in range(0, 10000, GROUND_TILE_WIDTH):
        ground_surface.blit(ground_texture, (i, 0))
        ground_surface.blit(ground_texture, (i, 0+(GROUND_TILE_WIDTH*1)))
        ground_surface.blit(ground_texture, (i, 0+(GROUND_TILE_WIDTH*2)))
    screen.blit(ground_surface, camera.world_to_screen(-5000, 0))
    return ground_surface



