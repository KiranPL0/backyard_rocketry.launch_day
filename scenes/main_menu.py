from settings import WIDTH, HEIGHT
from calc.mouse_collision import mouse_collision


class MainMenu:
    def __init__(self, callback_start):
        from assets.asset_loader import ui_elements

        self.start_btn_rect = None
        self.help_btn_rect = None
        self.callback_start = callback_start
        self.help_menu_hidden = True
        self.close_btn_rect = None
        self.quit_btn_rect = None

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
        help_btn_rect = help_btn.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
        self.help_btn_rect = help_btn_rect
        screen.blit(help_btn, help_btn_rect)
        font_surface = font_40.render("Help", True, (255, 255, 255))
        font_rect = font_surface.get_rect(center=help_btn_rect.center)
        screen.blit(font_surface, font_rect)
        quit_btn = ui_elements["vab_button"]
        quit_btn = pygame.transform.scale(quit_btn, (300, 100))
        quit_btn_rect = quit_btn.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 250))
        self.quit_btn_rect = quit_btn_rect
        screen.blit(quit_btn, quit_btn_rect)
        font_surface = font_40.render("Quit", True, (255, 255, 255))
        font_rect = font_surface.get_rect(center=quit_btn_rect.center)
        screen.blit(font_surface, font_rect)
        if self.help_menu_hidden == False:
            bg_panel = ui_elements["context_menu"]
            bg_panel_rect = bg_panel.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(bg_panel, bg_panel_rect)
            help_text = [
                "Welcome to Backyard Rocketry: Launch Day!",
                "To control your rocket, it must have a",
                "control surface component. Use the [A]",
                "and [D] keys to control your rocket's angle.",
                "If you find your flight is taking too long,",
                "You can press [E] to end it early.",
                "If you've already reached your contract",
                "expectations or milestone in your flight,",
                "then pressing [E] will not erase your progress. ",
                "Only skip cutscenes if you know what you're doing.",
                "Good luck, and have fun rocketing!",
            ]
            for i in range(len(help_text)):
                font_surface = font_20.render(help_text[i], True, (0, 0, 0))
                font_rect = font_surface.get_rect(
                    center=(WIDTH // 2, HEIGHT // 2 - 100 + i * 20)
                )
                screen.blit(font_surface, font_rect)
            close_button = ui_elements["button"]
            close_button = pygame.transform.scale(close_button, (100, 50))
            close_button_rect = close_button.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 150)
            )
            self.close_btn_rect = close_button_rect
            screen.blit(close_button, close_button_rect)
            font_surface = font_20.render("Close", True, (255, 255, 255))
            font_rect = font_surface.get_rect(center=close_button_rect.center)
            screen.blit(font_surface, font_rect)
        # ADD A CLOSE FEATURE!
        if mouse_collision(pygame, start_btn_rect):
            cursor_manager.click_cursor()
        elif mouse_collision(pygame, help_btn_rect):
            cursor_manager.click_cursor()
        elif mouse_collision(pygame, quit_btn_rect):
            cursor_manager.click_cursor()
        elif not self.help_menu_hidden and mouse_collision(pygame, self.close_btn_rect):
            cursor_manager.click_cursor()

    def handle_click(self, pygame):
        if (
            self.start_btn_rect
            and mouse_collision(pygame, self.start_btn_rect)
            and self.help_menu_hidden == True
        ):
            self.callback_start()
        elif (
            self.help_btn_rect
            and mouse_collision(pygame, self.help_btn_rect)
            and self.help_menu_hidden == True
        ):
            self.help_menu_hidden = False
        elif (
            self.close_btn_rect
            and mouse_collision(pygame, self.close_btn_rect)
            and self.help_menu_hidden == False
        ):
            self.help_menu_hidden = True
        elif (
            self.quit_btn_rect
            and mouse_collision(pygame, self.quit_btn_rect)
            and self.help_menu_hidden == True
        ):
            # Quit the game cleanly
            try:
                pygame.quit()
            except Exception:
                pass
            import sys

            sys.exit()
