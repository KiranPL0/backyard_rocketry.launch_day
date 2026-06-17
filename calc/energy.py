def calculateKineticEnergy(mass, v_x, v_y):
    return (1/2) * mass * (v_x**2 + v_y**2)**(1/2)

def calculateExplosionEnergy(mass, v_x, v_y):
    return min(calculateKineticEnergy(mass, v_x, v_y), 50)

