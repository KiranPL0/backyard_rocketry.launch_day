import math

def drag_density(altitude):
    return math.exp(-altitude/8500) # density = e^(altitude/8500) -> derived from air density formula

