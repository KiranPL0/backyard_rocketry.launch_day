from assets.asset_loader import fuels


class Rocket:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.v_x = 0
        self.v_y = 0
        self.angle = 0
        self.structure = {
            "left": [],
            "center": [],
            "right": [],
            "internal": []
        }
        self.component_space = 0
        self.air_resistance = 0
        self.crew = []
        self.stability = {
            "left": 0,
            "right": 0
        }
        self.propellants = {
            "oxidizer": None,
            "fuel": None
        }
        self.propellant_amount = {
            "oxidizer": 0,
            "fuel": 0
        }
        self.oxidizer_fuel_ratio = [] # oxidizer %, fuel %
        self.propellant_capacity = []
        self.total_volume = 0
        self.total_mass = 0
    def fuel(self, oxidizer_type, fuel_type, mixture):
        for i in fuels:
            if fuels[i]["name"] == oxidizer_type and fuels[i]["type"] == "oxidizer":
                self.propellants["oxidizer"] = fuels[i]
            if fuels[i]["name"] == fuel_type and fuels[i]["type"] == "fuel":
                self.propllants["fuel"] = fuels[i]
        self.oxidizer_fuel_ratio = mixture
        self.propellant_amount["oxidizer"] = self.propellant_capacity * (mixture[0])
        

