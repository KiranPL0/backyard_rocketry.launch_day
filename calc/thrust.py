import math

def characteristic_velocity(ideal, oxidizer_purity, fuel_purity, combustion_efficiency):
    """
    ideal = m/s  (ideal characteristic velocity at given ratio)
    oxidizer_purity = % (purity of the oxidizer)
    fuel_purity = % (purity of the fuel)
    combustion_efficiency = % (efficiency of the combustion process)
    """

    purity_factor = oxidizer_purity*fuel_purity
    return ideal*purity_factor*combustion_efficiency






def calculate_thrust(mass_flow_rate, exhaust_v, nozzle_size, exhaust_p, ambient_pressure,):
    """
    Calculates thrust based off atmospheric conditions
    mass_flow_rate: mass flow rate of the propellant (kg/s)
    exhaust_v: velocity of the exhaust gases (m/s)
    nozzle_size: area of the nozzle exit (m^2)
    exhaust_p: pressure of the exhaust gases at the nozzle exit (Pa)
    ambient_pressure: pressure of the atmosphere (Pa)
    """

    momentum_thrust = 
