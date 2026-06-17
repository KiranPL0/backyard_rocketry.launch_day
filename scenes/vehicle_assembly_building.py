from classes.component_menu import ComponentMenu
from classes.rocket_menu import RocketMenu
from classes.rocket import Rocket
from settings import VAB_ROCKET_LOCATIONS, WIDTH, HEIGHT
from calc.mouse_collision import mouse_collision


def init_side_menu(ui_elements, scene_elements, player, pygame):
    temp_rocket = Rocket()
    component_menu = ComponentMenu(
        ui_elements, scene_elements, player, pygame, temp_rocket
    )
    rocket_menu = RocketMenu(ui_elements, scene_elements, player, pygame, temp_rocket)
    rocket_menu.align_right()
    return component_menu, rocket_menu, temp_rocket


def calculate_cost(temp_rocket):
    total_cost = 0
    if temp_rocket.engine != None:
        total_cost += temp_rocket.engine.cost
    for component in temp_rocket.structure["left"]:
        total_cost += int(component.cost)
    for component in temp_rocket.structure["right"]:
        total_cost += int(component.cost)
    for component in temp_rocket.structure["center"]:
        total_cost += int(component.cost)
    for component in temp_rocket.structure["internal"]:
        total_cost += int(component.cost)
    return total_cost


def draw_vab(
    pygame,
    screen,
    component_menu,
    rocket_menu,
    cursor_manager,
    temp_rocket,
    ui_elements,
):
    component_menu.update_components(pygame)
    from assets.asset_loader import font_30

    screen.blit(
        component_menu.scene_elements["vab"][component_menu.player.stage], (0, 0)
    )
    component_menu.draw(pygame, screen, cursor_manager, temp_rocket)
    rocket_menu.update_list(temp_rocket, ui_elements, pygame)
    rocket_menu.draw(pygame, screen, cursor_manager, temp_rocket)
    temp_rocket.draw_fixed_position_rocket(
        pygame,
        screen,
        VAB_ROCKET_LOCATIONS[component_menu.player.stage][0],
        VAB_ROCKET_LOCATIONS[component_menu.player.stage][1],
        VAB_ROCKET_LOCATIONS[component_menu.player.stage][2],
    )
    if component_menu.warning_tooltip != None:
        warning = font_30.render(component_menu.warning_tooltip, False, (255, 255, 255))
        warning_rect = warning.get_rect(center=(WIDTH // 2, 100))
        screen.blit(warning, warning_rect)
    elif temp_rocket.engine == None:
        warning = font_30.render("Select an engine to start", False, (255, 255, 255))
        warning_rect = warning.get_rect(center=(WIDTH // 2, 100))
        screen.blit(warning, warning_rect)
    else:
        warning = font_30.render(
            "Add components to your rocket", False, (255, 255, 255)
        )
        warning_rect = warning.get_rect(center=(WIDTH // 2, 100))
        screen.blit(warning, warning_rect)
    launch_btn = ui_elements["vab_button"]
    launch_btn = pygame.transform.scale(launch_btn, (200, 75))
    launch_btn_rect = launch_btn.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(launch_btn, launch_btn_rect)
    # cost_panel = ui_elements["rocket_cost_panel"]
    # cost_panel = pygame.transform.scale(cost_panel, (100, 50))
    # cost_panel_rect = cost_panel.get_rect(center=(WIDTH - 150, HEIGHT - 50))
    # screen.blit(cost_panel, cost_panel_rect)
    # cost_text = font_30.render(str(calculate_cost(temp_rocket)), False, (255, 255, 255))
    # # cost_text_rect = cost_text.get_rect(center=()))
    # # screen.blit(cost_text, cost_text_rect)
    if temp_rocket.engine != None:
        launch_btn_text = font_30.render("Launch", False, (255, 255, 255))
    else:
        launch_btn_text = font_30.render("Launch", False, (150, 150, 150))
    launch_btn_text_rect = launch_btn_text.get_rect(center=launch_btn_rect.center)
    screen.blit(launch_btn_text, launch_btn_text_rect)
    if mouse_collision(pygame, launch_btn_rect) and temp_rocket.engine != None:
        cursor_manager.click_cursor()


def handle_launch_press(pygame, temp_rocket, rocket, scene_change_callback, player):
    launch_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 75)
    if mouse_collision(pygame, launch_button_rect) and temp_rocket.engine != None:
        rocket.structure = temp_rocket.structure
        rocket.engine = temp_rocket.engine
        rocket.prep_for_launch()
        temp_rocket.structure = {"left": [], "right": [], "center": [], "internal": []}
        temp_rocket.engine = None
        scene_change_callback("launch")
