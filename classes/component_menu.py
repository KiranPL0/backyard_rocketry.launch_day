from classes.menu_component import MenuComponent
from calc.mouse_collision import mouse_collision
from settings import WIDTH, HEIGHT, VAB_LEVEL_CONSTRAINTS


class ComponentMenu:
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
        self.warning_tooltip = None
        self.player = player

        from assets.asset_loader import unlocked_engines, unlocked_components

        curr_page = 0

        callback_action = self.add_engine
        callback_action_component = self.add_component
        engines = unlocked_engines
        components = unlocked_components
        for i in range(len(engines)):
            engine = engines[i]
            if curr_page in self.page_components:
                if len(self.page_components[curr_page]) < self.items_per_page:
                    self.page_components[curr_page].append(
                        MenuComponent(
                            engine.name,
                            f"Type: {engine.type}\nFuel Capacity: {engine.fuel_capacity} units\nMass: {engine.mass} kg\nCost: ${engine.cost}",
                            ui_elements["icon_" + engine.asset.split(".")[0]],
                            callback_action,
                        )
                    )
                else:
                    curr_page += 1
                    self.page_titles.append("Engines")
                    self.page_components[curr_page] = []
                    self.page_components[curr_page].append(
                        MenuComponent(
                            engine.name,
                            f"Type: {engine.type}\nFuel Capacity: {engine.fuel_capacity} units\nMass: {engine.mass} kg\nCost: ${engine.cost}",
                            pygame.image.load(
                                "./assets/rocket_components/engine/" + engine.asset
                            ).convert_alpha(),
                            callback_action,
                        )
                    )
            else:
                self.page_titles.append("Engines")
                self.page_components[curr_page] = []
                self.page_components[curr_page].append(
                    MenuComponent(
                        engine.name,
                        f"Type: {engine.type}\nFuel Capacity: {engine.fuel_capacity} units\nMass: {engine.mass} kg\nCost: ${engine.cost}",
                        pygame.image.load(
                            "./assets/rocket_components/engine/" + engine.asset
                        ).convert_alpha(),
                        callback_action,
                    )
                )

        curr_page += 1
        for i in range(len(components)):
            component = components[i]
            if curr_page in self.page_components:
                if len(self.page_components[curr_page]) < self.items_per_page:
                    self.page_components[curr_page].append(
                        MenuComponent(
                            component.name,
                            f"Type: {component.type}\nMass: {component.mass} kg\nCost: ${component.cost}",
                            pygame.image.load(
                                "./assets/rocket_components/structural/"
                                + component.asset
                            ).convert_alpha(),
                            callback_action_component,
                        )
                    )
                else:
                    curr_page += 1
                    self.page_titles.append("Components")
                    self.page_components[curr_page] = []
                    self.page_components[curr_page].append(
                        MenuComponent(
                            component.name,
                            f"Type: {component.type}\nMass: {component.mass} kg\nCost: ${component.cost}",
                            pygame.image.load(
                                "./assets/rocket_components/structural/"
                                + component.asset
                            ).convert_alpha(),
                            callback_action_component,
                        )
                    )

            else:
                self.page_titles.append("Components")
                self.page_components[curr_page] = []
                self.page_components[curr_page].append(
                    MenuComponent(
                        component.name,
                        f"Type: {component.type}\nMass: {component.mass} kg\nCost: ${component.cost}",
                        pygame.image.load(
                            "./assets/rocket_components/structural/" + component.asset
                        ).convert_alpha(),
                        callback_action_component,
                    )
                )

    def update_components(self, pygame):
        from assets.asset_loader import (
            unlocked_engines,
            unlocked_components,
            ui_elements,
        )

        # print(unlocked_engines)
        self.page_components = {}
        curr_page = 0

        callback_action = self.add_engine
        callback_action_component = self.add_component
        engines = unlocked_engines
        components = unlocked_components
        for i in range(len(engines)):
            engine = engines[i]
            if curr_page in self.page_components:
                if len(self.page_components[curr_page]) < self.items_per_page:
                    self.page_components[curr_page].append(
                        MenuComponent(
                            engine.name,
                            f"Type: {engine.type}\nFuel Capacity: {engine.fuel_capacity} units\nMass: {engine.mass} kg\nCost: ${engine.cost}",
                            pygame.image.load(
                                "./assets/rocket_components/engine/" + engine.asset
                            ).convert_alpha(),
                            callback_action,
                        )
                    )
                else:
                    curr_page += 1
                    self.page_titles.append("Engines")
                    self.page_components[curr_page] = []
                    self.page_components[curr_page].append(
                        MenuComponent(
                            engine.name,
                            f"Type: {engine.type}\nFuel Capacity: {engine.fuel_capacity} units\nMass: {engine.mass} kg\nCost: ${engine.cost}",
                            pygame.image.load(
                                "./assets/rocket_components/engine/" + engine.asset
                            ).convert_alpha(),
                            callback_action,
                        )
                    )
            else:
                self.page_titles.append("Engines")
                self.page_components[curr_page] = []
                self.page_components[curr_page].append(
                    MenuComponent(
                        engine.name,
                        f"Type: {engine.type}\nFuel Capacity: {engine.fuel_capacity} units\nMass: {engine.mass} kg\nCost: ${engine.cost}",
                        pygame.image.load(
                            "./assets/rocket_components/engine/" + engine.asset
                        ).convert_alpha(),
                        callback_action,
                    )
                )

        curr_page += 1
        for i in range(len(components)):
            component = components[i]
            if curr_page in self.page_components:
                if len(self.page_components[curr_page]) < self.items_per_page:
                    self.page_components[curr_page].append(
                        MenuComponent(
                            component.name,
                            f"Type: {component.type}\nMass: {component.mass} kg\nCost: ${component.cost}\nControl Surface: {component.control_surface}",
                            pygame.image.load(
                                "./assets/rocket_components/structural/"
                                + component.asset
                            ).convert_alpha(),
                            callback_action_component,
                        )
                    )
                else:
                    curr_page += 1
                    self.page_titles.append("Components")
                    self.page_components[curr_page] = []
                    self.page_components[curr_page].append(
                        MenuComponent(
                            component.name,
                            f"Type: {component.type}\nMass: {component.mass} kg\nCost: ${component.cost}\nControl Surface: {component.control_surface}",
                            pygame.image.load(
                                "./assets/rocket_components/structural/"
                                + component.asset
                            ).convert_alpha(),
                            callback_action_component,
                        )
                    )

            else:
                self.page_titles.append("Components")
                self.page_components[curr_page] = []
                self.page_components[curr_page].append(
                    MenuComponent(
                        component.name,
                        f"Type: {component.type}\nMass: {component.mass} kg\nCost: ${component.cost}\nControl Surface: {component.control_surface}",
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
        from assets.asset_loader import font_40

        if temp_rocket.engine == None and self.page != 0:
            self.page = 0
        if len(self.page_titles) == 0:
            return
        if self.page >= len(self.page_titles):
            self.page = len(self.page_titles) - 1

        side_menu = self.ui_elements["side_menu"]
        side_menu = pygame.transform.scale(side_menu, (self.width, self.height))
        title_text = font_40.render(self.page_titles[self.page], False, (255, 255, 255))
        screen.blit(side_menu, (self.x, self.y))
        title_text_rect = title_text.get_rect(
            center=(self.x + self.width // 2, self.y + 40)
        )
        screen.blit(title_text, title_text_rect)
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
        if self.page != len(self.page_components) - 1 and temp_rocket.engine != None:
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
        if len(self.page_components) == 0:
            return
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
        for i in range(len(self.page_components[self.page])):
            component = self.page_components[self.page][i]
            component.handle_click(pygame)

    def print_ack(self, name):
        print(name)

    def add_engine(self, name):
        from assets.asset_loader import engines

        engine_cost = 0
        for engine in engines:
            if engine.name == name:
                engine_cost = engine.cost
                break
        if self.player.money < engine_cost:
            self.warning_tooltip = "Not enough funds!"
        else:
            self.player.money -= engine_cost
            self.warning_tooltip = None
            self.temp_rocket.attach_engine(name)

    def add_component(self, name):
        max_height = VAB_LEVEL_CONSTRAINTS[self.player.stage]["height"]
        new_component = self.temp_rocket.get_component(name)
        from assets.asset_loader import components

        component_cost = 0
        for component in components:
            if component.name == name:
                component_cost = component.cost
                break
        if self.player.money < component_cost:
            self.warning_tooltip = "Not enough funds!"
            return
        else:
            _, height, _ = self.temp_rocket.get_rocket_dimensions_with_component(
                new_component
            )

            if height > max_height:
                self.warning_tooltip = "Rocket size limit reached"
            else:
                self.player.money -= component_cost
                self.temp_rocket.add_component(name)
                self.warning_tooltip = None
