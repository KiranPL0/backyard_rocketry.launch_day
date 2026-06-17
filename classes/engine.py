from pathlib import Path


class Engine:
    def __init__(
        self,
        flow_rate,
        size_scale,
        name,
        material,
        type,
        exit_area,
        exhaust_velocity,
        asset,
        height,
        width,
        side_offset,
        fuel_capacity,
        mass,
        drag_factor,
        stage,
        cost,
    ):
        self.max_flow_rate = flow_rate
        self.size_scale = size_scale
        self.name = name
        self.material = material
        self.type = type
        self.exit_area = exit_area
        self.exhaust_velocity = exhaust_velocity
        self.asset = asset
        self.height = height
        self.width = width
        self.side_offset = side_offset
        self.fuel_capacity = fuel_capacity
        self.mass = mass
        self.drag_factor = drag_factor
        self.stage = stage
        self.cost = cost

    def draw(self, pygame):
        asset_path = "./assets/rocket_components/engine/" + self.asset
        asset = pygame.image.load(asset_path).convert_alpha()
        asset = pygame.transform.scale(asset, (self.width, self.height))
        return asset
