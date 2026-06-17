from settings import WIDTH, HEIGHT


def draw_globalHud(pygame, screen, player):
    from assets.asset_loader import ui_elements, font_20

    panel = ui_elements["global_hud"]
    panel = pygame.transform.scale(panel, (250, 60))
    panel_rect = panel.get_rect(center=(WIDTH // 2, 40))
    screen.blit(panel, panel_rect)
    money = font_20.render(str(player.money), False, (255, 255, 255))
    money_rect = money.get_rect(midright=(WIDTH // 2 - 5, 40))
    screen.blit(money, money_rect)
    reputation = font_20.render(str(player.reputation), False, (255, 255, 255))
    reputation_rect = reputation.get_rect(midright=(WIDTH // 2 + 100, 40))
    screen.blit(reputation, reputation_rect)
