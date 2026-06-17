from settings import WIDTH, HEIGHT
from calc.mouse_collision import mouse_collision


class MainMenu:
    def __init__(self, callback_start):
        from assets.asset_loader import ui_elements

        self.start_btn_rect = None
        self.help_btn_rect = None
        self.callback_start = callback_start
        self.help_menu_hidden = True

    def draw(self, pygame, screen, cursor_manager):
        from assets.asset_loader import font_40, font_20, ui_elements

        img_bg = ui_elements["main_menu_bg"]
        img_bg = pygame.transform.scale(img_bg, (WIDTH, HEIGHT))
        screen.blit(img_bg, (0, 0))

        start_btn = ui_elements["vab_button"]
        start_btn = pygame.transform.scale(start_btn, (300, 100))
        start_btn_rect = start_btn.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        self.start_btn_rect = start_btn_rect
        screen.blit(start_btn, start_btn_rect)
        font_surface = font_40.render("Start Game", True, (255, 255, 255))
        font_rect = font_surface.get_rect(center=start_btn_rect.center)
        screen.blit(font_surface, font_rect)

        help_btn = ui_elements["vab_button"]
        help_btn = pygame.transform.scale(help_btn, (300, 100))
        help_btn_rect = help_btn.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))
        self.help_btn_rect = help_btn_rect
        screen.blit(help_btn, help_btn_rect)
        font_surface = font_40.render("Help", True, (255, 255, 255))
        font_rect = font_surface.get_rect(center=help_btn_rect.center)
        screen.blit(font_surface, font_rect)
        if self.help_menu_hidden == False:
            bg_panel = ui_elements["context_menu"]
            bg_panel_rect = bg_panel.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(bg_panel, bg_panel_rect)
            help_text = [
                "Welcome to Backyard Rocketry: Launch Day!",
                "In this game, you will design and launch ",
                "rockets to complete various missions.",
                "Use the VAB (Vehicle Assembly Building) to design ",
                "your rocket, then head to the launch pad to ",
                "test it out! Complete contracts and progress",
                "through the story to unlock new parts and ",
                "challenges. Good luck, and have fun rocketing!",
            ]
            for i in range(len(help_text)):
                font_surface = font_20.render(help_text[i], True, (0, 0, 0))
                font_rect = font_surface.get_rect(
                    center=(WIDTH // 2, HEIGHT // 2 - 100 + i * 20)
                )
                screen.blit(font_surface, font_rect)
        # ADD A CLOSE FEATURE!
        if mouse_collision(pygame, start_btn_rect):
            cursor_manager.click_cursor()
        elif mouse_collision(pygame, help_btn_rect):
            cursor_manager.click_cursor()

    def handle_click(self, pygame):
        if mouse_collision(pygame, self.start_btn_rect):
            self.callback_start()
        elif mouse_collision(pygame, self.help_btn_rect):
            self.help_menu_hidden = False
