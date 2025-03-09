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
pinky_starting_position  = (17, 16)

starting_positions = [pacman_starting_position, blinky_starting_position, clyde_starting_position, inky_starting_position, pinky_starting_position]

pacman  = pacman_m.Pacman(pacman_starting_position, "NONE")
blinky  = ghosts.Blinky(blinky_starting_position, "UP")
clyde   = ghosts.Clyde(clyde_starting_position, "UP")
inky    = ghosts.Inky(inky_starting_position, "UP")
pinky   = ghosts.Pinky(pinky_starting_position, "UP")

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
    blinky.update(tilemap.tilemap, pacman, ghosts_list)
    clyde.update(tilemap.tilemap, pacman, ghosts_list)
    inky.update(tilemap.tilemap, pacman, ghosts_list)
    pinky.update(tilemap.tilemap, pacman, ghosts_list)

    # check collision
    if (pacman.checkCollision(tilemap, ghosts_list, starting_positions)):
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

                #check for test mode entry
                if (event.type == pygame.KEYDOWN and not enable_test):
                    test_input_queue.append(event.key)
                if (len(test_input_queue) > len(key_order_tm)):
                    test_input_queue.pop(0)
                if (test_input_queue == key_order_tm and not enable_test):
                    print("TEST MODE ENABLED")
                    enable_test = True

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

    FPS = 60
    clock.tick(FPS) 

# test mode
next_direction = {
    "UP": "RIGHT",
    "RIGHT": "DOWN",
    "DOWN": "LEFT",
    "LEFT": "UP"
}

# setup variables
setup = True
clear_map = False
update_blinky, update_clyde, update_inky, update_pinky = False, False, False, False
update_ghosts = [update_blinky, update_inky, update_pinky, update_clyde]
dragging_mouse = False

# selection variables
select_ghost = False
selected_ghost = None

# update region
update_region2 = pygame.Rect(SCREEN_OFFSET * 50, SCREEN_OFFSET * 40, SCREEN_WIDTH, SCREEN_HEIGHT)
last_sprite_position = (0, 0, 0, 0)

# test mode loop
while(enable_test):
    if(setup):
        clear_map, update_ghosts = TMap.setupTestScreen(screen, pacman, ghosts_list, tilemap, clear_map, update_ghosts, update_region)
        setup = False

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            enable_test = False
            quiting = True

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.constants.K_ESCAPE):
                enable_test = False
                quiting = True

            if (event.key in input_mapping and pacman.lock_turn_time == 0 and not pacman.dead and not select_ghost):
                pacman.queue_turn = input_mapping[event.key]
                pacman.queue_time = pacman.MAX_QUEUE_TIME
           
            if (event.key == pygame.K_1):
                update_ghosts[0] = True #blinky
                blinky.snapDisplayToGrid()
            if (event.key == pygame.K_2):
                update_ghosts[1] = True #inky
                clyde.snapDisplayToGrid()
            if (event.key == pygame.K_3):
                update_ghosts[2] = True #pinky
                inky.snapDisplayToGrid()
            if (event.key == pygame.K_4):
                update_ghosts[3] = True #clyde
                pinky.snapDisplayToGrid()

            if(event.key == pygame.K_r):
                setup = True
            if(event.key == pygame.K_c):
                screen.fill((0, 0, 0), update_region)

        if (event.type == pygame.MOUSEBUTTONDOWN):
            if(event.button == 1):
                dragging_mouse = True
                for ghost in ghosts_list:
                    if(abs(ghost.display_x - event.pos[0]) < TILE_SIZE * 2 and abs(ghost.display_y - event.pos[1]) < TILE_SIZE * 2):
                        selected_ghost = ghost
                        select_ghost = True
            if(event.button == 3):
                if(select_ghost):
                    select_ghost = False
                    screen.fill((0, 0, 0), update_region2)
                else:
                    if(selected_ghost == None):
                        for ghost in ghosts_list:
                            if(abs(ghost.display_x - event.pos[0]) < TILE_SIZE * 2 and abs(ghost.display_y - event.pos[1]) < TILE_SIZE * 2):
                                selected_ghost = ghost
                                select_ghost = True
                    
        if (event.type == pygame.MOUSEBUTTONUP):
            if(select_ghost or abs(pacman.display_x - event.pos[0]) < TILE_SIZE * 2 and abs(pacman.display_y - event.pos[1]) < TILE_SIZE * 2):
                screen.fill((0, 0, 0), update_region)
            if(event.button == 3 and selected_ghost != None):
                selected_ghost.direction = next_direction[selected_ghost.direction]
                screen.fill((0, 0, 0), update_region2)
                SELECTED_GHOST_TEXT = GAME_FONT.render("Selected: " + selected_ghost.name + " | Direction: " + selected_ghost.direction, True, (255, 255, 0))
                screen.blit(SELECTED_GHOST_TEXT, (SCREEN_OFFSET * 50, SCREEN_OFFSET * 40))
            selected_ghost = None
            dragging_mouse = False
            select_ghost = False

        if(event.type == pygame.MOUSEMOTION and dragging_mouse):
            if(select_ghost):
                last_sprite_position = (selected_ghost.x * TILE_SIZE - selected_ghost.radius, selected_ghost.y * TILE_SIZE - selected_ghost.radius, TILE_SIZE * 2, TILE_SIZE * 2)
                selected_ghost.x, selected_ghost.y = event.pos[0] // TILE_SIZE, event.pos[1] // TILE_SIZE
                selected_ghost.snapDisplayToGrid()
                pygame.display.update(update_region)
            elif (abs(pacman.display_x - event.pos[0]) < TILE_SIZE * 2 and abs(pacman.display_y - event.pos[1]) < TILE_SIZE * 2):
                last_sprite_position = (pacman.x * TILE_SIZE - pacman.radius, pacman.y * TILE_SIZE - pacman.radius, TILE_SIZE * 2, TILE_SIZE * 2)
                pacman.x, pacman.y = event.pos[0] // TILE_SIZE, event.pos[1] // TILE_SIZE
                pacman.snapDisplayToGrid()
                pygame.display.update(update_region)
            screen.fill((0, 0, 0), last_sprite_position)

    # update pacman
    pacman.update(tilemap.tilemap)
    if(pacman.checkObstructionDirection(tilemap.tilemap, pacman.direction)):
        pacman.direction = "NONE"
        screen.fill((0, 0, 0), update_region)
    if(pacman.direction != "NONE"):
        screen.fill((0, 0, 0), update_region)

    # update ghosts
    if(update_ghosts[0]): #blinky
        if(blinky.x == pacman.x and blinky.y == pacman.y):
            update_ghosts[0] = False
        else:
            blinky.update(tilemap.tilemap, pacman, ghosts_list)
    if(update_ghosts[1]): #inky
        if(inky.x == pacman.x and inky.y == pacman.y):
            update_ghosts[1] = False
        else:
            inky.update(tilemap.tilemap, pacman, ghosts_list)
    if(update_ghosts[2]): #pinky
        if(pinky.x == pacman.x and pinky.y == pacman.y):
            update_ghosts[2] = False
        else:
            pinky.update(tilemap.tilemap, pacman, ghosts_list)
    if(update_ghosts[3]): #clyde
        if(clyde.x == pacman.x and clyde.y == pacman.y):
            update_ghosts[3] = False
        else:
            clyde.update(tilemap.tilemap, pacman, ghosts_list)
    if(any(update_ghosts)):
        screen.fill((0, 0, 0), update_region2)

    # render objects
    tilemap.render(screen)
    pacman.render(screen, tilemap)
    blinky.render(screen)
    clyde.render(screen)
    inky.render(screen)
    pinky.render(screen)

    pygame.display.update()

    FPS = 60
    clock.tick(FPS)

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