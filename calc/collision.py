def pixelPerfectCollision(pygame, playerImg, enemyImg, playerX, playerY, enemyX, enemyY):
    """
    This function will return the collision location of two transparent images
    or None if no collision occurs
    Call only after all assets have been loaded into memory
    """
    
    playerMask = pygame.mask.from_surface(playerImg)
    enemyMask = pygame.mask.from_surface(enemyImg)
    offset = (int(playerX - enemyX), int(playerY - enemyY))
    poi = enemyMask.overlap(playerMask, offset)
    return poi
