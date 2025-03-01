# imports
import pygame
import time

# local imports
import pacman as pacman_m
import ghosts
import tile_map as TMap

# constants
TILE_RESU = TMap.TILE_RESU
TILE_SIZE = TMap.TILE_SIZE

MAP_WIDTH = TMap.MAP_WIDTH
MAP_HEIGHT = TMap.MAP_HEIGHT

SCREEN_OFFSET = TMap.SCREEN_OFFSET
SCREEN_WIDTH = TMap.SCREEN_WIDTH
SCREEN_HEIGHT = TMap.SCREEN_HEIGHT

# input mapping
input_mapping = {
    pygame.constants.K_UP: "UP",
    pygame.constants.K_DOWN: "DOWN",
    pygame.constants.K_LEFT: "LEFT",
    pygame.constants.K_RIGHT: "RIGHT"
}

# initialize pygame
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH + SCREEN_OFFSET * 2, SCREEN_HEIGHT + SCREEN_OFFSET * 2))
clock = pygame.time.Clock()
running = True
start = False

# initialize objects
pacman_starting_position = (15, 28)
blinky_starting_position = (15, 16)
clyde_starting_position = (15, 19)
inky_starting_position = (13, 19)
pinky_starting_position = (17, 19)

pacman = pacman_m.Pacman(pacman_starting_position, "NONE")
blinky = ghosts.Ghost(blinky_starting_position, "UP", "blinky")
clyde = ghosts.Ghost(clyde_starting_position, "UP", "clyde")
inky = ghosts.Ghost(inky_starting_position, "UP", "inky")
pinky = ghosts.Ghost(pinky_starting_position, "UP", "pinky")

ghosts_list = [blinky, clyde, inky, pinky]

# load map
tilemap = TMap.Tilemap("Resource\\map\\map.png")

while running:
    # check input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.constants.K_ESCAPE):
                running = False

            if (event.key in input_mapping and pacman.lock_turn_time == 0):
                pacman.queue_turn = input_mapping[event.key]
                pacman.queue_time = pacman.MAX_QUEUE_TIME

    # update pacman
    pacman.update(tilemap.tilemap)

    # update ghosts
    blinky.update(tilemap.tilemap, pacman)
    clyde.update(tilemap.tilemap, pacman)
    inky.update(tilemap.tilemap, pacman)
    pinky.update(tilemap.tilemap, pacman)

    # check collision
    if pacman.checkCollision(ghosts_list):
        for ghost in ghosts_list:
            if not ghost.feared_state:
                if pacman.lives == 0:
                    running = False
                pacman.resetPosition(pacman_starting_position, "DOWN")
                blinky.resetPosition(blinky_starting_position, "UP")
                clyde.resetPosition(clyde_starting_position, "UP")
                inky.resetPosition(inky_starting_position, "UP")
                pinky.resetPosition(pinky_starting_position, "UP")
                start = False
                break

    # render objects
    tilemap.render(screen)
    pacman.render(screen, tilemap)
    blinky.render(screen)
    clyde.render(screen)
    inky.render(screen)
    pinky.render(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

     # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    FPS = 60
    clock.tick(FPS) 

pygame.quit()