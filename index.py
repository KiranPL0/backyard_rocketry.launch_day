import pygame
from scenes.story import Story
from settings import WIDTH, HEIGHT, STAGE_THRESHOLDS
from assets.asset_loader import init_ram, load_fonts
from classes.rocket import Rocket
from assets.asset_loader import loaded, load_explosion, load_ui_elements
from classes.camera import Camera
from calc.background import draw_background
from calc.stars import generate_star_surface
from calc.clouds import generate_clouds
from calc.draw_thrust import init_thrust_images
from calc.ground import init_texture, draw_ground
from calc.save import save_game, load_game
from classes.player import Player
from classes.context_menu import (
    SaveGameContextMenu,
    WarningContextMenu,
    LoadGameContextMenu,
)
from scenes.vehicle_assembly_building import (
    draw_vab,
    init_side_menu,
    handle_launch_press,
)
from classes.cursor_manager import CursorManager
from gui.launch_hud import draw_launch_hud
from classes.launch_complete import LaunchComplete
from assets.asset_loader import update_loaded_engines, update_loaded_components
from scenes.headquarters import Headquarters
from classes.contract_menu import ContractMenu
from gui.global_hud import draw_globalHud
from scenes.main_menu import MainMenu

#################################### CLASSES ##################################


#################################### FUNCTIONS ################################


#################################### GLOBAL VARIABLES #########################
pygame.init()
init_ram(pygame)
# You may change the width and height of your window
icon = pygame.image.load("./assets/images/icon.ico")
icon = pygame.transform.scale(icon, (64, 64))
pygame.display.set_icon(icon)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Backyard Rocketry: Launch Day")

star_surface = generate_star_surface(pygame)

load_explosion(pygame)


MISSION_END_CONTRACT_STATE = None

clock = pygame.time.Clock()

camera = Camera()

rocket = Rocket()

clouds = generate_clouds(pygame, 200)

init_thrust_images(pygame)
init_texture(pygame)

player = Player()

game_focus = True

## font ##
load_fonts(pygame)
load_ui_elements(pygame)
## cursor ##
from assets.asset_loader import ui_elements, scene_elements

current_scene = "main_menu"  # main_menu, vab, launch, hq, story

cursor_manager = CursorManager()

update_loaded_engines(player)
update_loaded_components(player)


## game loop function ##
def unfocus_game():
    global game_focus
    game_focus = False


def focus_game():
    global game_focus
    game_focus = True


def open_load_menu():
    load_game_menu.hidden = False
    unfocus_game()


def check_update_stage():
    global player
    global current_scene
    if player.stage < 2:
        next_stage = player.stage + 1
        if (
            player.reputation >= STAGE_THRESHOLDS[next_stage]
            and current_scene != "story"
            and current_scene != "launch"
        ):
            player.stage = next_stage
            if player.stage == 1:
                scene_zero_one_transition()
                story.line_finish_callback = lambda: scene_change_callback("hq")
            elif player.stage == 2:
                scene_one_two_transition()
                story.line_finish_callback = lambda: scene_change_callback("hq")


def scene_change_callback(scene):
    global current_scene
    current_scene = scene


def scene_zero_one_transition():
    global current_scene
    global story
    global player
    story = Story(
        [
            "Your rocket hobby project has taken off!",
            "The media calls you the backyard rocket scientist.",
            "Your neighbours call you crazy.",
            "So, you decide to start your own rocket company.",
            "Northridge Aerospace is born.",
        ]
    )
    current_scene = "story"
    player.stage = 1


def scene_one_two_transition():
    global current_scene
    global story
    global player
    story = Story(
        [
            "Northridge Aerospace takes off (literally).",
            "You've made enough money and have built a large reputation.",
            "You decide to expand your company.",
            "You start working towards your final goal...",
            "...Orbital Flight!",
        ],
    )
    current_scene = "story"
    player.stage = 2


def spacecutscene():
    global current_scene
    global story
    global player
    story = Story(
        [
            "You have successfully made it to orbit.",
            "You owe yourself a pat on the back.",
            "Congratulations! You have completed Backyard Rocketry: Launch Day!",
            "I hope you enjoyed playing this game.",
        ],
    )
    current_scene = "story"
    story.line_finish_callback = lambda: scene_change_callback("main_menu")


save_game_menu = SaveGameContextMenu(focus_game, unfocus_game)

load_game_menu = LoadGameContextMenu(focus_game, unfocus_game)
# save_game_menu.hidden = False

warning_modal = WarningContextMenu(
    "Warning", "Save file does not exist", focus_game, unfocus_game
)

component_menu, rocket_menu, temp_rocket = init_side_menu(
    ui_elements, scene_elements, player, pygame
)


mission_end_screen = LaunchComplete(rocket, player)

headquarters = Headquarters(scene_elements, player, ui_elements, scene_change_callback)

main_menu = MainMenu(lambda: scene_change_callback("story"))

story = Story(
    [
        "Welcome to Backyard Rocketry: Launch Day!",
        "Your mission is to build and launch rockets.",
        "You'll have to complete contracts to earn money.",
        "Build rockets in the VAB, and launch them!",
        "You'll progress, growing your rocketry program.",
        "Reaching milestones will help you progress further.",
        "Earning reputation yields better contracts.",
        "You'll unlock parts by progressing through the game.",
        "Your ultimate goal is to achieve orbital flight!",
        "Good luck, and have fun playing!",
    ],
    line_finish_callback=lambda: scene_change_callback("hq"),
)

#################################### GAME LOOP ################################
running = True
full_loaded = False
built = False
while running:
    check_update_stage()
    cursor_manager.reset_cursor()
    # ============================== HANDLE EVENTS  ========================= #
    update_loaded_engines(player)
    update_loaded_components(player)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and current_scene == "story":
                scene_change_callback("hq")
            if event.key == pygame.K_e and current_scene == "launch":
                rocket.end_flight()
            if event.key == pygame.K_a and current_scene == "launch":
                rocket.move("left")
            if event.key == pygame.K_d and current_scene == "launch":
                rocket.move("right")
            if event.key == pygame.K_s and game_focus and current_scene == "launch":
                rocket.sas_active = not rocket.sas_active
                # print("SAS: " + str(rocket.sas_active))
            if game_focus == False and save_game_menu.hidden == False:
                save_game_menu.text_update(pygame, event)
            if game_focus == False and load_game_menu.hidden == False:
                load_game_menu.text_update(pygame, event)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a and current_scene == "launch":
                rocket.stop_moving()
            if event.key == pygame.K_d and current_scene == "launch":
                rocket.stop_moving()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_focus == False and save_game_menu.hidden == False:
                button_status = save_game_menu.button_update(pygame, event)
                if button_status != None:
                    save_game(button_status, player, rocket)
            if game_focus == False and warning_modal.hidden == False:
                warning_modal.button_update(pygame, event)
            if game_focus == False and load_game_menu.hidden == False:
                button_status = load_game_menu.button_update(pygame, event)
                if button_status != None:
                    try:
                        player = load_game(button_status, rocket)
                    except FileNotFoundError:
                        unfocus_game()
                        load_game_menu.hidden = True
                        warning_modal.update_content(
                            "Error", "Save file does not exist"
                        )
                        warning_modal.hidden = False
                        warning_modal.set_acknowledge_callback(open_load_menu)
            if component_menu.visible == True and current_scene == "vab":
                component_menu.handle_click(pygame)
            if rocket_menu.visible == True and current_scene == "vab":
                rocket_menu.handle_click(pygame)
            if current_scene == "vab":
                handle_launch_press(
                    pygame, temp_rocket, rocket, scene_change_callback, player
                )

            if (
                current_scene == "launch"
                and rocket.running == False
                and rocket.flight_complete == True
            ):
                mission_end_screen.handle_click(pygame, scene_change_callback)
            if current_scene == "hq":
                headquarters.handle_click(pygame)
            if current_scene == "main_menu":
                main_menu.handle_click(pygame)

    if not running:
        break
        # INSERT EVENTS HERE

    if (
        loaded[0]
        and loaded[1]
        and loaded[2]
        and loaded[3]
        and loaded[4]
        and loaded[5]
        and loaded[6]
        and loaded[7]
        and loaded[8]
    ):
        full_loaded = True

    # ============================== CALCULATE TIME ========================= $
    if full_loaded:
        dt = clock.tick(60) / 1000  # 60 updates/second

    # ============================== MOVE STUFF ============================= #

    # ============================== COLLISION ============================== #
    if full_loaded == True and built == False:
        # player = load_game("first_save", rocket)
        # player = Player("kiran")
        # rocket.attach_engine("candy-rocket")
        # rocket.add_component("cardboard_fuselage", "center")
        # rocket.add_component("cardboard_nose_cone", "center")
        # rocket.add_component("cardboard_fin_left", "left")
        # rocket.add_component("cardboard_fin_right", "right")
        # rocket.check_SAS()
        # rocket.fuel("Ammonium Perchlorate", "Aluminum Powder", [0.5, 0.5])
        # rocket.calculate_mass()
        # rocket.calculate_drag()
        # rocket.set_real_y()
        built = True

    # ============================== DRAW STUFF ============================= #
    if full_loaded:
        if current_scene == "launch":
            draw_background(screen, rocket, star_surface, clouds, camera)
            ground = draw_ground(pygame, screen, camera)
            rocket.throttle = 1
            if game_focus:
                camera.follow_object(rocket.x, rocket.y)
                rocket.draw_rocket(pygame, screen, camera, dt)
                rocket.update(
                    pygame, dt, camera, ground, mission_end_screen, spacecutscene
                )
                draw_launch_hud(pygame, screen, rocket)
                if rocket.running == False and rocket.flight_complete == True:
                    mission_end_screen.draw(
                        pygame, screen, rocket, ui_elements, player, cursor_manager
                    )
            draw_globalHud(pygame, screen, player)
        if current_scene == "vab":
            draw_vab(
                pygame,
                screen,
                component_menu,
                rocket_menu,
                cursor_manager,
                temp_rocket,
                ui_elements,
            )
            draw_globalHud(pygame, screen, player)
        if current_scene == "test":
            draw_launch_hud(pygame, screen, rocket)
            mission_end_screen.draw_mission_end(
                pygame,
                screen,
                rocket,
                ui_elements,
                player,
                cursor_manager,
            )
            draw_globalHud(pygame, screen, player)
        if current_scene == "hq":
            headquarters.draw(pygame, screen, cursor_manager)
            draw_globalHud(pygame, screen, player)
        if current_scene == "story":
            story.draw(pygame, screen, dt)
        if current_scene == "main_menu":
            main_menu.draw(pygame, screen, cursor_manager)
        load_game_menu.draw(pygame, screen)
        save_game_menu.draw(pygame, screen)
        warning_modal.draw(pygame, screen)
        # print("Altitude: " + str(rocket.y) + " m")
        # print("Vertical Velocity: " + str(rocket.v_y) + " m/s")
        # # print(rocket.propellant_amount['oxidizer'])
        # print(rocket.propellant_amount['fuel'])
    # ============================== PYGAME STUFF (DO NOT EDIT) ============= #
    cursor_manager.apply_cursor(pygame, ui_elements)
    pygame.display.flip()
pygame.quit()
