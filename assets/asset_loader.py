import json
from classes.engine import Engine
from classes.component import Component
from classes.contract import Contract
from classes.milestone import Milestone
from settings import WIDTH, HEIGHT

fuels = []
engines = []
components = []
unlocked_engines = []
unlocked_components = []
contracts = []
milestones = []
loaded = [False, False, False, False, False, False, False, False, False]
explosion_images = []
ui_elements = {}
scene_elements = {}


# saving fuels to memory
def load_fuels():
    global fuels
    if loaded[0] == False:
        print("Loading fuels into memory...")
        with open("./library/fuels.json", "r") as f:
            fuels_data = json.load(f)
        fuels.clear()
        fuels.extend(fuels_data)
        loaded[0] = True
        print("Fuels loaded into memory")


def load_engines():
    if loaded[1] == False:
        print("Loading engines into memory...")
        with open("./library/engines.json", "r") as f:
            f = json.load(f)
            for a in f:
                engines.append(
                    Engine(
                        a["flow_rate"],
                        a["size_scale"],
                        a["name"],
                        a["material"],
                        a["type"],
                        a["exit_area"],
                        a["exhaust_velocity"],
                        a["asset"],
                        a["height"],
                        a["width"],
                        a["side-offset"],
                        a["fuel_capacity"],
                        a["mass"],
                        a["drag-factor"],
                        a["stage"],
                        a["cost"],
                    )
                )
        loaded[1] = True
        print("Engines loaded into memory")


def load_components():
    if loaded[2] == False:
        print("Loading components into memory...")
        with open("./library/components.json", "r") as f:
            f = json.load(f)
            for a in f:
                components.append(
                    Component(
                        a["name"],
                        a["mass"],
                        a["width"],
                        a["height"],
                        a["x-offset"],
                        a["size_scale"],
                        a["asset"],
                        a["type"],
                        a["position"],
                        a["stage"],
                        a["cost"],
                        a["fuel_capacity"],
                        a["control_surface"],
                        a["stability_offset"],
                        a["drag-factor"],
                    )
                )
        loaded[2] = True
        print("Components loaded into memory")


def load_explosion(pygame):
    if loaded[3] == False:
        print("Loading explosion images into memory...")
        for i in range(10):
            explosion_images.append(
                pygame.image.load(
                    "./assets/explosion/" + str(i) + ".png"
                ).convert_alpha()
            )
        loaded[3] = True
        print("Explosion images loaded into memory")


def load_fonts(pygame):
    if loaded[4] == False:
        print("Loading fonts into memory...")
        global font_10, font_20, font_40, font_60, font_15, font_30

        font_10 = pygame.font.Font("./assets/fonts/PressStart2P-Regular.ttf", 5)
        font_20 = pygame.font.Font("./assets/fonts/PressStart2P-Regular.ttf", 10)
        font_15 = pygame.font.Font("./assets/fonts/PressStart2P-Regular.ttf", 7)
        font_30 = pygame.font.Font("./assets/fonts/PressStart2P-Regular.ttf", 15)
        font_40 = pygame.font.Font("./assets/fonts/PressStart2P-Regular.ttf", 20)
        font_60 = pygame.font.Font("./assets/fonts/PressStart2P-Regular.ttf", 30)
        loaded[4] = True
        print("Fonts loaded into memory")


def load_ui_elements(pygame):
    if loaded[5] == False:
        print("Loading UI elements into memory...")
        global ui_elements
        ui_elements = {}
        ui_elements["context_menu"] = pygame.image.load(
            "./assets/ui/context_menu.png"
        ).convert_alpha()
        ui_elements["text_box"] = pygame.image.load(
            "./assets/ui/text_box.png"
        ).convert_alpha()
        ui_elements["button"] = pygame.image.load(
            "./assets/ui/button.png"
        ).convert_alpha()
        ui_elements["button_hover"] = pygame.image.load(
            "./assets/ui/button_hover.png"
        ).convert_alpha()
        # cursors
        pointer_img = pygame.image.load(
            "./assets/ui/cursors/pointer.png"
        ).convert_alpha()
        pointer_img = pygame.transform.scale(pointer_img, (15, 22))
        ui_elements["cursor_pointer"] = pygame.cursors.Cursor((0, 0), pointer_img)
        clicker_img = pygame.image.load(
            "./assets/ui/cursors/clicker.png"
        ).convert_alpha()
        clicker_img = pygame.transform.scale(clicker_img, (28, 32))
        ui_elements["cursor_clicker"] = pygame.cursors.Cursor((0, 0), clicker_img)
        # context menu icons
        ui_elements["icon_warning"] = pygame.image.load(
            "./assets/ui/icons/warning.png"
        ).convert_alpha()
        ui_elements["side_menu"] = pygame.image.load(
            "./assets/ui/side_menu.png"
        ).convert_alpha()

        # component icons

        ui_elements["icon_vab_forward"] = pygame.image.load(
            "./assets/ui/icons/vab_forward.png"
        ).convert_alpha()
        ui_elements["icon_vab_previous"] = pygame.image.load(
            "./assets/ui/icons/vab_previous.png"
        ).convert_alpha()
        ui_elements["icon_qsac"] = pygame.image.load(
            "./assets/ui/icons/questionably_safe_aerospace_corporation.png"
        ).convert_alpha()

        ui_elements["vab_button"] = pygame.image.load(
            "./assets/ui/vab_button.png"
        ).convert_alpha()

        ui_elements["launch_info_hud"] = pygame.image.load(
            "./assets/ui/launch_info_hud.png"
        ).convert_alpha()
        ui_elements["launch_end"] = pygame.image.load(
            "./assets/ui/launch_end.png"
        ).convert_alpha()
        ui_elements["active_contract_panel"] = pygame.image.load(
            "./assets/ui/active_contract_panel.png"
        ).convert_alpha()
        ui_elements["global_hud"] = pygame.image.load(
            "./assets/ui/global_hud.png"
        ).convert_alpha()
        ui_elements["rocket_cost_panel"] = pygame.image.load(
            "./assets/ui/rocket_cost_panel.png"
        ).convert_alpha()

        ui_elements["icon_local_stem_club"] = pygame.image.load(
            "./assets/ui/icons/local_stem_club.png"
        ).convert_alpha()

        ui_elements["icon_rocket_lab_youth"] = pygame.image.load(
            "./assets/ui/icons/rocket_lab_youth.png"
        ).convert_alpha()

        ui_elements["icon_qsac"] = pygame.image.load(
            "./assets/ui/icons/questionably_safe_aerospace_corporation.png"
        ).convert_alpha()

        ui_elements["icon_cansat_group"] = pygame.image.load(
            "./assets/ui/icons/cansat_group.png"
        ).convert_alpha()

        ui_elements["icon_aero_club"] = pygame.image.load(
            "./assets/ui/icons/aero_club.png"
        ).convert_alpha()

        ui_elements["main_menu_bg"] = pygame.image.load(
            "./assets/scenes/main_menu/bg.png"
        )

        print("UI elements loaded into memory")
        loaded[5] = True


def load_scene_elements(pygame):
    if loaded[6] == False:
        print("Loading scene elements into memory...")
        global scene_elements
        scene_elements = {}
        scene_elements["vab"] = []
        scene_elements["hq"] = []
        for i in range(3):
            img = pygame.image.load("./assets/scenes/vab/" + str(i) + ".png")
            img = pygame.transform.scale(img, (WIDTH, HEIGHT))
            scene_elements["vab"].append(img)
        for i in range(3):
            img = pygame.image.load("./assets/scenes/hq/" + str(i) + ".png")
            img = pygame.transform.scale(img, (WIDTH, HEIGHT))
            scene_elements["hq"].append(img)
        print("Loaded scene elements into memory")
        loaded[6] = True


def import_contracts():
    global contracts
    if loaded[7] == False:
        print("Loading contracts into memory...")
        with open("./library/contracts.json", "r") as f:
            loaded_contracts = json.load(f)
        for contract in loaded_contracts:
            contracts.append(
                Contract(
                    contract["name"],
                    contract["description"],
                    contract["goal"],
                    contract["value"],
                    contract["money"],
                    contract["reputation"],
                    contract["company"],
                    contract["stage"],
                    contract["reputation_required"],
                    contract["unlock_components"],
                    contract["unlock_engines"],
                )
            )
        print("Contracts loaded into memory")
        loaded[7] = True


def import_milestones():
    if loaded[8] == False:
        print("Loading milestones into memory...")
        global milestones
        with open("./library/milestones.json", "r") as f:
            loaded_milestones = json.load(f)
        for milestone in loaded_milestones:
            milestones.append(
                Milestone(
                    milestone["name"],
                    milestone["description"],
                    milestone["goal"],
                    milestone["value"],
                    milestone["money"],
                    milestone["reputation"],
                    milestone["unlock_components"],
                    milestone["unlock_engines"],
                )
            )
        print("Milestones loaded into memory")
        loaded[8] = True


def reset_milestones():
    for milestone in milestones:
        milestone.achieved = False


def update_loaded_engines(player):
    global unlocked_engines
    unlocked_engines.clear()
    for engine in engines:
        if engine.stage <= player.stage:
            unlocked_engines.append(engine)
    for engine in player.unlocked_engines:
        for e in engines:
            if e.name == engine and e not in unlocked_engines:
                unlocked_engines.append(e)


def update_loaded_components(player):
    global unlocked_components
    unlocked_components.clear()
    for component in components:
        if component.stage <= player.stage:
            unlocked_components.append(component)
    for component in player.unlocked_components:
        for c in components:
            if c.name == component and c not in unlocked_components:
                unlocked_components.append(c)


def init_ram(pygame):
    load_fuels()
    load_engines()
    load_components()
    load_fonts(pygame)
    load_scene_elements(pygame)
    import_contracts()
    import_milestones()
