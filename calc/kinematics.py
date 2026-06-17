import math
from settings import GRAVITY_CONSTANT


def acceleration_components(thrust, angle):    
    a_x = math.sin(angle)*thrust
    a_y = (math.cos(angle)*thrust) - GRAVITY_CONSTANT 
    return a_x, a_y

