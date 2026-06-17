from settings import WIDTH, HEIGHT
from calc.mouse_collision import mouse_collision
from classes.contract_menu import ContractMenu
from classes.milestones_menu import MilestonesMenu


class Headquarters:
    def __init__(self, scene_elements, player, ui_elements, callback):
        self.scene_elements = scene_elements
        self.player = player
        self.ui_elements = ui_elements
        self.go_to_vab_rect = None
        self.contract_menu = ContractMenu(ui_elements, scene_elements, player)
        self.milestones_menu = MilestonesMenu(ui_elements, scene_elements, player)
        self.milestones_menu.align_right()
        self.callback = callback

    def draw(self, pygame, screen, cursor_manager):
        from assets.asset_loader import font_30, font_20, font_15, milestones

        self.milestones_menu.update_milestones_menu()
        self.contract_menu.update_contracts()
        screen.blit(self.scene_elements["hq"][self.player.stage], (0, 0))
        vab_button = self.ui_elements["vab_button"]
        vab_button = pygame.transform.scale(vab_button, (200, 75))
        vab_button_rect = vab_button.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.go_to_vab_rect = vab_button_rect
        screen.blit(vab_button, vab_button_rect)
        vab_button_text = font_30.render("Go to VAB", False, (255, 255, 255))
        vab_button_text_rect = vab_button_text.get_rect(center=vab_button_rect.center)
        screen.blit(vab_button_text, vab_button_text_rect)
        if mouse_collision(pygame, vab_button_rect):
            cursor_manager.click_cursor()

        # milestones side panel
        milestones_side_panel = self.ui_elements["side_menu"]
        milestones_side_panel = pygame.transform.scale(
            milestones_side_panel, (300, 600)
        )
        milestones_side_panel_rect = milestones_side_panel.get_rect(
            center=(WIDTH - 160, 360)
        )
        screen.blit(milestones_side_panel, milestones_side_panel_rect)
        milestones_text = font_30.render("Milestones", False, (255, 255, 255))
        milestones_text_rect = milestones_text.get_rect(
            center=(
                milestones_side_panel_rect.centerx,
                milestones_side_panel_rect.top + 40,
            )
        )
        screen.blit(milestones_text, milestones_text_rect)
        # display milestones

        for i in range(len(milestones)):
            milestone = milestones[i]
            milestone_text = font_20.render(
                f"{i+1}. {milestone.name}", False, (255, 255, 255)
            )
            milestone_text_rect = milestone_text.get_rect(
                topleft=(
                    milestones_side_panel_rect.left + 30,
                    milestones_side_panel_rect.top + 70 + i * 60,
                )
            )
            screen.blit(milestone_text, milestone_text_rect)
            milestone_description = font_15.render(
                milestone.description, False, (230, 230, 230)
            )
            milestone_description_rect = milestone_description.get_rect(
                topleft=(
                    milestones_side_panel_rect.left + 30,
                    milestones_side_panel_rect.top + 90 + i * 60,
                )
            )
            screen.blit(milestone_description, milestone_description_rect)
            milestone_status = milestone.check_achivement_list(self.player)
            if milestone_status:
                status_text = font_15.render("Status: Not Achieved", False, (255, 0, 0))
            else:
                status_text = font_15.render("Status: Achieved", False, (0, 255, 0))
            status_text_rect = status_text.get_rect(
                topleft=(
                    milestones_side_panel_rect.left + 30,
                    milestones_side_panel_rect.top + 110 + i * 60,
                )
            )
            screen.blit(status_text, status_text_rect)
        if self.player.active_contract == None:
            self.contract_menu.draw(pygame, screen, cursor_manager)
        else:
            panel = self.ui_elements["active_contract_panel"]
            panel = pygame.transform.scale(panel, (400, 200))
            screen.blit(panel, (10, 10))
            panel_text = font_30.render("Active Contract", False, (255, 255, 255))
            panel_text_rect = panel_text.get_rect(center=(210, 60))
            screen.blit(panel_text, panel_text_rect)
            contract_name_text = font_15.render(
                f"Contract: {self.player.active_contract.name}", False, (255, 255, 255)
            )
            contract_name_text_rect = contract_name_text.get_rect(topleft=(45, 80))
            screen.blit(contract_name_text, contract_name_text_rect)
            contract_description_text = font_15.render(
                self.player.active_contract.description, False, (230, 230, 230)
            )
            contract_description_text_rect = contract_description_text.get_rect(
                topleft=(45, 100)
            )
            screen.blit(contract_description_text, contract_description_text_rect)
            contract_reward_text = font_15.render(
                f"Reward: ${self.player.active_contract.money}", False, (255, 255, 255)
            )
            contract_reward_text_rect = contract_reward_text.get_rect(topleft=(45, 120))
            screen.blit(contract_reward_text, contract_reward_text_rect)
            contract_reward_reputation_text = font_15.render(
                f"Reputation: {self.player.active_contract.reputation}",
                False,
                (255, 255, 255),
            )
            contract_reward_reputation_text_rect = (
                contract_reward_reputation_text.get_rect(topleft=(45, 140))
            )
            screen.blit(
                contract_reward_reputation_text, contract_reward_reputation_text_rect
            )
        self.milestones_menu.draw(pygame, screen, cursor_manager)

    def handle_click(self, pygame):
        if self.player.active_contract == None:
            self.contract_menu.handle_click(pygame)
        if self.go_to_vab_rect != None:
            if mouse_collision(pygame, self.go_to_vab_rect):
                self.callback("vab")
        self.milestones_menu.handle_click(pygame)
