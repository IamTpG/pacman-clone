if __name__ == '__main__':
    print("This is a module, it should not be run standalone!")
    exit()

import pygame

# local
import tile_map as TMap

# constants
TILE_SIZE = TMap.TILE_SIZE

SCREEN_OFFSET = TMap.SCREEN_OFFSET
SCREEN_WIDTH = TMap.SCREEN_WIDTH
SCREEN_HEIGHT = TMap.SCREEN_HEIGHT

GAME_FONT = TMap.GAME_FONT
FPS = TMap.FPS

clock = pygame.time.Clock()

# test mode
next_direction = {
    "UP": "RIGHT",
    "RIGHT": "DOWN",
    "DOWN": "LEFT",
    "LEFT": "UP"
}

# mapping
input_mapping = {
    pygame.constants.K_UP: "UP",
    pygame.constants.K_DOWN: "DOWN",
    pygame.constants.K_LEFT: "LEFT",
    pygame.constants.K_RIGHT: "RIGHT"
}
input_mapping_wasd = {
    pygame.constants.K_w: (0, -1),
    pygame.constants.K_s: (0, 1),
    pygame.constants.K_a: (-1, 0),
    pygame.constants.K_d: (1, 0)
}
ghosts_mapping = {
    pygame.constants.K_1: 0,
    pygame.constants.K_2: 1,
    pygame.constants.K_3: 2,
    pygame.constants.K_4: 3
}
ghosts_colors_mapping = {
    "blinky": (255, 0, 0), # red
    "inky": (0, 255, 255), # cyan
    "pinky": (255, 105, 180), # pink
    "clyde": (255, 165, 0) # orange
}

# setup variables
setup = True
clear_map = False
update_blinky, update_clyde, update_inky, update_pinky = False, False, False, False
update_ghosts = [update_blinky, update_inky, update_pinky, update_clyde]
dragging_mouse = False

# selection variables
hold_time = 0
hold_max_time = 200
select_ghost = False
selected_ghost = None

# update region
update_region2 = pygame.Rect(SCREEN_OFFSET * 50, SCREEN_OFFSET * 40, SCREEN_WIDTH, SCREEN_HEIGHT)

# test mode loop
def test_mode_loop(screen, tilemap, pacman, blinky, inky, pinky, clyde, ghosts_list, update_region):
    last_sprite_position = (0, 0, 0, 0)

    setup = True
    preset = 1 # default preset 0
    clear_map = False
    update_ghosts = [False, False, False, False]

    select_ghost = False
    selected_ghost = None
    dragging_mouse = False

    preset_positions = {
        #pacman, blinky, inky, pinky, clyde
        # corner 2, 3, 4, 5, 1 is default
        1 : [(15, 28), (2, 34), (10, 34), (20, 34), (28, 34)], # default
        2 : [(28, 34), (2, 6), (2, 6), (2, 6), (2, 6)], # top left to bottom right
        3 : [(28, 6), (2, 34), (2, 34), (2, 34), (2, 34)], # bottom left to top right
        4 : [(24, 19), (5, 19), (5, 19), (5, 19), (5, 19)], # tunnel left to right
        5 : [(15, 34), (15, 19), (15, 19), (15, 19), (15, 19)] # ghost house to bottom middle
    }

    while(True):
        if(setup):
            clear_map, update_ghosts = TMap.setupTestScreen(screen, pacman, ghosts_list, tilemap, clear_map, update_ghosts, update_region, preset, preset_positions)
            for ghost in ghosts_list:
                ghost.direction = "UP"
            setup = False

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                return

            advanced_key_press = pygame.key.get_pressed()
            if(advanced_key_press[pygame.K_LSHIFT] and advanced_key_press[pygame.K_1]):
                setup = True
                preset = 1
            elif(advanced_key_press[pygame.K_LSHIFT] and advanced_key_press[pygame.K_2]):
                setup = True
                preset = 2
            elif(advanced_key_press[pygame.K_LSHIFT] and advanced_key_press[pygame.K_3]):
                setup = True
                preset = 3
            elif(advanced_key_press[pygame.K_LSHIFT] and advanced_key_press[pygame.K_4]):
                setup = True
                preset = 4
            elif(advanced_key_press[pygame.K_LSHIFT] and advanced_key_press[pygame.K_5]):
                setup = True
                preset = 5

            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.constants.K_ESCAPE):
                    return

                if (event.key in input_mapping and pacman.lock_turn_time == 0 and not pacman.dead and not select_ghost):
                    pacman.queue_turn = input_mapping[event.key]
                    pacman.queue_time = pacman.MAX_QUEUE_TIME

                if (event.key in input_mapping and select_ghost):
                    selected_ghost.direction = input_mapping[event.key]
                    SELECTED_GHOST_TEXT = GAME_FONT.render("Selected: " + selected_ghost.name + " | Direction: " + selected_ghost.direction, True, ghosts_colors_mapping[selected_ghost.name])
                    screen.fill((0, 0, 0), update_region2)
                    screen.blit(SELECTED_GHOST_TEXT, (SCREEN_OFFSET * 50, SCREEN_OFFSET * 45))

                if (event.key in input_mapping_wasd and select_ghost):
                    selected_ghost.x += input_mapping_wasd[event.key][0] 
                    selected_ghost.y += input_mapping_wasd[event.key][1] 
                    last_sprite_position = (selected_ghost.x * TILE_SIZE - TILE_SIZE * 2, selected_ghost.y * TILE_SIZE - TILE_SIZE * 2 , TILE_SIZE * 4, TILE_SIZE * 4 + 4)
                    screen.fill((0, 0, 0), last_sprite_position)
                    selected_ghost.snapDisplayToGrid()

                if(event.key == pygame.K_r):
                    setup = True
                    screen.fill((0, 0, 0), update_region2)
                    select_ghost = False
                    selected_ghost = None
                if(event.key == pygame.K_c):
                    screen.fill((0, 0, 0), update_region)

                if(event.key in ghosts_mapping and not advanced_key_press[pygame.K_LSHIFT]):
                    if(selected_ghost == ghosts_list[ghosts_mapping[event.key]]):
                        update_ghosts[ghosts_mapping[event.key]] = True
                        select_ghost = False
                        selected_ghost = None
                    else:
                        selected_ghost = ghosts_list[ghosts_mapping[event.key]]
                        select_ghost = True
                        screen.fill((0, 0, 0), update_region2)
                        SELECTED_GHOST_TEXT = GAME_FONT.render("Selected: " + selected_ghost.name + " | Direction: " + selected_ghost.direction, True, ghosts_colors_mapping[selected_ghost.name])
                        screen.blit(SELECTED_GHOST_TEXT, (SCREEN_OFFSET * 50, SCREEN_OFFSET * 45))

            if (event.type == pygame.MOUSEBUTTONDOWN):
                if(event.button == 1):
                    dragging_mouse = True
                    hold_time = pygame.time.get_ticks()
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
                if(event.button == 1):
                    if(pygame.time.get_ticks() - hold_time < hold_max_time):
                        for i in range(4):
                            if(abs(ghosts_list[i].display_x - event.pos[0]) < TILE_SIZE * 2 and abs(ghosts_list[i].display_y - event.pos[1]) < TILE_SIZE * 2):
                                update_ghosts[i] = True
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
                blinky.update(tilemap.tilemap, pacman, ghosts_list, True)
        if(update_ghosts[1]): #inky
            if(inky.x == pacman.x and inky.y == pacman.y):
                update_ghosts[1] = False
            else:
                inky.update(tilemap.tilemap, pacman, ghosts_list, True)
        if(update_ghosts[2]): #pinky
            if(pinky.x == pacman.x and pinky.y == pacman.y):
                update_ghosts[2] = False
            else:
                pinky.update(tilemap.tilemap, pacman, ghosts_list, True)
        if(update_ghosts[3]): #clyde
            if(clyde.x == pacman.x and clyde.y == pacman.y):
                update_ghosts[3] = False
            else:
                clyde.update(tilemap.tilemap, pacman, ghosts_list, True)
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

        clock.tick(FPS)