# imports
import pygame
import time

# initialize pygame
pygame.init()
pygame.mixer.init()

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

GAME_FONT = TMap.GAME_FONT

# input mapping
input_mapping = {
    pygame.constants.K_UP:      "UP",
    pygame.constants.K_DOWN:    "DOWN",
    pygame.constants.K_LEFT:    "LEFT",
    pygame.constants.K_RIGHT:   "RIGHT"
}

# game loop 
screen = pygame.display.set_mode((SCREEN_WIDTH + SCREEN_OFFSET * 2, SCREEN_HEIGHT + SCREEN_OFFSET * 2))
clock = pygame.time.Clock()
running = True
start = False

# initialize objects
pacman_starting_position = (15, 28)
blinky_starting_position = (15, 16)
clyde_starting_position  = (15, 19)
inky_starting_position   = (13, 19)
pinky_starting_position  = (17, 19)

starting_positions = [pacman_starting_position, blinky_starting_position, clyde_starting_position, inky_starting_position, pinky_starting_position]
starting_state = (50, "SCATTER") # time of scatter mode, scatter mode

pacman  = pacman_m.Pacman(pacman_starting_position, "NONE")
blinky  = ghosts.Blinky(blinky_starting_position, "UP", starting_state)
clyde   = ghosts.Clyde(clyde_starting_position, "UP", starting_state)
inky    = ghosts.Inky(inky_starting_position, "UP", starting_state)
pinky   = ghosts.Pinky(pinky_starting_position, "UP", starting_state)

ghosts_list = [blinky, clyde, inky, pinky]

# load map
tilemap = TMap.Tilemap("Resource\\map\\map.png")

#starting sequence
READY_TEXT = GAME_FONT.render("READY!", True, (255, 255, 0))
BLACK_READY_TEXT = GAME_FONT.render("READY!", True, (0, 0, 0))
intro_sfx = pygame.mixer.Sound("Resource\\sfx\\intro.wav")
intro_sfx.set_volume(0.5)
start = True
enable_intro = True

# pause time
pause_time = 1 #milliseconds #original 4500
pausing = pygame.time.get_ticks() + pause_time

# weird img files bug
print("something something all those pngs file are corrupted or sth idk man i just work here")
print("type \"debugmode\" to enable debug mode")

#debug mode
enable_debug = True
key_order = [pygame.K_d, pygame.K_e, pygame.K_b, pygame.K_u, pygame.K_g, pygame.K_m, pygame.K_o, pygame.K_d, pygame.K_e] #[debugmode]
debug_input_queue = []

while (running):
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.constants.K_ESCAPE):
                running = False

            if (event.key in input_mapping and pacman.lock_turn_time == 0 and not pacman.dead):
                pacman.queue_turn = input_mapping[event.key]
                pacman.queue_time = pacman.MAX_QUEUE_TIME

            #debug, turn ghosts into scared mode
            if (event.key == pygame.constants.K_SPACE):
                for ghost in ghosts_list:
                    ghost.state = "SCARED"
                    ghost.speed = TMap.GHOST_SPEED / 2
                    ghost.snapDisplayToGrid()
                    ghost.scared_time = ghost.MAX_SCARED_TIME

    # update pacman
    pacman.update(tilemap.tilemap)

    # update ghosts
    blinky.update(tilemap.tilemap, pacman, ghosts_list)
    clyde.update(tilemap.tilemap, pacman, ghosts_list)
    inky.update(tilemap.tilemap, pacman, ghosts_list)
    pinky.update(tilemap.tilemap, pacman, ghosts_list)

    # check collision
    if (pacman.checkCollision(ghosts_list, starting_positions)):
        running = False

    # render objects
    tilemap.render(screen)
    blinky.render(screen)
    clyde.render(screen)
    inky.render(screen)
    pinky.render(screen)
    pacman.render(screen, tilemap)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # fill the screen with a color to wipe away anything from last frame
    if (not start or not enable_intro):
        screen.fill("black")

    # display game info
    TMap.displayGameInfo(screen, pacman)
    if (enable_debug):
        TMap.displayDebugInfo(screen, pacman, ghosts_list)

    # starting sequence
    if (start and enable_intro):
        start = False
        #intro_sfx.play()
        last_toggle_time = 0
        show_text = True
        while (pygame.time.get_ticks() < pausing):
            last_toggle_time, show_text = TMap.flashText(screen, last_toggle_time, show_text, READY_TEXT, BLACK_READY_TEXT)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    running = False
                    break

                if (event.type == pygame.KEYDOWN and not enable_debug):
                    debug_input_queue.append(event.key)

                if (len(debug_input_queue) > len(key_order)):
                    debug_input_queue.pop(0)        

                if (debug_input_queue == key_order and not enable_debug):
                    print("DEBUG MODE ENABLED")
                    enable_debug = True    
            if (not running):
                break

        if (enable_debug):
            TMap.enableDebugMode(SCREEN_WIDTH)

    FPS = 60
    clock.tick(FPS) 

pygame.quit()