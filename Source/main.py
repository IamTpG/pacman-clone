# imports
import pygame
import time

# local
import pacman as pacman_m
import ghosts
import tile_map as TMap

# Constants
TILE_RESU = TMap.TILE_RESU
TILE_SIZE = TMap.TILE_SIZE

MAP_WIDTH = TMap.MAP_WIDTH
MAP_HEIGHT = TMap.MAP_HEIGHT

SCREEN_OFFSET = TMap.SCREEN_OFFSET
SCREEN_WIDTH = TMap.SCREEN_WIDTH
SCREEN_HEIGHT = TMap.SCREEN_HEIGHT

# Utils function for reading tilemap

pygame.init()
pygame.mixer.init()

intro_sfx = pygame.mixer.Sound("Resource\\sfx\\intro.wav")

screen = pygame.display.set_mode((SCREEN_WIDTH + SCREEN_OFFSET * 2, SCREEN_HEIGHT + SCREEN_OFFSET * 2))
clock = pygame.time.Clock()
running = True
start = False

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

tilemap = TMap.Tilemap("Resource\\map\\map.png")

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.constants.K_ESCAPE):
                running = False

            if (event.key == pygame.constants.K_UP and pacman.lock_turn_time == 0):
                pacman.queue_turn = "UP"
                pacman.queue_time = pacman.MAX_QUEUE_TIME
            if (event.key == pygame.constants.K_DOWN and pacman.lock_turn_time == 0):
                pacman.queue_turn = "DOWN"
                pacman.queue_time = pacman.MAX_QUEUE_TIME
            if (event.key == pygame.constants.K_LEFT and pacman.lock_turn_time == 0):
                pacman.queue_turn = "LEFT"
                pacman.queue_time = pacman.MAX_QUEUE_TIME
            if (event.key == pygame.constants.K_RIGHT and pacman.lock_turn_time == 0):
                pacman.queue_turn = "RIGHT"
                pacman.queue_time = pacman.MAX_QUEUE_TIME

            #debug, remove this later
            if(event.key == pygame.constants.K_SPACE):
                blinky.feared_state = not blinky.feared_state
                clyde.feared_state = not clyde.feared_state
                inky.feared_state = not inky.feared_state
                pinky.feared_state = not pinky.feared_state

                blinky.feared_time = blinky.MAX_FEARED_TIME
                clyde.feared_time = clyde.MAX_FEARED_TIME
                inky.feared_time = inky.MAX_FEARED_TIME
                pinky.feared_time = pinky.MAX_FEARED_TIME

    # update pacman
    pacman.update(tilemap.tilemap)

    # check collision
    if pacman.checkCollision(ghosts_list):
        for ghost in ghosts_list:
            if not ghost.feared_state:
                if pacman.lives == 0:
                    running = False
                pacman.reset(pacman_starting_position, "NONE")
                blinky.reset(blinky_starting_position, "UP")
                clyde.reset(clyde_starting_position, "UP")
                inky.reset(inky_starting_position, "UP")
                pinky.reset(pinky_starting_position, "UP")
                start = False
                break
    
    for i in range(4):
        for j in range(4):
            if ghosts_list[j] == ghosts_list[i]:
                continue
            else:
                ghosts_list[i].preventCollisionWithOtherGhosts(ghosts_list[j])

    # update ghosts
    blinky.update(tilemap.tilemap)
    clyde.update(tilemap.tilemap)
    inky.update(tilemap.tilemap)
    pinky.update(tilemap.tilemap)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # render objects
    tilemap.render(screen)
    pacman.render(screen, tilemap)
    blinky.render(screen)
    clyde.render(screen)
    inky.render(screen)
    pinky.render(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    FPS = 60
    clock.tick(FPS) 

pygame.quit()