class CursorManager:
    def __init__(self):
        self.cursor = "pointer"

    def reset_cursor(self):
        self.cursor = "pointer"

    def click_cursor(self):
        self.cursor = "clicker"

    def apply_cursor(self, pygame, ui_elements):
        if self.cursor == "clicker":
            pygame.mouse.set_cursor(ui_elements["cursor_clicker"])
        else:
            pygame.mouse.set_cursor(ui_elements["cursor_pointer"])
