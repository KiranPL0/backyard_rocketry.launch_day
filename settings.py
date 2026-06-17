WIDTH = 1280
HEIGHT = 720

### PHYSICS ###

GRAVITY_CONSTANT = 9.81
ANGULAR_DAMPING = 0.02

### ALTITUDE ###

## ATMOSPHERIC COLORS ##
# SKY_BLUE = (54, 168, 255)
SKY_BLUE = (85, 144, 246)

SPACE = (0, 0, 0)

## ATMOSPHERIC BOUNDARIES ##
SPACE_ALT = 100000

STAR_START_ALTITUDE = 75000

## SPACE CONSTANTS ##
STAR_NUMBER = 150

## CLOUD BANDS ##

LOW_BAND = [500, 10000]  # [min alt, max alt]
MEDIUM_BAND = [10000, 25000]  # [min alt, max alt]
HIGH_BAND = [25000, 40000]  # [min alt, max alt]

LOW_ALT_CLOUDS = [
    "./assets/clouds/low_alt/1.png",
    "./assets/clouds/low_alt/2.png",
    "./assets/clouds/low_alt/3.png",
    "./assets/clouds/low_alt/4.png",
]

MEDIUM_ALT_CLOUDS = ["./assets/clouds/med_alt/1.png", "./assets/clouds/med_alt/2.png"]

HIGH_ALT_CLOUDS = ["./assets/clouds/high_alt/1.png", "./assets/clouds/high_alt/2.png"]

## GROUND TILES ##

GROUND_TILE_WIDTH = 128

## EXPLOSION DYNAMICS ##
MAX_PARTICLE_COUNT = 100


## VEHICLE ASSEMBLY BUILDINGS ##
VAB_ROCKET_LOCATIONS = {
    0: (WIDTH // 2, HEIGHT - 100, 3),  # X, Y, Scale
    1: (WIDTH // 2, HEIGHT - 100 // 2, 1),
    2: (WIDTH // 2, HEIGHT - 100 // 2, 1),
}

VAB_LEVEL_CONSTRAINTS = {0: {"height": 200}, 1: {"height": 500}, 2: {"height": 750}}

## STAGES:
STAGE_THRESHOLDS = [0, 5, 12]
