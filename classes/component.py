from pathlib import Path


class Component:
    def __init__(
        self,
        name,
        mass,
        width,
        height,
        x_offset,
        size_scale,
        asset,
        type,
        position,
        stage,
        cost,
        fuel_capacity=0,
        control_surface=False,
        stability_offset=None,
        drag_factor=0,
    ):
        self.mass = mass
        self.width = width
        self.height = height
        self.x_offset = x_offset
        self.size_scale = size_scale
        self.name = name
        self.asset = asset
        self.type = type
        self.stage = stage
        self.cost = cost
        self.fuel_capacity = fuel_capacity
        self.control_surface = control_surface
        self.stability_offset = stability_offset
        self.drag_factor = drag_factor
        self.position = position

    def draw(self, pygame):
        asset_path = "./assets/rocket_components/" + self.type + "/" + self.asset
        asset = pygame.image.load(asset_path).convert_alpha()
        asset = pygame.transform.scale(asset, (self.width, self.height))
        return asset
