import math
from settings import GRAVITY_CONSTANT

def acceleration(thrust, mass):
    f_net = thrust - (mass*GRAVITY_CONSTANT)
    a = f_net/mass
    return a

def acceleration_components(thrust, mass, angle):
    a_total = acceleration(thrust, mass)
    
    a_x = math.sin(angle)*a_total
    a_y = math.cos(angle)*a_total
    
    return a_x, a_y

