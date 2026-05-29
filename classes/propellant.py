class Propellant:
    def __init__(self, name, state, mixture, density, purity, type):
        self.name = name
        self.state = state
        self.density = density
        self.purity = purity
        self.type = type # oxidizer or fuel
