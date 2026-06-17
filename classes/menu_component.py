from calc.mouse_collision import mouse_collision


class MenuComponent:
    def __init__(self, name, description, image, action):
        self.name = name
        self.description = description
        self.image = image
        self.action = action
        self.image_rect = None

    def draw(self, pygame, screen, x, y, width, height, cursor_manager):
        # preserve aspect ratio
        from assets.asset_loader import font_20, font_15

        img = self.image
        img_width, img_height = img.get_size()
        aspect_ratio = img_width / img_height
        img = pygame.transform.scale(
            img, (int((height - 10) * aspect_ratio), height - 10)
        )
        self.image_rect = img.get_rect(topleft=(x + 5, y + 5))
        screen.blit(img, self.image_rect)
        # name
        name = font_20.render(self.name, False, (255, 255, 255))
        screen.blit(name, (x + int((height - 10) * aspect_ratio) + 10, y + 2))
        description_text = self.description.split("\n")
        for i in range(len(description_text)):
            description = font_15.render(description_text[i], False, (230, 230, 230))
            screen.blit(
                description,
                (
                    x + int((height - 10) * aspect_ratio) + 10,
                    y + 3 + name.get_height() + i * description.get_height(),
                ),
            )
            self.handle_hover(pygame, cursor_manager)

    def handle_hover(self, pygame, cursor_manager):
        if self.image_rect != None and mouse_collision(pygame, self.image_rect):
            cursor_manager.click_cursor()

    def handle_click(self, pygame):
        if self.action != None and self.image_rect != None:
            if mouse_collision(pygame, self.image_rect):
                self.action(self.name)
