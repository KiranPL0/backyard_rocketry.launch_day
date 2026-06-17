import math

class Explosion:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy
        self.frame = 0
        self.frame_duration = 0.12
    
    def draw(self, pygame, screen, camera):
        from assets.asset_loader import explosion_images
        r = self.energy * 10
        image = explosion_images[self.frame]
        image = pygame.transform.scale(image, (r*2, r*2))
        rect = image.get_rect(center=(camera.world_to_screen(self.x, self.y)))
        screen.blit(image, rect )
    def next_frame(self):
        self.frame += 1
        if self.frame >= 10:
            return "REMOVE"
