from settings import WIDTH, HEIGHT
from calc.mouse_collision import mouse_collision


class LaunchComplete:
    def __init__(self, rocket, player):
        self.rocket = rocket
        self.player = player
        self.active_contract = None
        self.contract_preserved = False
        self.milestones_achieved_cycle = []

    def check_mission_end(self):
        from assets.asset_loader import milestones

        if self.contract_preserved == False:
            self.active_contract = self.player.active_contract
            self.contract_preserved = True
            self.player.active_contract = None
        for milestone in milestones:
            current_achievement = milestone.check_achievement(self.rocket, self.player)
            if current_achievement == True:
                self.milestones_achieved_cycle.append(milestone)

    def draw(self, pygame, screen, rocket, ui_elements, player, cursor_manager):
        dim = pygame.Surface((WIDTH, HEIGHT))
        dim.set_alpha(128)
        dim.fill((0, 0, 0))
        screen.blit(dim, (0, 0))
        from assets.asset_loader import font_40, font_15, font_20, font_30
        from assets.asset_loader import milestones

        self.check_mission_end()

        if self.player.active_contract and self.contract_preserved == False:
            self.active_contract = self.player.active_contract
            self.contract_preserved = True
        if self.active_contract != None:
            contract_status = self.active_contract.check_contract_completion(
                self.player, self.rocket
            )
            if contract_status == True:
                title = font_40.render("Mission Complete!", False, (255, 255, 255))
                sub_text = font_15.render(
                    f"Contract Completed: {self.active_contract.name}",
                    True,
                    (255, 255, 255),
                )
            else:
                title = font_40.render("Mission Failed!", False, (255, 255, 255))
                sub_text = font_15.render(
                    f"Contract Failed: {self.active_contract.name}",
                    True,
                    (255, 255, 255),
                )
        else:
            title = font_40.render("No Active Contract", False, (255, 255, 255))
            sub_text = font_15.render(
                "Please select an active contract to progress", False, (255, 255, 255)
            )
        launch_end = ui_elements["launch_end"]
        launch_end = pygame.transform.scale(launch_end, (450, 600))
        screen.blit(
            launch_end,
            (
                WIDTH // 2 - launch_end.get_width() // 2,
                HEIGHT // 2 - launch_end.get_height() // 2,
            ),
        )

        screen.blit(
            title,
            (
                WIDTH // 2 - title.get_width() // 2,
                HEIGHT // 2 - title.get_height() // 2 - 250,
            ),
        )
        screen.blit(
            sub_text,
            (
                WIDTH // 2 - sub_text.get_width() // 2,
                HEIGHT // 2 - sub_text.get_height() // 2 - 200,
            ),
        )

        max_alt = font_20.render(
            f"Max Altitude: {int(rocket.max_alt)}m", False, (255, 255, 255)
        )
        screen.blit(
            max_alt,
            (
                WIDTH // 2 - max_alt.get_width() // 2,
                HEIGHT // 2 - max_alt.get_height() // 2 - 175,
            ),
        )
        max_velocity = font_20.render(
            f"Max Velocity: {int(rocket.max_v)}m/s", True, (255, 255, 255)
        )
        screen.blit(
            max_velocity,
            (
                WIDTH // 2 - max_velocity.get_width() // 2,
                HEIGHT // 2 - max_velocity.get_height() // 2 - 150,
            ),
        )

        milestones_title = font_30.render("Milestones:", False, (255, 255, 255))
        screen.blit(
            milestones_title,
            (
                WIDTH // 2 - milestones_title.get_width() // 2,
                HEIGHT // 2 - milestones_title.get_height() // 2 - 100,
            ),
        )
        milestone_count = 0

        for milestone in self.milestones_achieved_cycle:
            milestone_text = font_20.render(
                f"{milestone.name}: Achieved", False, (0, 255, 0)
            )
            screen.blit(
                milestone_text,
                (
                    WIDTH // 2 - milestone_text.get_width() // 2,
                    HEIGHT // 2 + (-75 + (milestone_count * 25)),
                ),
            )
            milestone_count += 1

        hq_btn = ui_elements["vab_button"]
        hq_btn = pygame.transform.scale(hq_btn, (150, 50))
        hq_btn_rect = hq_btn.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))
        screen.blit(hq_btn, hq_btn_rect)
        if mouse_collision(pygame, hq_btn_rect):
            cursor_manager.click_cursor()
        hq_btn_text = font_20.render("Headquarters", False, (255, 255, 255))
        hq_btn_text_rect = hq_btn_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))
        screen.blit(hq_btn_text, hq_btn_text_rect)
        main_menu = ui_elements["vab_button"]
        main_menu_btn = pygame.transform.scale(main_menu, (150, 50))
        main_menu_btn_rect = main_menu_btn.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 250)
        )
        screen.blit(main_menu_btn, main_menu_btn_rect)
        if mouse_collision(pygame, main_menu_btn_rect):
            cursor_manager.click_cursor()
        main_menu_btn_text = font_20.render("Main Menu", False, (255, 255, 255))
        main_menu_btn_text_rect = main_menu_btn_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 250)
        )
        screen.blit(main_menu_btn_text, main_menu_btn_text_rect)

    def handle_click(self, pygame, callback):
        hq_btn_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 175, 150, 50)
        if mouse_collision(pygame, hq_btn_rect):
            self.active_contract = None
            self.milestones_achieved_cycle = []
            self.rocket.reset()
            self.player.active_contract = None
            callback("hq")
            self.__init__(self.rocket, self.player)
        if mouse_collision(
            pygame, pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 225, 150, 50)
        ):
            self.active_contract = None
            self.milestones_achieved_cycle = []
            self.player.active_contract = None
            self.rocket.reset()
            self.__init__(self.rocket, self.player)
            callback("main_menu")
