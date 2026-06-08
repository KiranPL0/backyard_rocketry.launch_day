def calculate_thrust(mass_flow_rate, exhaust_velocity, fuel_purity, oxidizer_purity):
    """
    Calculate the thrust of the rocket, incorporating fuel and oxidizer purity.

    Takes In:
        mass_flow_rate: Base mass flow rate of the propellant (kg/s)
        fuel_purity: Purity of the fuel (0-1)
        oxidizer_purity: Purity of the oxidizer (0-1)
        exhaust_velocity: velocity of exhaust fuels relative to the rocket (m/s)

    Returns:
        Thrust (N)
    """
    # Adjust mass flow rate based on fuel and oxidizer purity
    combustion_efficiency = (fuel_purity + oxidizer_purity)/2
    effective_exhaust_velocity = exhaust_velocity * combustion_efficiency
    thrust = mass_flow_rate * effective_exhaust_velocity
    return thrust