import pygame
from settings import WIDTH, HEIGHT
from assets.asset_loader import init_ram, fuels
from classes.rocket import Rocket
from assets.asset_loader import loaded
from classes.camera import Camera
from calc.background import draw_background
from calc.stars import generate_star_surface
from calc.clouds import generate_clouds
from calc.draw_thrust import init_thrust_images
#################################### CLASSES ##################################



#################################### FUNCTIONS ################################
 


#################################### GLOBAL VARIABLES #########################
pygame.init()
init_ram()
#You may change the width and height of your window
icon = pygame.image.load("./assets/images/icon.ico")
icon = pygame.transform.scale(icon, (64, 64))
pygame.display.set_icon(icon)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Backyard Rocketry: Launch Day")

star_surface = generate_star_surface()



clock = pygame.time.Clock()

camera = Camera()

rocket = Rocket()

clouds = generate_clouds(200)

init_thrust_images(pygame)
#################################### GAME LOOP ################################
running = True
full_loaded = False
built = False
while running:
    # ============================== HANDLE EVENTS  ========================= #

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                    print("Max Altitude: " + str(rocket.max_alt) + " m")
                    print("Max Velocity: " + str(rocket.max_v) + " m/s")

    if not running:
        break            
         #INSERT EVENTS HERE

                
    if loaded[0] and loaded[1] and loaded[2]:
        full_loaded = True

    # ============================== CALCULATE TIME ========================= $
    if full_loaded:
        dt = clock.tick(60)/1000 # 60 updates/second

    # ============================== MOVE STUFF ============================= #


    # ============================== COLLISION ============================== #
    if full_loaded == True and built == False:
        rocket.attach_engine('candy-rocket')
        rocket.add_component('cardboard_fuselage', 'center')
        rocket.add_component('cardboard_nose_cone', 'center')
        rocket.add_component('cardboard_fin_left', 'left')
        rocket.add_component('cardboard_fin_right', 'right')
        rocket.fuel('Ammonium Perchlorate', 'Aluminum Powder', [0.5, 0.5])
        rocket.calculate_mass()
        rocket.calculate_drag()
        built = True
  
  
    # ============================== DRAW STUFF ============================= #  
    if full_loaded:                             
        draw_background(screen, rocket, star_surface, clouds, camera)
        camera.follow_object(rocket.x, rocket.y)
        rocket.draw_rocket(camera, dt)
        rocket.throttle = 1
        rocket.update(dt)
        # print("Altitude: " + str(rocket.y) + " m")
        # print("Vertical Velocity: " + str(rocket.v_y) + " m/s")
        # # print(rocket.propellant_amount['oxidizer'])
        # print(rocket.propellant_amount['fuel'])
    # ============================== PYGAME STUFF (DO NOT EDIT) ============= #
    pygame.display.flip()
pygame.quit()