# imports
import pygame

# initialize pygame
pygame.init()
pygame.mixer.init()

# local imports
import pacman as pacman_m
import ghosts
import tile_map as TMap
import test_mode as test_md

# constants
TILE_RESU = TMap.TILE_RESU
TILE_SIZE = TMap.TILE_SIZE

MAP_WIDTH = TMap.MAP_WIDTH
MAP_HEIGHT = TMap.MAP_HEIGHT

SCREEN_OFFSET = TMap.SCREEN_OFFSET
SCREEN_WIDTH = TMap.SCREEN_WIDTH
SCREEN_HEIGHT = TMap.SCREEN_HEIGHT

GAME_FONT = TMap.GAME_FONT
FPS = TMap.FPS

# input mapping
input_mapping = {
    pygame.constants.K_UP:      "UP",
    pygame.constants.K_DOWN:    "DOWN",
    pygame.constants.K_LEFT:    "LEFT",
    pygame.constants.K_RIGHT:   "RIGHT"
}

# game loop 
update_region = pygame.Rect(0, SCREEN_OFFSET * 7, SCREEN_WIDTH + SCREEN_OFFSET * 2, SCREEN_HEIGHT + SCREEN_OFFSET * 2)
screen = pygame.display.set_mode((SCREEN_WIDTH + SCREEN_OFFSET * 2, SCREEN_HEIGHT + SCREEN_OFFSET * 2))
clock = pygame.time.Clock()
running = True
start = False
win = False
quiting = False

# initialize objects
pacman_starting_position = (15, 28)
blinky_starting_position = (17, 19)
clyde_starting_position  = (15, 19)
inky_starting_position   = (13, 19)
pinky_starting_position  = (15, 16)

starting_positions = [pacman_starting_position, blinky_starting_position, clyde_starting_position, inky_starting_position, pinky_starting_position]

pacman  = pacman_m.Pacman(pacman_starting_position, "NONE")
inky    = ghosts.BFSGhost(inky_starting_position, "UP", "inky")
pinky   = ghosts.IDSGhost(pinky_starting_position, "UP", "pinky")
clyde   = ghosts.UCSGhost(clyde_starting_position, "UP", "clyde")
blinky  = ghosts.AStarGhost(blinky_starting_position, "UP", "blinky")

ghosts_list = [blinky, inky, pinky, clyde]

# load map
tilemap = TMap.Tilemap("Resource\\map\\map.png")

#starting sequence
READY_TEXT = GAME_FONT.render("READY!", True, (255, 255, 0))
BLACK_READY_TEXT = GAME_FONT.render("READY!", True, (0, 0, 0))
intro_sfx = pygame.mixer.Sound("Resource\\sfx\\intro.wav")
intro_sfx.set_volume(0.3)
start = True
enable_intro = True

# pause time
pause_time = 4500 #milliseconds #original 4500
pausing = pygame.time.get_ticks() + pause_time

#debug mode
enable_debug = False #default False
key_order_dm = [pygame.K_d, pygame.K_e, pygame.K_b, pygame.K_u, pygame.K_g, pygame.K_m, pygame.K_o, pygame.K_d, pygame.K_e] #[debugmode]
debug_input_queue = []

#test mode
enable_test = False #default False
key_order_tm = [pygame.K_t, pygame.K_e, pygame.K_s, pygame.K_t, pygame.K_m, pygame.K_o, pygame.K_d, pygame.K_e] #[testmode] 
test_input_queue = []

#extra codes
enable_invincibility = False #default False
key_order_invc = [pygame.K_u, pygame.K_n, pygame.K_d, pygame.K_i, pygame.K_e] #[undie]
invincibility_input_queue = []

#debug
print("Fix these pngs files bruh")

while (running): 
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
            quiting = True

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.constants.K_ESCAPE):
                running = False
                quiting = True

            if (event.key in input_mapping and pacman.lock_turn_time == 0 and not pacman.dead):
                pacman.queue_turn = input_mapping[event.key]
                pacman.queue_time = pacman.MAX_QUEUE_TIME

    # update pacman
    pacman.update(tilemap.tilemap) 
    pacman.eatFood(tilemap, ghosts_list)

    # update ghosts
    blinky.update(tilemap.tilemap, pacman, ghosts_list, enable_test)
    clyde.update(tilemap.tilemap, pacman, ghosts_list, enable_test)
    inky.update(tilemap.tilemap, pacman, ghosts_list, enable_test)
    pinky.update(tilemap.tilemap, pacman, ghosts_list, enable_test)

    # check collision
    if (enable_invincibility):
        pass
    elif (pacman.checkCollision(tilemap, ghosts_list, starting_positions)):
        win = False
        running = False

    if (tilemap.pellet_count == 0):
        win = True
        running = False

    # render objects
    tilemap.render(screen)
    blinky.render(screen)
    clyde.render(screen)
    inky.render(screen)
    pinky.render(screen)
    pacman.render(screen, tilemap)

    # flip() the display to put your work on screen
    pygame.display.update()

    # fill the screen with a color to wipe away anything from last frame
    if (not start or not enable_intro):
        screen.fill((0, 0, 0), update_region)

    # display game info
    TMap.displayGameInfo(screen, pacman, tilemap)
    if (enable_debug):
        TMap.displayDebugInfo(screen, pacman, ghosts_list)

    # starting sequence
    if (start and enable_intro):
        TMap.displayTitleCard(screen, enable_debug)
        start = False
        intro_sfx.play()
        last_toggle_time = 0
        show_text = True
        while (pygame.time.get_ticks() < pausing):
            last_toggle_time, show_text = TMap.flashText(screen, last_toggle_time, show_text, READY_TEXT, BLACK_READY_TEXT)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    running = False
                    quiting = True
                    break

                #check for debug mode entry
                if (event.type == pygame.KEYDOWN and not enable_debug):
                    debug_input_queue.append(event.key)
                if (len(debug_input_queue) > len(key_order_dm)):
                    debug_input_queue.pop(0)       
                if (debug_input_queue == key_order_dm and not enable_debug):
                    print("DEBUG MODE ENABLED")
                    enable_debug = True    
                    standard_mode = False

                #check for test mode entry
                if (event.type == pygame.KEYDOWN and not enable_test):
                    test_input_queue.append(event.key)
                if (len(test_input_queue) > len(key_order_tm)):
                    test_input_queue.pop(0)
                if (test_input_queue == key_order_tm and not enable_test):
                    print("TEST MODE ENABLED")
                    enable_test = True
                    standard_mode = False

                #check for invincibility mode entry
                if (event.type == pygame.KEYDOWN and not enable_invincibility):
                    invincibility_input_queue.append(event.key)
                if (len(invincibility_input_queue) > len(key_order_invc)):
                    invincibility_input_queue.pop(0)
                if (invincibility_input_queue == key_order_invc and not enable_invincibility):
                    print("INVINCIBILITY ENABLED")
                    enable_invincibility = True

            if (not running):
                break

        if (enable_debug):
            screen, new_screen_width = TMap.enableDebugMode(SCREEN_WIDTH)
            update_region = pygame.Rect(0, SCREEN_OFFSET * 7, new_screen_width + SCREEN_OFFSET * 2, SCREEN_HEIGHT + SCREEN_OFFSET)

        if (enable_test):
            screen, new_screen_width = TMap.enableTestMode(SCREEN_WIDTH)
            TMap.displayTestScreen(screen)
            running = False

        TMap.displayTitleCard(screen, enable_debug)
        tilemap.start_time = pygame.time.get_ticks()

    clock.tick(FPS) 

if (enable_test):
    test_md.test_mode_loop(screen, tilemap, pacman, blinky, inky, pinky, clyde, ghosts_list, update_region)
    quiting = True

# display endcard
if(not quiting):
    update_region = TMap.displayEndCard(screen, win, tilemap)
    pygame.display.update(update_region)
    ending = True
    while (ending):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                ending = False
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.constants.K_ESCAPE):
                    ending = False

pygame.quit()