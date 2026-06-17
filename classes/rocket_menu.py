from classes.menu_component import MenuComponent
from calc.mouse_collision import mouse_collision
from settings import WIDTH, HEIGHT


class RocketMenu:
    def __init__(self, ui_elements, scene_elements, player, pygame, temp_rocket):
        self.visible = True
        self.ui_elements = ui_elements
        self.scene_elements = scene_elements
        self.player = player
        self.page = 0
        self.width = 350
        self.height = 700
        self.x = 10
        self.y = 10
        self.grid_x = self.x + 25
        self.grid_y = self.y + 60
        self.grid_height = self.height - 120
        self.grid_width = self.width - 45
        self.items_per_page = 7
        self.item_height = self.grid_height // self.items_per_page
        self.page_components = {}
        self.page_titles = []
        self.button_next_rect = None
        self.button_previous_rect = None
        self.button_next_visible = True
        self.button_prev_visible = True
        self.temp_rocket = temp_rocket

    def update_list(self, temp_rocket, ui_elements, pygame):
        engine = temp_rocket.engine

        curr_page = 0

        callback_action = self.remove_engine
        callback_action_component = self.remove_component
        self.page_components = {}
        self.page_titles = []
        self.page_components[curr_page] = []
        self.page_titles.append("Engines")
        if engine != None:
            self.page_components[curr_page].append(
                MenuComponent(
                    engine.name,
                    "",
                    pygame.image.load(
                        "./assets/rocket_components/engine/" + engine.asset
                    ).convert_alpha(),
                    callback_action,
                )
            )
        else:
            self.page_components[curr_page].append(
                MenuComponent(
                    "No Engine",
                    "",
                    ui_elements["icon_warning"],
                    callback_action,
                )
            )
        curr_page += 1
        # left structure
        left_structure = temp_rocket.structure["left"]
        for i in range(len(left_structure)):
            component = left_structure[i]
            if curr_page in self.page_components:
                if len(self.page_components[curr_page]) < self.items_per_page:
                    self.page_components[curr_page].append(
                        MenuComponent(
                            component.name,
                            f"Type: {component.type}\nMass: {component.mass} kg",
                            pygame.image.load(
                                "./assets/rocket_components/structural/"
                                + component.asset
                            ).convert_alpha(),
                            callback_action_component,
                        )
                    )
                else:
                    curr_page += 1
                    self.page_titles.append("Left Structure")
                    self.page_components[curr_page] = []
                    self.page_components[curr_page].append(
                        MenuComponent(
                            component.name,
                            f"Type: {component.type}\nMass: {component.mass} kg",
                            pygame.image.load(
                                "./assets/rocket_components/structural/"
                                + component.asset
                            ).convert_alpha(),
                            callback_action_component,
                        )
                    )
            else:
                self.page_titles.append("Left Structure")
                self.page_components[curr_page] = []
                self.page_components[curr_page].append(
                    MenuComponent(
                        component.name,
                        f"Type: {component.type}\nMass: {component.mass} kg",
                        pygame.image.load(
                            "./assets/rocket_components/structural/" + component.asset
                        ).convert_alpha(),
                        callback_action_component,
                    )
                )
        if len(left_structure) > 0:
            curr_page += 1
        # center structure
        center_structure = temp_rocket.structure["center"]
        for i in range(len(center_structure)):
            component = center_structure[i]
            if curr_page in self.page_components:
                if len(self.page_components[curr_page]) < self.items_per_page:
                    self.page_components[curr_page].append(
                        MenuComponent(
                            component.name,
                            f"Type: {component.type}\nMass: {component.mass} kg",
                            pygame.image.load(
                                "./assets/rocket_components/structural/"
                                + component.asset
                            ).convert_alpha(),
                            callback_action_component,
                        )
                    )
                else:
                    curr_page += 1
                    self.page_titles.append("Center Structure")
                    self.page_components[curr_page] = []
                    self.page_components[curr_page].append(
                        MenuComponent(
                            component.name,
                            f"Type: {component.type}\nMass: {component.mass} kg",
                            pygame.image.load(
                                "./assets/rocket_components/structural/"
                                + component.asset
                            ).convert_alpha(),
                            callback_action_component,
                        )
                    )
            else:
                self.page_titles.append("Center Structure")
                self.page_components[curr_page] = []
                self.page_components[curr_page].append(
                    MenuComponent(
                        component.name,
                        f"Type: {component.type}\nMass: {component.mass} kg",
                        pygame.image.load(
                            "./assets/rocket_components/structural/" + component.asset
                        ).convert_alpha(),
                        callback_action_component,
                    )
                )
        if len(center_structure) > 0:
            curr_page += 1
        # right structure
        right_structure = temp_rocket.structure["right"]
        for i in range(len(right_structure)):
            component = right_structure[i]
            if curr_page in self.page_components:
                if len(self.page_components[curr_page]) < self.items_per_page:
                    self.page_components[curr_page].append(
                        MenuComponent(
                            component.name,
                            f"Type: {component.type}\nMass: {component.mass} kg",
                            pygame.image.load(
                                "./assets/rocket_components/structural/"
                                + component.asset
                            ).convert_alpha(),
                            callback_action_component,
                        )
                    )
                else:
                    curr_page += 1
                    self.page_titles.append("Right Structure")
                    self.page_components[curr_page] = []
                    self.page_components[curr_page].append(
                        MenuComponent(
                            component.name,
                            f"Type: {component.type}\nMass: {component.mass} kg",
                            pygame.image.load(
                                "./assets/rocket_components/structural/"
                                + component.asset
                            ).convert_alpha(),
                            callback_action_component,
                        )
                    )
            else:
                self.page_titles.append("Right Structure")
                self.page_components[curr_page] = []
                self.page_components[curr_page].append(
                    MenuComponent(
                        component.name,
                        f"Type: {component.type}\nMass: {component.mass} kg",
                        pygame.image.load(
                            "./assets/rocket_components/structural/" + component.asset
                        ).convert_alpha(),
                        callback_action_component,
                    )
                )
        if len(right_structure) > 0:
            curr_page += 1
        # internal structure
        internal_structure = temp_rocket.structure["internal"]
        for i in range(len(internal_structure)):
            component = internal_structure[i]
            if curr_page in self.page_components:
                if len(self.page_components[curr_page]) < self.items_per_page:
                    self.page_components[curr_page].append(
                        MenuComponent(
                            component.name,
                            f"Type: {component.type}\nMass: {component.mass} kg",
                            pygame.image.load(
                                "./assets/rocket_components/structural/"
                                + component.asset
                            ).convert_alpha(),
                            callback_action_component,
                        )
                    )
                else:
                    curr_page += 1
                    self.page_titles.append("Internal Structure")
                    self.page_components[curr_page] = []
                    self.page_components[curr_page].append(
                        MenuComponent(
                            component.name,
                            f"Type: {component.type}\nMass: {component.mass} kg",
                            pygame.image.load(
                                "./assets/rocket_components/structural/"
                                + component.asset
                            ).convert_alpha(),
                            callback_action_component,
                        )
                    )
            else:
                self.page_titles.append("Internal Structure")
                self.page_components[curr_page] = []
                self.page_components[curr_page].append(
                    MenuComponent(
                        component.name,
                        f"Type: {component.type}\nMass: {component.mass} kg",
                        pygame.image.load(
                            "./assets/rocket_components/structural/" + component.asset
                        ).convert_alpha(),
                        callback_action_component,
                    )
                )

    def align_right(self):
        self.x = WIDTH - self.width - 10
        self.grid_x = self.x + 25
        self.grid_y = self.y + 60
        self.item_height = self.grid_height // self.items_per_page

    def draw(self, pygame, screen, cursor_manager, temp_rocket):
        from assets.asset_loader import font_30

        side_menu = self.ui_elements["side_menu"]
        side_menu = pygame.transform.scale(side_menu, (self.width, self.height))
        screen.blit(side_menu, (self.x, self.y))
        if self.page_titles != []:
            title_text = font_30.render(
                self.page_titles[self.page], False, (255, 255, 255)
            )
            title_text_rect = title_text.get_rect(
                center=(self.x + self.width // 2, self.y + 40)
            )
            screen.blit(title_text, title_text_rect)
            for i in range(len(self.page_components[self.page])):
                component = self.page_components[self.page][i]
                component.draw(
                    pygame,
                    screen,
                    self.grid_x,
                    self.grid_y + i * self.item_height,
                    self.grid_width,
                    self.item_height,
                    cursor_manager,
                )

        # pygame.draw.rect(
        #     screen,
        #     (255, 255, 255),
        #     (self.grid_x, self.grid_y, self.grid_width, self.grid_height),
        #     2,
        # )
        # (NOTE TO SELF): uncomment above code to view ui boundin box

        # for i in range(self.items_per_page):
        #     pygame.draw.rect(
        #         screen,
        #         (28 * i, 28 * i, 28 * i),
        #         (
        #             self.grid_x,
        #             self.grid_y + i * self.item_height,
        #             self.grid_width,
        #             self.item_height,
        #         ),
        #     )

        forward_btn = self.ui_elements["icon_vab_forward"]
        backward_btn = self.ui_elements["icon_vab_previous"]
        forward_btn = pygame.transform.scale(forward_btn, (40, 40))
        backward_btn = pygame.transform.scale(backward_btn, (40, 40))
        forward_btn_rect = forward_btn.get_rect(
            center=(((self.width) // 2 + self.x) + 30, self.y + (self.height - 40))
        )
        self.button_next_rect = forward_btn_rect
        backward_btn_rect = backward_btn.get_rect(
            center=(((self.width) // 2 + self.x) - 30, self.y + (self.height - 40))
        )
        self.button_previous_rect = backward_btn_rect
        self.button_prev_visible = False
        self.button_next_visible = False
        if self.page != 0:
            screen.blit(backward_btn, backward_btn_rect)
            self.button_prev_visible = True
        if self.page != len(self.page_components) - 1:
            screen.blit(forward_btn, forward_btn_rect)
            self.button_next_visible = True
        self.handle_hover(pygame, cursor_manager)

    def handle_hover(self, pygame, cursor_manager):
        if self.button_next_rect != None and self.button_next_rect != None:
            next_rect_collision = mouse_collision(pygame, self.button_next_rect)
            previous_rect_collision = mouse_collision(pygame, self.button_previous_rect)
            if (next_rect_collision and self.button_next_visible) or (
                previous_rect_collision and self.button_prev_visible
            ):
                cursor_manager.click_cursor()
                return

    def handle_click(self, pygame):
        if self.button_next_rect != None and self.button_next_rect != None:
            next_rect_collision = mouse_collision(pygame, self.button_next_rect)
            previous_rect_collision = mouse_collision(pygame, self.button_previous_rect)
            if next_rect_collision and self.button_next_visible:
                if self.page < len(self.page_components) - 1:
                    self.page += 1
                return
            elif previous_rect_collision and self.button_prev_visible:
                if self.page > 0:
                    self.page -= 1
                return
        for component in self.page_components[self.page]:
            component.handle_click(pygame)

    def print_ack(self, name):
        print(name)

    def remove_component(self, name):
        from assets.asset_loader import components

        component_price = 0
        for component in components:
            if component.name == name:
                component_price = component.cost
                break
        self.player.money += component_price
        self.temp_rocket.remove_component(name)
        self.page = 0

    def remove_engine(self, _):
        from assets.asset_loader import engines

        engine_price = 0
        for engine in engines:
            if engine.name == self.temp_rocket.engine.name:
                engine_price = engine.cost
                break
        self.player.money += engine_price
        self.temp_rocket.engine = None
        self.page = 0
