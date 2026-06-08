import math
import random
from assets.asset_loader import fuels
from assets.asset_loader import engines
from assets.asset_loader import components
from calc.thrust import calculate_thrust
from calc.kinematics import acceleration_components
from classes.spacer import Spacer
from classes.component import Component
from calc.atmosphere import drag_density
from settings import ANGULAR_DAMPING
from calc.draw_thrust import get_thrust_object, change_thrust_object, change_burn_out_object, get_burn_out_object 

class Rocket:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.v_x = 0
        self.v_y = 0
        self.angle = 0 #angle from 90* to horizontal
        self.structure = {
            "left": [],
            "center": [], # index 0 represents bottom of rocket, attatched to engine
            "right": [],
            "internal": []
        }
        self.component_space = 0
        self.air_resistance = 0 #drag coefficient
        self.crew = []
        self.stability = {
            "left": 0,
            "right": 0
        }
        self.propellants = {
            "oxidizer": None,
            "fuel": None
        }
        self.propellant_amount = { #in kgs
            "oxidizer": 0,
            "fuel": 0
        }
        self.oxidizer_fuel_ratio = [] # oxidizer %, fuel %
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
        self.thrust_frame_duration = 0.12 # seconds
        self.burning_out = False
        self.burn_complete = False
        self.burn_out_frame_duration = 0.12 # seconds
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
    def attach_engine(self, name):
        for i in engines:
            if i.name == name:
                self.engine = i
    
    def calculate_drag(self):
        self.air_resistance = 0
        self.air_resistance += self.engine.drag_factor
        for i in self.structure['center']:
            if isinstance(i, Component):
                self.air_resistance += i.drag_factor
        for i in self.structure['left']:
            if isinstance(i, Component):
                self.air_resistance += i.drag_factor
        for i in self.structure['right']:
            if isinstance(i, Component):
                self.air_resistance += i.drag_factor
    def update(self, dt):
        if self.stability['left'] > 0 and self.stability['right'] > 0:
            torque = (self.stability['left'] - self.stability['right'])*ANGULAR_DAMPING
        else:
            torque = random.random()*0.2-0.1*ANGULAR_DAMPING
        self.angular_velocity += torque*dt
        self.angle += self.angular_velocity*dt
        if self.throttle > 0 and self.propellant_amount['fuel'] > 0 and self.propellant_amount['oxidizer'] > 0:
            flow_rate = self.engine.max_flow_rate*self.throttle
            self.propellant_amount['fuel'] -= flow_rate*dt
            self.propellant_amount['oxidizer'] -= flow_rate*dt
            if self.propellant_amount['fuel'] < 0:
                self.propellant_amount['fuel'] = 0
            if self.propellant_amount['oxidizer'] < 0:
                self.propellant_amount['oxidizer'] = 0
            # print(self.propellants['fuel'])
            thrust = calculate_thrust(flow_rate, self.engine.exhaust_velocity, self.propellants['fuel']['purity'], self.propellants['oxidizer']['purity'])
            # print(self.propellant_amount['fuel'], self.propellant_amount['oxidizer'])
            a_x, a_y = acceleration_components(thrust, self.total_mass, self.angle)
            a_x *= (1+(self.stability['left']-self.stability['right']))
        else:
            if self.burn_complete == False and self.burning_out == False:
                self.thrust_timer = 0
                self.burning_out = True
            a_x, a_y = acceleration_components(0, self.total_mass, self.angle)
            self.angular_velocity += random.randint(-50, 50)*ANGULAR_DAMPING*dt

        scalar_velocity = math.sqrt(self.v_x**2 + self.v_y**2) # v = (vx^2 + vy^2)^1/2

        a_drag_x = 0
        a_drag_y = 0
        if scalar_velocity != 0:
            f_drag = 0.5 * self.air_resistance * (scalar_velocity**2) * drag_density(self.y)

            f_drag_x = -f_drag * (self.v_x/scalar_velocity) # trig ratio
            f_drag_y = -f_drag * (self.v_y/scalar_velocity)

            a_drag_x = f_drag_x / self.total_mass
            a_drag_y = f_drag_y / self.total_mass

        a_x += a_drag_x
        a_y += a_drag_y
        self.v_x += a_x*dt
        self.v_y += a_y*dt
        self.x += self.v_x*dt
        self.y += self.v_y*dt
        self.max_alt = max(self.max_alt, self.y)
        if self.y > 0:
            self.max_v = max(self.max_v, scalar_velocity)

    def get_rocket_dimensions(self):
        width = self.engine.width
        left_shift = 0
        for i in self.structure['left']:
            if isinstance(i, Component):
                width += i.width
                left_shift += i.width
        for i in self.structure['right']:
            if isinstance(i, Component):
                width += i.width
        height = self.engine.height
        for i in self.structure['center']:
            if isinstance(i, Component):
                height += i.height
        return width, height, left_shift #height is buffered

    def add_component(self, name, location): # bottom up
        for i in components:
            if i.name == name:
                self.structure[location].append(i)
                if i.stability_offset != None:
                    self.stability[location] += i.stability_offset
                break

    def add_spacer(self, height, location, width=1):
        self.structure[location].append(Spacer(height, width))

    def calculate_propellant_capacity(self):
        capacity = self.engine.fuel_capacity
        for i in self.structure['center']:
            if isinstance(i, Component):
                capacity += i.fuel_capacity
        for i in self.structure['left']:
            if isinstance(i, Component):
                capacity += i.fuel_capacity
        for i in self.structure['right']:
            if isinstance(i, Component):
                capacity += i.fuel_capacity
        self.propellant_capacity = capacity

    def calculate_mass(self):
        mass = self.engine.mass
        for i in self.structure['center']:
            if isinstance(i, Component):
                mass += i.mass
        for i in self.structure['left']:
            if isinstance(i, Component):
                mass += i.mass
        for i in self.structure['right']:
            if isinstance(i, Component):
                mass += i.mass
        for i in self.structure['internal']:
            if isinstance(i, Component):
                mass += i.mass
        self.total_mass = mass

    def draw_rocket(self, camera, dt):
        from index import pygame, screen
        rocket_width, rocket_height, rocket_left_shift = self.get_rocket_dimensions()
        rocket_surface = pygame.Surface((rocket_width, rocket_height+180), pygame.SRCALPHA) # +180 = +160 for engine flame + 20 for buffer
        # body first
        base_x = rocket_left_shift
        base_y = rocket_height - self.engine.height
        current_x = base_x
        current_y = base_y

        asset = self.engine.draw()
        rocket_surface.blit(asset, (current_x, current_y))
        for i in self.structure['center']:
            asset = i.draw()
            current_x += i.x_offset
            current_y -= (i.height-5)
            if current_y < 0:
                return "OOR"
            rocket_surface.blit(asset, (current_x, current_y))
        current_x = base_x
        current_y = base_y
        current_x += self.engine.side_offset
        for i in self.structure['left']:
            if isinstance(i, Component):
                asset = i.draw()
                if current_y < 0:
                    return "OOR"
                rocket_surface.blit(asset, ((current_x - i.width), current_y))
                current_y -= i.height
            if isinstance(i, Spacer):
                current_y -= Spacer.height
                if current_y < 0:
                    return "OOR"
        current_x = base_x
        current_y = base_y
        current_x -= self.engine.side_offset
        for i in self.structure['right']:
            if isinstance(i, Component):
                asset = i.draw()
                rocket_surface.blit(asset, (self.structure['center'][0].width + current_x, current_y))
                current_y -= i.height
                if current_y < 0:
                    return "OOR"
            if isinstance(i, Spacer):
                current_y -= Spacer.height
                if current_y < 0:
                    return "OOR"
        
        if self.throttle > 0 and self.propellant_amount['fuel'] > 0 and self.propellant_amount['oxidizer'] > 0:
            self.thrust_timer += dt
            if self.thrust_timer > self.thrust_frame_duration:
                self.thrust_timer = 0
                change_thrust_object()
            thrust_object = get_thrust_object()
            rocket_surface.blit(thrust_object, (base_x, base_y+self.engine.height))
        else:
            if self.burn_complete == False and self.burning_out == True:
                self.thrust_timer += dt
                if self.thrust_timer > self.burn_out_frame_duration:
                    self.thrust_timer = 0
                    self.burn_complete = change_burn_out_object()
                if self.burn_complete == False:
                    thrust_object = get_burn_out_object()
                    rocket_surface.blit(thrust_object, (base_x, base_y+self.engine.height))


        rotated = pygame.transform.rotate(rocket_surface, -math.degrees(self.angle))
        real_x, real_y = camera.world_to_screen(self.x, self.y)
        rocket_rect = rotated.get_rect(center=(real_x, real_y))
        screen.blit(rotated, rocket_rect)
        return "OK"
    
    


        
        


