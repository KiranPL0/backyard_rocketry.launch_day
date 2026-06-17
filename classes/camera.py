from settings import WIDTH, HEIGHT
import math

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def follow_object(self, x, y):
        target_x = x
        target_y = y

        self.x += (target_x-self.x) * 0.8
        self.y += (target_y-self.y) * 0.8
    
    def world_to_screen(self, world_x, world_y):
        return world_x - self.x + math.floor(WIDTH/2), self.y - world_y + math.floor(HEIGHT/2)
    
    def screen_to_world(self, screen_x, screen_y):
        return screen_x + self.x - math.floor(WIDTH/2), self.y - screen_y + math.floor(HEIGHT/2)

    def return_pygame_position(self, rocket):
        return rocket.x - self.x + math.floor(WIDTH/2), self.y - rocket.y + math.floor(HEIGHT/2)
