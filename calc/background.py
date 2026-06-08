from calc.interpolation import interpolate_color_linear
from settings import SKY_BLUE, SPACE, STAR_START_ALTITUDE, SPACE_ALT
from calc.clouds import draw_clouds
def draw_background(screen, rocket, star_surface, clouds, camera):
    t = min(rocket.y/SPACE_ALT, 1)
    color = interpolate_color_linear(SKY_BLUE, SPACE, t)
    screen.fill(color)

    if rocket.y > STAR_START_ALTITUDE:
        a = min((rocket.y-STAR_START_ALTITUDE)/(SPACE_ALT-STAR_START_ALTITUDE), 1) # how far into space from the position after rocket y and then until the space boundary
        star_surface.set_alpha(a*255)
        screen.blit(star_surface, (0, 0))
    draw_clouds(clouds, screen, camera)

