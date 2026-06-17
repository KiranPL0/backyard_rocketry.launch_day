import math
import random
from assets.asset_loader import fuels
from assets.asset_loader import engines
from assets.asset_loader import components
from calc import ground
from calc.thrust import calculate_thrust
from calc.kinematics import acceleration_components
from classes import camera
from classes.spacer import Spacer
from classes.component import Component
from calc.atmosphere import drag_density
from settings import ANGULAR_DAMPING, GRAVITY_CONSTANT
from calc.draw_thrust import (
    get_thrust_object,
    change_thrust_object,
    change_burn_out_object,
    get_burn_out_object,
)
from calc.collision import pixelPerfectCollision
from classes.explosion import Explosion
from calc.energy import calculateExplosionEnergy


class Rocket:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.v_x = 0
        self.v_y = 0
        self.angle = 0  # angle from 90* to horizontal
        self.structure = {
            "left": [],
            "center": [],  # index 0 represents bottom of rocket, attatched to engine
            "right": [],
            "internal": [],
        }
        self.component_space = 0
        self.air_resistance = 0  # drag coefficient
        self.crew = []
        self.stability = {"left": 0, "right": 0}
        self.propellants = {"oxidizer": None, "fuel": None}
        self.propellant_amount = {"oxidizer": 0, "fuel": 0}  # in kgs
        self.oxidizer_fuel_ratio = []  # oxidizer %, fuel %
        self.propellant_capacity = 0
        self.total_volume = 0
        self.total_mass = 0
        self.throttle = 0
        self.acceleration = 0
        self.angular_velocity = 0
        self.max_alt = 0
        self.max_v = 0
        self.engine = None
        self.thrust_timer = 0
        self.thrust_frame_duration = 0.12  # seconds
        self.burning_out = False
        self.burn_complete = False
        self.burn_out_frame_duration = 0.12  # seconds
        self.stability_control_module_present = False
        self.sas_active = False
        self.rocket_surface = None
        self.explosion = None
        self.explosion_timer = 0
        self.running = True
        self.flight_complete = False
        self.flight_computer = None
        self.dry_mass = 0
        self.delta_v = 0
        self.begin_moving = None
        self.has_control_surface = False
        self.orbit = False

    def fuel(self, oxidizer_type, fuel_type, mixture):
        self.calculate_propellant_capacity()
        for i in fuels:
            if i["name"] == oxidizer_type and i["type"] == "oxidizer":
                self.propellants["oxidizer"] = i
            if i["name"] == fuel_type and i["type"] == "fuel":
                self.propellants["fuel"] = i
        self.oxidizer_fuel_ratio = mixture
        self.propellant_amount["oxidizer"] = self.propellant_capacity * (mixture[0])
        self.propellant_amount["fuel"] = self.propellant_capacity * (mixture[1])

    def check_control_surface(self):
        self.has_control_surface = False
        for i in self.structure["left"]:
            if isinstance(i, Component) and i.control_surface == True:
                self.has_control_surface = True
                return True
        for i in self.structure["right"]:
            if isinstance(i, Component) and i.control_surface == True:
                self.has_control_surface = True
                return True

    def move(self, direction):
        if direction == "left" and self.has_control_surface:
            self.begin_moving = "left"
        if direction == "right" and self.has_control_surface:
            self.begin_moving = "right"

    def stop_moving(self):
        self.begin_moving = None

    def attach_engine(self, name):
        for i in engines:
            if i.name == name:
                self.engine = i

    def end_flight(self):
        self.running = False
        self.flight_complete = True

    def calculate_TWR(self):
        if self.engine != None and self.total_mass != 0:
            thrust = calculate_thrust(
                self.engine.max_flow_rate,
                self.engine.exhaust_velocity,
                self.propellants["fuel"]["purity"],
                self.propellants["oxidizer"]["purity"],
            )
            weight = self.total_mass * GRAVITY_CONSTANT
            return thrust / weight
        else:
            return 0

    def calculate_delta_v(self):
        if self.engine != None and self.total_mass != 0 and self.dry_mass != 0:
            self.delta_v = self.engine.exhaust_velocity * math.log(
                self.total_mass / self.dry_mass
            )
        else:
            self.delta_v = 0

    def calculate_apogee(self):
        # using vf^2 = vi^2 + 2*a*d
        # rearrange being (vf^2 - vi^2)/2a (where a = g)
        apogee = (0 - self.v_y**2) / (2 * -GRAVITY_CONSTANT)
        return apogee + self.y

    def calculate_time_to_apogee(self):
        time = self.v_y / GRAVITY_CONSTANT
        return time

    def set_real_y(self):
        _, height, _ = self.get_rocket_dimensions()
        flame_buffer = self.engine.width * (7 / 3)
        # Position the rocket so its engine bottom sits at world y = 0.
        # The rocket surface includes a flame buffer below the engine,
        # so use half the body height and half the flame buffer.
        self.y = (height / 2) - (flame_buffer / 2)

    def checkFlightComputer(self):
        for i in self.structure["internal"]:
            if (
                i.name == "basic_flight_computer"
                or i.name == "advanced_flight_computer"
            ):
                self.flight_computer = i
            else:
                self.flight_computer = None

    def calculate_drag(self):
        self.air_resistance = 0
        self.air_resistance += self.engine.drag_factor
        for i in self.structure["center"]:
            if isinstance(i, Component):
                self.air_resistance += i.drag_factor
        for i in self.structure["left"]:
            if isinstance(i, Component):
                self.air_resistance += i.drag_factor
        for i in self.structure["right"]:
            if isinstance(i, Component):
                self.air_resistance += i.drag_factor

    def check_stability(self):
        stability = {"left": 0, "right": 0}
        for i in self.structure["left"]:
            if isinstance(i, Component):
                stability["left"] += i.stability_offset
        for i in self.structure["right"]:
            if isinstance(i, Component):
                stability["right"] += i.stability_offset
        self.stability = stability

    def update(self, pygame, dt, camera, ground, mission_end_screen, end_cutscene):
        if self.y < -100:
            self.handle_impact((self.x, self.y), camera)
            mission_end_screen.check_mission_end()
            self.running = False

        if self.running == True:
            if self.y > 100000:
                self.orbit = True
                mission_end_screen.check_mission_end()
                self.end_flight()
                end_cutscene()
                # finally made it
            self.calculate_mass()
            self.calculate_delta_v()
            self.calculate_apogee()
            self.calculate_time_to_apogee()
            self.calculate_TWR()
            has_fins = self.stability["left"] > 0 and self.stability["right"] > 0
            has_sas = self.stability_control_module_present and self.sas_active
            if self.begin_moving == "left":
                self.angle -= 0.01
            elif self.begin_moving == "right":
                self.angle += 0.01

            if has_sas or (
                (self.stability["left"] - self.stability["right"]) == 0 and has_fins
            ):
                self.angular_velocity = 0
            else:
                torque = random.random() * 0.2 - 0.1 * ANGULAR_DAMPING
                self.angular_velocity += torque * dt
                self.angle += self.angular_velocity * dt
            if (
                self.throttle > 0
                and self.propellant_amount["fuel"] > 0
                and self.propellant_amount["oxidizer"] > 0
            ):
                flow_rate = self.engine.max_flow_rate * self.throttle
                self.propellant_amount["fuel"] -= flow_rate * dt
                self.propellant_amount["oxidizer"] -= flow_rate * dt
                if self.propellant_amount["fuel"] < 0:
                    self.propellant_amount["fuel"] = 0
                if self.propellant_amount["oxidizer"] < 0:
                    self.propellant_amount["oxidizer"] = 0
                # print(self.propellants['fuel'])
                thrust = calculate_thrust(
                    flow_rate,
                    self.engine.exhaust_velocity,
                    self.propellants["fuel"]["purity"],
                    self.propellants["oxidizer"]["purity"],
                )
                # print(self.propellant_amount['fuel'], self.propellant_amount['oxidizer'])
                a_x, a_y = acceleration_components(thrust, self.angle)
                a_x *= 1 + (self.stability["left"] - self.stability["right"])
            else:
                if self.burn_complete == False and self.burning_out == False:
                    self.thrust_timer = 0
                    self.burning_out = True
                if (
                    self.stability_control_module_present == False
                    or self.sas_active == False
                ):
                    self.angular_velocity += (
                        random.randint(-50, 50) * ANGULAR_DAMPING * dt
                    )
                a_x, a_y = acceleration_components(0, self.angle)
            scalar_velocity = math.sqrt(
                self.v_x**2 + self.v_y**2
            )  # v = (vx^2 + vy^2)^1/2

            a_drag_x = 0
            a_drag_y = 0
            if scalar_velocity != 0:
                f_drag = (
                    0.5
                    * self.air_resistance
                    * (scalar_velocity**2)
                    * drag_density(self.y)
                )

                f_drag_x = -f_drag * (self.v_x / scalar_velocity)  # trig ratio
                f_drag_y = -f_drag * (self.v_y / scalar_velocity)

                a_drag_x = f_drag_x / self.total_mass
                a_drag_y = f_drag_y / self.total_mass

            a_x += a_drag_x
            a_y += a_drag_y
            self.v_x += a_x * dt
            self.v_y += a_y * dt
            self.x += self.v_x * dt
            self.y += self.v_y * dt
            self.max_alt = max(self.max_alt, self.y)
            if self.y > 0:
                self.max_v = max(self.max_v, scalar_velocity)
            rocket_rect = self.rocket_surface.get_rect(
                center=(
                    camera.world_to_screen(self.x, self.y)[0],
                    camera.world_to_screen(self.x, self.y)[1],
                )
            )
            ground_x, ground_y = camera.world_to_screen(-5000, 0)

            if self.v_y <= 0:
                collision = pixelPerfectCollision(
                    pygame,
                    self.rocket_surface,
                    ground,
                    rocket_rect.left,
                    rocket_rect.top,
                    ground_x,
                    ground_y,
                )
                if collision != None:
                    self.handle_impact(collision, camera)
                    mission_end_screen.check_mission_end()
                    self.running = False

        # check collision

    def handle_impact(self, collision, camera):
        if self.explosion == None:
            explosion_energy = calculateExplosionEnergy(
                self.total_mass, self.v_x, self.v_y
            )
            ground_x, ground_y = camera.world_to_screen(-5000, 0)
            screen_x = collision[0] + ground_x
            screen_y = collision[1] + ground_y
            world_x, world_y = camera.screen_to_world(screen_x, screen_y)
            self.explosion = Explosion(world_x, world_y, explosion_energy)

    def get_rocket_dimensions(self):
        width = self.engine.width
        left_shift = 0
        for i in self.structure["left"]:
            if isinstance(i, Component):
                width += i.width
                left_shift += i.width
        for i in self.structure["right"]:
            if isinstance(i, Component):
                width += i.width
        height = self.engine.height
        for i in self.structure["center"]:
            if isinstance(i, Component):
                height += i.height
        return width, height, left_shift  # height is buffered

    def get_rocket_dimensions_with_component(self, component):
        width = self.engine.width
        left_shift = 0
        for i in self.structure["left"]:
            if isinstance(i, Component):
                width += i.width
                left_shift += i.width
        for i in self.structure["right"]:
            if isinstance(i, Component):
                width += i.width
        height = self.engine.height
        for i in self.structure["center"]:
            if isinstance(i, Component):
                height += i.height
        if component.position == "center":
            height += component.height
        return width, height, left_shift  # height is buffered

    def add_component(self, name):  # bottom up
        for i in components:
            if i.name == name:
                self.structure[i.position].append(i)
                if i.stability_offset != None:
                    self.stability[i.position] += i.stability_offset
                break

    def get_component(self, name):
        for i in components:
            if i.name == name:
                return i

    def prep_for_launch(self):
        self.check_SAS()
        print("fuelling rocket...")
        self.fuel("Ammonium Perchlorate", "Aluminum Powder", [0.5, 0.5])
        self.calculate_mass()
        self.calculate_drag()
        self.set_real_y()
        self.checkFlightComputer()
        self.check_stability()
        self.check_control_surface()

    def remove_component(self, name):
        for i in self.structure["center"]:
            if isinstance(i, Component) and i.name == name:
                self.structure["center"].remove(i)
                return
        for i in self.structure["left"]:
            if isinstance(i, Component) and i.name == name:
                self.structure["left"].remove(i)
                return
        for i in self.structure["right"]:
            if isinstance(i, Component) and i.name == name:
                self.structure["right"].remove(i)
                return
        for i in self.structure["internal"]:
            if isinstance(i, Component) and i.name == name:
                self.structure["internal"].remove(i)
                return

    def add_spacer(self, height, location, width=1):
        self.structure[location].append(Spacer(height, width))

    def calculate_propellant_capacity(self):
        capacity = self.engine.fuel_capacity
        for i in self.structure["center"]:
            if isinstance(i, Component):
                capacity += i.fuel_capacity
        for i in self.structure["left"]:
            if isinstance(i, Component):
                capacity += i.fuel_capacity
        for i in self.structure["right"]:
            if isinstance(i, Component):
                capacity += i.fuel_capacity
        self.propellant_capacity = capacity

    def calculate_mass(self):
        mass = self.engine.mass
        for i in self.structure["center"]:
            if isinstance(i, Component):
                mass += i.mass
        for i in self.structure["left"]:
            if isinstance(i, Component):
                mass += i.mass
        for i in self.structure["right"]:
            if isinstance(i, Component):
                mass += i.mass
        for i in self.structure["internal"]:
            if isinstance(i, Component):
                mass += i.mass
        self.dry_mass = mass
        self.total_mass = (
            mass + self.propellant_amount["fuel"] + self.propellant_amount["oxidizer"]
        )

    def draw_explosion(self, pygame, screen, camera, dt):
        if self.explosion != None:
            self.explosion.draw(pygame, screen, camera)
            if self.explosion_timer > self.explosion.frame_duration:
                self.explosion_timer = 0
                if self.explosion.next_frame() == "REMOVE":
                    self.flight_complete = True
                    self.explosion = None
                    self.explosion_timer = 0
            self.explosion_timer += dt

    def check_SAS(self):
        for i in self.structure["internal"]:
            if (
                i.name == "stability_control_module"
                or i.name == "stability_ctrl_module"
            ):
                self.stability_control_module_present = True
                return True
        self.stability_control_module_present = False
        return False

    def check_component(self, name):
        for i in self.structure["center"]:
            if isinstance(i, Component) and i.name == name:
                return True
        for i in self.structure["left"]:
            if isinstance(i, Component) and i.name == name:
                return True
        for i in self.structure["right"]:
            if isinstance(i, Component) and i.name == name:
                return True
        for i in self.structure["internal"]:
            if isinstance(i, Component) and i.name == name:
                return True
        return False

    def draw_rocket(self, pygame, screen, camera, dt):

        rocket_width, rocket_height, rocket_left_shift = self.get_rocket_dimensions()
        flame_buffer = self.engine.width * (7 / 3)
        body_surface = pygame.Surface(
            (rocket_width, rocket_height + flame_buffer), pygame.SRCALPHA
        )
        flame_surface = pygame.Surface(
            (rocket_width, rocket_height + flame_buffer), pygame.SRCALPHA
        )
        # body first
        base_x = rocket_left_shift
        base_y = rocket_height - self.engine.height
        current_x = base_x
        current_y = base_y

        asset = self.engine.draw(pygame)
        body_surface.blit(asset, (current_x, current_y))
        for i in self.structure["center"]:
            asset = i.draw(pygame)
            current_x += i.x_offset
            current_y -= i.height - 5
            if current_y < 0:
                return "OOR"
            body_surface.blit(asset, (current_x, current_y))
        current_x = base_x
        current_y = base_y
        current_x += self.engine.side_offset
        for i in self.structure["left"]:
            if isinstance(i, Component):
                asset = i.draw(pygame)
                if current_y < 0:
                    return "OOR"
                body_surface.blit(asset, ((current_x - i.width), current_y))
                current_y -= i.height
            if isinstance(i, Spacer):
                current_y -= Spacer.height
                if current_y < 0:
                    return "OOR"
        current_x = base_x
        current_y = base_y
        current_x -= self.engine.side_offset
        for i in self.structure["right"]:
            if isinstance(i, Component):
                asset = i.draw(pygame)
                body_surface.blit(
                    asset,
                    (
                        self.structure["center"][0].width + current_x + i.x_offset,
                        current_y,
                    ),
                )
                current_y -= i.height
                if current_y < 0:
                    return "OOR"
            if isinstance(i, Spacer):
                current_y -= Spacer.height
                if current_y < 0:
                    return "OOR"

        if (
            self.throttle > 0
            and self.propellant_amount["fuel"] > 0
            and self.propellant_amount["oxidizer"] > 0
        ):
            self.thrust_timer += dt
            if self.thrust_timer > self.thrust_frame_duration:
                self.thrust_timer = 0
                change_thrust_object()
            thrust_object = get_thrust_object(pygame, self.engine.width)
            flame_surface.blit(thrust_object, (base_x, base_y + self.engine.height))
        else:
            if self.burn_complete == False and self.burning_out == True:
                self.thrust_timer += dt
                if self.thrust_timer > self.burn_out_frame_duration:
                    self.thrust_timer = 0
                    self.burn_complete = change_burn_out_object()
                if self.burn_complete == False:
                    thrust_object = get_burn_out_object(pygame, self.engine.width)
                    flame_surface.blit(
                        thrust_object, (base_x, base_y + self.engine.height)
                    )

        rotated_body = pygame.transform.rotate(body_surface, -math.degrees(self.angle))
        rotated_flame = pygame.transform.rotate(
            flame_surface, -math.degrees(self.angle)
        )
        real_x, real_y = camera.world_to_screen(self.x, self.y)
        rocket_rect = rotated_body.get_rect(center=(real_x, real_y))
        flame_rect = rotated_flame.get_rect(center=(real_x, real_y))
        self.rocket_surface = rotated_body
        self.flame_surface = rotated_flame
        screen.blit(rotated_flame, flame_rect)
        screen.blit(rotated_body, rocket_rect)
        self.draw_explosion(pygame, screen, camera, dt)
        return "OK"

    def export_data(self):
        propellant_amount = {"oxidizer": None, "fuel": None}
        propellant_amount["oxidizer"] = self.propellant_capacity * (
            self.oxidizer_fuel_ratio[0]
        )
        propellant_amount["fuel"] = self.propellant_capacity * (
            self.oxidizer_fuel_ratio[1]
        )

        center_cache = []
        left_cache = []
        right_cache = []
        internal_cache = []
        for i in self.structure["center"]:
            center_cache.append(i.name)
        for i in self.structure["left"]:
            left_cache.append(i.name)
        for i in self.structure["right"]:
            right_cache.append(i.name)
        for i in self.structure["internal"]:
            internal_cache.append(i.name)

        return {
            "propellant_amount": propellant_amount,
            "propellant_capacity": self.propellant_capacity,
            "oxidizer_fuel_ratio": self.oxidizer_fuel_ratio,
            "propellants": self.propellants,
            "engine": self.engine.name,
            "structure": {
                "center": center_cache,
                "left": left_cache,
                "right": right_cache,
                "internal": internal_cache,
            },
        }

    def draw_fixed_position_rocket(self, pygame, screen, x, y, scale):
        if self.engine != None:
            rocket_width, rocket_height, rocket_left_shift = (
                self.get_rocket_dimensions()
            )
            body_surface = pygame.Surface(
                (rocket_width, rocket_height), pygame.SRCALPHA
            )
            # body first
            base_x = rocket_left_shift
            base_y = rocket_height - self.engine.height
            current_x = base_x
            current_y = base_y
            asset = self.engine.draw(pygame)
            body_surface.blit(asset, (current_x, current_y))
            for i in self.structure["center"]:
                asset = i.draw(pygame)
                current_x += i.x_offset
                current_y -= i.height - 5
                body_surface.blit(asset, (current_x, current_y))
            current_x = base_x
            current_y = base_y
            current_x += self.engine.side_offset
            for i in self.structure["left"]:
                if isinstance(i, Component):
                    asset = i.draw(pygame)
                    body_surface.blit(asset, ((current_x - i.width), current_y))
                    current_y -= i.height
                if isinstance(i, Spacer):
                    current_y -= Spacer.height
            current_x = base_x
            current_y = base_y
            current_x -= self.engine.side_offset
            for i in self.structure["right"]:
                if isinstance(i, Component):
                    asset = i.draw(pygame)
                    body_surface.blit(
                        asset,
                        (
                            self.structure["center"][0].width + current_x + i.x_offset,
                            current_y,
                        ),
                    )
                    current_y -= i.height
                if isinstance(i, Spacer):
                    current_y -= Spacer.height
            new_width = body_surface.get_width() * scale
            new_height = body_surface.get_height() * scale
            body_surface = pygame.transform.scale(body_surface, (new_width, new_height))
            rect = body_surface.get_rect(midbottom=(x, y))
            screen.blit(body_surface, rect)

    def reset(self):
        self.__init__()
