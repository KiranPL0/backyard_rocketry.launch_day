import json
from classes.player import Player

save_buffer_template = {"version:": 1, "player_data": None, "rocket_designs": []}


save_buffer = save_buffer_template.copy()


def get_player_data(player):
    return player.export_data()


def import_player_data(data):
    return Player(
        money=data["money"],
        reputation=data["reputation"],
        active_contract=data["active_contract"],
        completed_contracts=data["completed_contracts"],
        stage=data["stage"],
        unlocked_components=data["unlocked_components"],
        unlocked_engines=data["unlocked_engines"],
        xp=data["xp"],
        launches=data["launches"],
        career_apogee=data["career_apogee"],
        career_max_velocity=data["career_max_velocity"],
        milestones_completed=data["milestones_completed"],
    )


def import_rocket_data(rocket, data):
    rocket.propellant_amount = data["propellant_amount"]
    rocket.propellants = data["propellants"]
    for i in data["structure"]["center"]:
        rocket.add_component(i, "center")
    for i in data["structure"]["left"]:
        rocket.add_component(i, "left")
    for i in data["structure"]["right"]:
        rocket.add_component(i, "right")
    for i in data["structure"]["internal"]:
        rocket.add_component(i, "internal")
    rocket.attach_engine(data["engine"])
    rocket.oxidizer_fuel_ratio = data["oxidizer_fuel_ratio"]
    rocket.propellant_amount = data["propellant_amount"]
    rocket.propellant_capacity = data["propellant_capacity"]
    rocket.calculate_mass()
    rocket.calculate_drag()
    rocket.set_real_y()
    rocket.check_SAS()


def save_player_data(player):
    global save_buffer
    save_buffer["player_data"] = get_player_data(player)


def save_current_rocket(rocket):
    global save_buffer
    save_buffer["rocket_designs"] = rocket.export_data()


def save_game(save_name, player, rocket):
    global save_buffer
    save_player_data(player)
    save_current_rocket(rocket)
    with open("./saves/" + save_name + ".BR_save", "w") as f:
        json.dump(save_buffer, f)


def load_game(save_name, rocket):
    with open("./saves/" + save_name + ".BR_save", "r") as f:
        data = json.load(f)
    player = import_player_data(data["player_data"])
    import_rocket_data(rocket, data["rocket_designs"])
    return player
