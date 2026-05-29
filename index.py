import pygame
from calc.thrust import calculate_thrust
from settings import WIDTH, HEIGHT
from assets.asset_loader import load_fuels
#################################### CLASSES ##################################



#################################### FUNCTIONS ################################
 


#################################### GLOBAL VARIABLES #########################
pygame.init()
load_fuels()
#You may change the width and height of your window
icon = pygame.image.load("./assets/images/icon.ico")
icon = pygame.transform.scale(icon, (64, 64))
pygame.display.set_icon(icon)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Backyard Rocketry: Launch Day")



#################################### GAME LOOP ################################
done = False
while True:
    # ============================== HANDLE EVENTS  ========================= #

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            done = True
            break
        
         #INSERT EVENTS HERE

                
    if done == True:
        break


    # ============================== MOVE STUFF ============================= #



    # ============================== COLLISION ============================== #
  
  
  
    # ============================== DRAW STUFF ============================= #                               
    screen.fill((0, 0, 0))


    
    
    # ============================== PYGAME STUFF (DO NOT EDIT) ============= #
    pygame.display.flip()
    pygame.time.delay(20)
pygame.quit()