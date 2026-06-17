class Story:
    def __init__(self, lines, line_finish_callback=None):
        self.lines = lines
        self.current_line = 0
        self.current_line_displayed = ""
        self.character_index = 0
        self.char_interval = 0.1
        self.character_timer = 0
        self.line_timer = 0
        self.line_display_time = 2.0
        self.line_done = False
        self.line_finish_callback = line_finish_callback
        self.finished = False

    def draw(self, pygame, screen, dt):
        screen.fill((0, 0, 0))
        from assets.asset_loader import font_40, font_30

        current_full_line = self.lines[self.current_line]
        if not self.line_done:
            self.character_timer += dt
            if self.character_timer >= self.char_interval:
                self.character_timer -= self.char_interval
                if self.character_index < len(current_full_line):
                    self.current_line_displayed += current_full_line[
                        self.character_index
                    ]
                    self.character_index += 1
                else:
                    self.line_done = True
        else:
            self.line_timer += dt

            if self.line_timer >= self.line_display_time:
                self.line_timer = 0

                if self.current_line < len(self.lines) - 1:
                    self.current_line += 1
                    self.current_line_displayed = ""
                    self.character_index = 0
                    self.line_done = False
                else:
                    self.finished = True
                    if self.line_finish_callback != None:
                        self.line_finish_callback()
        text_surface = font_40.render(
            self.current_line_displayed, True, (255, 255, 255)
        )

        text_rect = text_surface.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2)
        )

        text2_surface = font_30.render("Press [S] to skip", True, (230, 230, 230))
        text2_rect = text2_surface.get_rect(
            center=(screen.get_width() // 2, screen.get_height() - 50)
        )
        screen.blit(text_surface, text_rect)
        screen.blit(text2_surface, text2_rect)
