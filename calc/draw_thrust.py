
images = []
burn_out_images = []
thrust_image_number = 0
burn_out_anim = 0
def init_thrust_images(pygame):
    for i in range(8):
        images.append(pygame.image.load('./assets/atmospheric_engine/' + str(i) + '.png').convert_alpha())
    for i in range(5):
        burn_out_images.append(pygame.image.load('./assets/engine_burn_out/' + str(i) + '.png').convert_alpha())


def change_thrust_object():
    global thrust_image_number
    if thrust_image_number == 7:
        thrust_image_number = 0
    else:
        thrust_image_number += 1

def change_burn_out_object():
    global burn_out_anim
    if burn_out_anim == 4:
        burn_out_anim = 0
        return True
    else:
        burn_out_anim += 1
        return False


def get_thrust_object():
    from index import pygame
    global thrust_image_number
    global images
    gen_image = images[thrust_image_number]
    gen_image = pygame.transform.rotate(gen_image, 90)
    return gen_image

def get_burn_out_object():
    from index import pygame
    global burn_out_anim
    global burn_out_images
    gen_image = burn_out_images[burn_out_anim]
    gen_image = pygame.transform.rotate(gen_image, 90)
    return gen_image