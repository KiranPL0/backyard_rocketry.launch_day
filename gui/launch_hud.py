from settings import WIDTH, HEIGHT


def draw_launch_hud(pygame, screen, rocket):
    from assets.asset_loader import ui_elements, font_15, font_20

    hud = ui_elements["launch_info_hud"]
    hud = pygame.transform.scale(hud, (200, 300))  # width, height
    screen.blit(hud, (WIDTH - hud.get_width() - 10, 10))

    title = font_20.render("Flight Data", False, (2, 189, 52))
    screen.blit(title, (WIDTH - hud.get_width() + 10, 30))
    altitude = font_15.render(f"Altitude: {int(rocket.y)} m", False, (2, 189, 52))
    screen.blit(altitude, (WIDTH - hud.get_width() + 10, 50))
    velocity = font_15.render(
        f"Velocity: {int((rocket.v_x**2 + rocket.v_y**2) ** 0.5)} m/s",
        False,
        (2, 189, 52),
    )
    screen.blit(velocity, (WIDTH - hud.get_width() + 10, 70))
    if rocket.flight_computer is not None:
        apogee = font_15.render(
            f"Apogee: {int(rocket.calculate_apogee())} m", False, (2, 189, 52)
        )
        screen.blit(apogee, (WIDTH - hud.get_width() + 10, 90))
        time_to_apogee = font_15.render(
            f"Time to Apogee: {int(rocket.calculate_time_to_apogee())} s",
            False,
            (2, 189, 52),
        )
        screen.blit(time_to_apogee, (WIDTH - hud.get_width() + 10, 110))
        fuel_remaining = font_15.render(
            f"Fuel: {rocket.propellant_amount['fuel']:.2f} kg",
            False,
            (2, 189, 52),
        )
        screen.blit(fuel_remaining, (WIDTH - hud.get_width() + 10, 130))
        oxidizer_remaining = font_15.render(
            f"Oxidizer: {rocket.propellant_amount['oxidizer']:.2f} kg",
            False,
            (2, 189, 52),
        )
        screen.blit(oxidizer_remaining, (WIDTH - hud.get_width() + 10, 150))
    # else:
    #     no_computer = font_15.render("No flight computer", False, (2, 189, 52))
    #     screen.blit(no_computer, (WIDTH - hud.get_width() + 10, 90))
    #     apogee = font_15.render("Apogee: ERR", False, (2, 189, 52))
    #     screen.blit(apogee, (WIDTH - hud.get_width() + 10, 110))
    #     time_to_apogee = font_15.render(
    #         "Time to Apogee: ERR",
    #         False,
    #         (2, 189, 52),
    #     )
    #     screen.blit(time_to_apogee, (WIDTH - hud.get_width() + 10, 130))
    #     fuel_remaining = font_15.render(
    #         "Fuel: ERR",
    #         False,
    #         (2, 189, 52),
    #     )
    #     screen.blit(fuel_remaining, (WIDTH - hud.get_width() + 10, 150))
    #     oxidizer_remaining = font_15.render(
    #         "Oxidizer: ERR",
    #         False,
    #         (2, 189, 52),
    #     )
    #     screen.blit(oxidizer_remaining, (WIDTH - hud.get_width() + 10, 170))
    if rocket.flight_computer == "advanced_flight_computer":
        throttle = font_15.render(
            f"Throttle: {int(rocket.throttle * 100)}%", False, (2, 189, 52)
        )
        screen.blit(throttle, (WIDTH - hud.get_width() + 10, 190))
        delta_v = font_15.render(
            f"Delta-V: {int(rocket.delta_v)} m/s", False, (2, 189, 52)
        )
        screen.blit(delta_v, (WIDTH - hud.get_width() + 10, 210))
        TWR = font_15.render(
            f"TWR: {round(rocket.calculate_TWR(), 2)}", False, (2, 189, 52)
        )
        screen.blit(TWR, (WIDTH - hud.get_width() + 10, 230))
    # else:
    #     no_advanced = font_15.render("No advanced flight comp.", False, (2, 189, 52))
    #     screen.blit(no_advanced, (WIDTH - hud.get_width() + 10, 190))
    #     throttle = font_15.render("Throttle: ERR", False, (2, 189, 52))
    #     screen.blit(throttle, (WIDTH - hud.get_width() + 10, 210))
    #     delta_v = font_15.render("Delta-V: ERR", False, (2, 189, 52))
    #     screen.blit(delta_v, (WIDTH - hud.get_width() + 10, 230))
    #     TWR = font_15.render("TWR: ERR", False, (2, 189, 52))
    #     screen.blit(TWR, (WIDTH - hud.get_width() + 10, 250))
    if rocket.sas_active and rocket.stability_control_module_present:
        SAS = font_15.render("SAS: ACTIVE", False, (2, 189, 52))
    elif rocket.stability_control_module_present == False:
        SAS = font_15.render("SAS: N/A", False, (2, 189, 52))
    else:
        SAS = font_15.render("SAS: INACTIVE", False, (2, 189, 52))
    screen.blit(SAS, (WIDTH - hud.get_width() + 10, 270))

    # HUD DATA:
    # altitude (w/o flight computer)
    # velocity (magnitude, w/o flight computer)
    # Apogee (basic flight computer)
    # time to Apogee (basic flight computer)
    # fuel remaining (basic flight computer)
    # throttle (advanced flight computer + control surface)
    # delta-v (advanced flight computer)
    # thrust to weight ratio (advnaced flight computer)
    # SAS status (stability control module)
