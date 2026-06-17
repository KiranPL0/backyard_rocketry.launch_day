from calc.mouse_collision import mouse_collision


class Modal:
    def __init__(self, title):
        self.hidden = True
        self.title = title

    def update(self, events):
        pass

    def draw(self, screen):
        pass


class WarningContextMenu(Modal):
    def __init__(self, title, description, focus, unfocus):
        super().__init__(title)
        self.description = description
        self.button_rect = None
        self.focus_callback = focus
        self.unfocus_callback = unfocus
        self.acknowledge_callback = None

    def show(self):
        self.hidden = False

    def set_acknowledge_callback(self, callback):
        self.acknowledge_callback = callback

    def update_content(self, title, desciription):
        self.title = title
        self.description = desciription

    def draw(self, pygame, screen):
        from assets.asset_loader import font_20, font_15, font_10, ui_elements
        from settings import WIDTH, HEIGHT

        if self.hidden == False:
            dim = pygame.Surface((WIDTH, HEIGHT))
            dim.set_alpha(128)
            dim.fill((0, 0, 0))
            screen.blit(dim, (0, 0))

            bg_img = ui_elements["context_menu"]
            bg_img = pygame.transform.scale(bg_img, (400, 200))
            bg_rect = bg_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(bg_img, bg_rect)
            title = font_15.render(self.title, True, (220, 220, 220))
            screen.blit(title, (bg_rect.x + 110, bg_rect.y + 7))

            warning_icon = pygame.transform.scale(ui_elements["icon_warning"], (50, 50))
            warning_icon_rect = warning_icon.get_rect(
                center=(WIDTH // 2, bg_rect.y + 60)
            )
            screen.blit(warning_icon, warning_icon_rect)

            description = font_20.render(self.description, True, (14, 14, 14))
            description_rect = description.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(description, description_rect)

            button_img = ui_elements["button"]
            button_hover_img = ui_elements["button_hover"]
            button_img = pygame.transform.scale(button_img, (100, 33))
            button_hover_img = pygame.transform.scale(button_hover_img, (100, 33))
            button_rect = button_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            self.button_rect = button_rect
            if mouse_collision(pygame, button_rect):
                screen.blit(button_hover_img, button_rect)
                pygame.mouse.set_cursor(ui_elements["cursor_clicker"])
            else:
                screen.blit(button_img, button_rect)
                pygame.mouse.set_cursor(ui_elements["cursor_pointer"])
            button_text = font_15.render("OK", True, (255, 255, 255))
            button_text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, button_text_rect)

    def button_update(self, pygame, event):
        from assets.asset_loader import ui_elements

        if self.hidden == False:
            if mouse_collision(pygame, self.button_rect):
                self.hidden = True
                pygame.mouse.set_cursor(ui_elements["cursor_pointer"])
                self.focus_callback()
                self.acknowledge_callback()


class SaveGameContextMenu(Modal):
    def __init__(self, focus, unfocus):
        super().__init__("Save Game")
        self.text_field = ""
        self.width = 600
        self.height = 400
        self.continue_rect = None
        self.back_rect = None
        self.focus_callback = focus
        self.unfocus_callback = unfocus

    def text_update(self, pygame, event):
        if self.hidden == False:
            if event.key == pygame.K_BACKSPACE:
                if len(self.text_field) > 0:
                    self.text_field = self.text_field[:-1]  # backspace
            else:
                if len(self.text_field) <= 20:
                    if event.unicode != "\\" and event.unicode != "/":
                        self.text_field += event.unicode

    def button_update(self, pygame, event):
        from assets.asset_loader import ui_elements

        if self.hidden == False:
            if mouse_collision(pygame, self.continue_rect) and self.text_field != "":
                # process continue
                self.hidden = True
                text_cache = self.text_field
                self.text_field = ""
                self.focus_callback()
                pygame.mouse.set_cursor(ui_elements["cursor_pointer"])
                return text_cache
            if mouse_collision(pygame, self.back_rect):
                self.hidden = True
                self.text_field = ""
                self.focus_callback()
                pygame.mouse.set_cursor(ui_elements["cursor_pointer"])

    def draw(self, pygame, screen):
        from assets.asset_loader import font_20, font_40, ui_elements
        from settings import WIDTH, HEIGHT

        if self.hidden == False:
            dim = pygame.Surface((WIDTH, HEIGHT))
            dim.set_alpha(128)
            dim.fill((0, 0, 0))
            screen.blit(dim, (0, 0))

            bg_img = ui_elements["context_menu"]
            bg_img = pygame.transform.scale(bg_img, (self.width, self.height))
            bg_rect = bg_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(bg_img, bg_rect)
            title = font_20.render(self.title, True, (220, 220, 220))
            screen.blit(title, (bg_rect.x + 170, bg_rect.y + 20))

            title_context = font_40.render("Enter a save name", True, (14, 14, 14))
            title_context_rect = title_context.get_rect(
                center=(WIDTH // 2, bg_rect.y + 100)
            )
            screen.blit(title_context, title_context_rect)

            text_box_img = ui_elements["text_box"]
            text_box_img = pygame.transform.scale(text_box_img, (250, 50))
            text_box_rect = text_box_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text_box_img, text_box_rect)

            text_box_content = font_20.render(self.text_field, True, (14, 14, 14))
            text_box_content_rect = text_box_content.get_rect(
                center=(WIDTH // 2, HEIGHT // 2)
            )
            screen.blit(text_box_content, text_box_content_rect)
            button_img = ui_elements["button"]
            button_hover_img = ui_elements["button_hover"]
            button_img = pygame.transform.scale(button_img, (150, 50))
            button_hover_img = pygame.transform.scale(button_hover_img, (150, 50))
            button_rect_continue = button_img.get_rect(
                center=(WIDTH // 2 + 100, HEIGHT // 2 + 100)
            )
            self.continue_rect = button_rect_continue
            button_rect_back = button_img.get_rect(
                center=(WIDTH // 2 - 100, HEIGHT // 2 + 100)
            )
            self.back_rect = button_rect_back
            if mouse_collision(pygame, button_rect_continue):
                screen.blit(button_hover_img, button_rect_continue)
            else:
                screen.blit(button_img, button_rect_continue)

            if mouse_collision(pygame, button_rect_back):
                screen.blit(button_hover_img, button_rect_back)
            else:
                screen.blit(button_img, button_rect_back)

            if mouse_collision(pygame, button_rect_continue) or mouse_collision(
                pygame, button_rect_back
            ):
                pygame.mouse.set_cursor(ui_elements["cursor_clicker"])
            else:
                pygame.mouse.set_cursor(ui_elements["cursor_pointer"])

            continue_text = font_20.render("Continue", True, (255, 255, 255))
            continue_text_rect = continue_text.get_rect(
                center=(WIDTH // 2 + 100, HEIGHT // 2 + 95)
            )
            screen.blit(continue_text, continue_text_rect)
            back_text = font_20.render("Cancel", True, (255, 255, 255))
            back_text_rect = back_text.get_rect(
                center=(WIDTH // 2 - 100, HEIGHT // 2 + 95)
            )
            screen.blit(back_text, back_text_rect)


class LoadGameContextMenu(Modal):
    def __init__(self, focus, unfocus):
        super().__init__("Load Game")
        self.text_field = ""
        self.width = 600
        self.height = 400
        self.continue_rect = None
        self.back_rect = None
        self.focus_callback = focus
        self.unfocus_callback = unfocus

    def text_update(self, pygame, event):
        if self.hidden == False:
            if event.key == pygame.K_BACKSPACE:
                if len(self.text_field) > 0:
                    self.text_field = self.text_field[:-1]  # backspace
            else:
                if len(self.text_field) <= 20:
                    if event.unicode != "\\" and event.unicode != "/":
                        self.text_field += event.unicode

    def button_update(self, pygame, event):
        from assets.asset_loader import ui_elements

        if self.hidden == False:
            if mouse_collision(pygame, self.continue_rect) and self.text_field != "":
                # process continue
                self.hidden = True
                text_cache = self.text_field
                self.text_field = ""
                self.focus_callback()
                pygame.mouse.set_cursor(ui_elements["cursor_pointer"])
                return text_cache
            if mouse_collision(pygame, self.back_rect):
                self.hidden = True
                self.text_field = ""
                self.focus_callback()
                pygame.mouse.set_cursor(ui_elements["cursor_pointer"])

    def draw(self, pygame, screen):
        from assets.asset_loader import font_20, font_40, ui_elements
        from settings import WIDTH, HEIGHT

        if self.hidden == False:
            dim = pygame.Surface((WIDTH, HEIGHT))
            dim.set_alpha(128)
            dim.fill((0, 0, 0))
            screen.blit(dim, (0, 0))

            bg_img = ui_elements["context_menu"]
            bg_img = pygame.transform.scale(bg_img, (self.width, self.height))
            bg_rect = bg_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(bg_img, bg_rect)
            title = font_20.render(self.title, True, (220, 220, 220))
            screen.blit(title, (bg_rect.x + 170, bg_rect.y + 20))

            title_context = font_40.render("Enter a save name", True, (14, 14, 14))
            title_context_rect = title_context.get_rect(
                center=(WIDTH // 2, bg_rect.y + 100)
            )
            screen.blit(title_context, title_context_rect)

            text_box_img = ui_elements["text_box"]
            text_box_img = pygame.transform.scale(text_box_img, (250, 50))
            text_box_rect = text_box_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text_box_img, text_box_rect)

            text_box_content = font_20.render(self.text_field, True, (14, 14, 14))
            text_box_content_rect = text_box_content.get_rect(
                center=(WIDTH // 2, HEIGHT // 2)
            )
            screen.blit(text_box_content, text_box_content_rect)
            button_img = ui_elements["button"]
            button_hover_img = ui_elements["button_hover"]
            button_img = pygame.transform.scale(button_img, (150, 50))
            button_hover_img = pygame.transform.scale(button_hover_img, (150, 50))
            button_rect_continue = button_img.get_rect(
                center=(WIDTH // 2 + 100, HEIGHT // 2 + 100)
            )
            self.continue_rect = button_rect_continue
            button_rect_back = button_img.get_rect(
                center=(WIDTH // 2 - 100, HEIGHT // 2 + 100)
            )
            self.back_rect = button_rect_back
            if mouse_collision(pygame, button_rect_continue):
                screen.blit(button_hover_img, button_rect_continue)
            else:
                screen.blit(button_img, button_rect_continue)

            if mouse_collision(pygame, button_rect_back):
                screen.blit(button_hover_img, button_rect_back)
            else:
                screen.blit(button_img, button_rect_back)

            if mouse_collision(pygame, button_rect_continue) or mouse_collision(
                pygame, button_rect_back
            ):
                pygame.mouse.set_cursor(ui_elements["cursor_clicker"])
            else:
                pygame.mouse.set_cursor(ui_elements["cursor_pointer"])

            continue_text = font_20.render("Continue", True, (255, 255, 255))
            continue_text_rect = continue_text.get_rect(
                center=(WIDTH // 2 + 100, HEIGHT // 2 + 95)
            )
            screen.blit(continue_text, continue_text_rect)
            back_text = font_20.render("Cancel", True, (255, 255, 255))
            back_text_rect = back_text.get_rect(
                center=(WIDTH // 2 - 100, HEIGHT // 2 + 95)
            )
            screen.blit(back_text, back_text_rect)
