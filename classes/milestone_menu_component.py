from calc.mouse_collision import mouse_collision


class MenuComponent:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def draw(self, screen, x, y):
        # preserve aspect ratio
        from assets.asset_loader import font_20, font_15

        name = font_20.render(self.name, False, (255, 255, 255))
        screen.blit(name, (x + 10, y + 2))
        description_text = self.description.split("\n")
        for i in range(len(description_text)):
            if "status" in description_text[i].lower():
                if "not" in description_text[i].lower():
                    description = font_15.render(
                        description_text[i], False, (255, 100, 100)
                    )
                else:
                    description = font_15.render(
                        description_text[i], False, (100, 255, 100)
                    )
            else:
                description = font_15.render(
                    description_text[i], False, (230, 230, 230)
                )
            screen.blit(
                description,
                (
                    x + 10,
                    y + 5 + name.get_height() + i * (description.get_height() + 5),
                ),
            )
