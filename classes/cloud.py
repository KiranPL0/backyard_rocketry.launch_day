import random

class Cloud:
    def __init__(self, img, band):
        self.img = img
        self.x = random.randint(-5000, 5000)
        self.y = random.randint(band[0], band[1]) # band: [min_alt, max_alt]

    def draw(self, screen, camera):
        x, y = camera.world_to_screen(self.x, self.y)
        screen.blit(self.img, (x, y))