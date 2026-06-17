def mouse_collision(pygame, rect):
    mouseX, mouseY = pygame.mouse.get_pos()
    if (
        mouseX > rect.x
        and mouseX < rect.x + rect.width
        and mouseY > rect.y
        and mouseY < rect.y + rect.height
    ):
        return True
    else:
        return False
