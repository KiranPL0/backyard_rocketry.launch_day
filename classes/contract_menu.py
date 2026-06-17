from classes.menu_component import MenuComponent
from calc.mouse_collision import mouse_collision
from settings import WIDTH, HEIGHT, VAB_LEVEL_CONSTRAINTS


class ContractMenu:
    def __init__(self, ui_elements, scene_elements, player):
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
        self.warning_tooltip = None

        from assets.asset_loader import contracts

        curr_page = 0

        for i in range(len(contracts)):
            contract = contracts[i]
            if contract.check_requirements(self.player):
                if curr_page in self.page_components:
                    if len(self.page_components[curr_page]) < self.items_per_page:
                        self.page_components[curr_page].append(
                            MenuComponent(
                                contract.name,
                                f"Description: {contract.description}\nReward: ${contract.money}\nReputation: {contract.reputation}",
                                ui_elements[
                                    "icon_" + contract.company.replace(" ", "_").lower()
                                ],
                                lambda _, contract=contract: player.accept_contract(
                                    contract
                                ),
                            )
                        )
                    else:
                        curr_page += 1
                        self.page_titles.append("Contracts")
                        self.page_components[curr_page] = []
                        self.page_components[curr_page].append(
                            MenuComponent(
                                contract.name,
                                f"Description: {contract.description}\nReward: ${contract.money}\nReputation: {contract.reputation}",
                                ui_elements[
                                    "icon_" + contract.company.replace(" ", "_").lower()
                                ],
                                lambda _, contract=contract: player.accept_contract(
                                    contract
                                ),
                            )
                        )
                else:
                    self.page_titles.append("Contracts")
                    self.page_components[curr_page] = []
                    self.page_components[curr_page].append(
                        MenuComponent(
                            contract.name,
                            f"Description: {contract.description}\nReward: ${contract.money}\nReputation: {contract.reputation}",
                            ui_elements[
                                "icon_" + contract.company.replace(" ", "_").lower()
                            ],
                            lambda _, contract=contract: player.accept_contract(
                                contract
                            ),
                        )
                    )

    def align_right(self):
        self.x = WIDTH - self.width - 10
        self.grid_x = self.x + 25
        self.grid_y = self.y + 60
        self.item_height = self.grid_height // self.items_per_page

    def draw(self, pygame, screen, cursor_manager):
        from assets.asset_loader import font_40

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

    def update_contracts(self):
        from assets.asset_loader import contracts, ui_elements

        self.page_components = {}
        self.page_titles = []
        curr_page = 0

        for i in range(len(contracts)):
            contract = contracts[i]
            if contract.check_requirements(self.player):
                callback_action = (
                    lambda _, contract=contract: self.player.accept_contract(contract)
                )
                if curr_page in self.page_components:
                    if len(self.page_components[curr_page]) < self.items_per_page:
                        self.page_components[curr_page].append(
                            MenuComponent(
                                contract.name,
                                f"Description: {contract.description}\nReward: ${contract.money}\nReputation: {contract.reputation}",
                                ui_elements[
                                    "icon_" + contract.company.replace(" ", "_").lower()
                                ],
                                callback_action,
                            )
                        )
                    else:
                        curr_page += 1
                        self.page_titles.append("Contracts")
                        self.page_components[curr_page] = []
                        self.page_components[curr_page].append(
                            MenuComponent(
                                contract.name,
                                f"Description: {contract.description}\nReward: ${contract.money}\nReputation: {contract.reputation}",
                                ui_elements[
                                    "icon_" + contract.company.replace(" ", "_").lower()
                                ],
                                callback_action,
                            )
                        )
                else:
                    self.page_titles.append("Contracts")
                    self.page_components[curr_page] = []
                    self.page_components[curr_page].append(
                        MenuComponent(
                            contract.name,
                            f"Description: {contract.description}\nReward: ${contract.money}\nReputation: {contract.reputation}",
                            ui_elements[
                                "icon_" + contract.company.replace(" ", "_").lower()
                            ],
                            callback_action,
                        )
                    )
