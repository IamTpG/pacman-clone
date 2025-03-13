if __name__ == '__main__':
    print("This is a module, it should not be run standalone!")
    exit()

import pygame

pygame.display.set_caption("Pacman")
pygame.display.set_icon(pygame.image.load("Resource\\ghosts\\blinky\\right.png"))

TILE_RESU = 8   # Tile size in .png
TILE_SIZE = 16  # Tile size to render

# original size 29, 37
MAP_WIDTH  = 29
MAP_HEIGHT = 37

SCREEN_OFFSET = 10
SCREEN_WIDTH  = MAP_WIDTH  * TILE_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE

PACMAN_RADIUS = TILE_SIZE - 5
PACMAN_SPEED = 2

GHOST_RADIUS = TILE_SIZE - 5
GHOST_SPEED = 2

FPS = 60

# ghost colors 
ghost_colors = {
    "blinky": (255, 0, 0),
    "clyde":  (255, 165, 0),
    "inky":   (0, 255, 255),
    "pinky":  (255, 105, 180)
}

# display game info
GAME_FONT_SMALL = pygame.font.Font("Resource\\text_font\\Emulogic-zrEw.ttf", 8)
GAME_FONT = pygame.font.Font("Resource\\text_font\\Emulogic-zrEw.ttf", 10)
GAME_FONT_LARGE = pygame.font.Font("Resource\\text_font\\Emulogic-zrEw.ttf", 21)

#load pngs
lives_image = pygame.image.load("Resource\\pacman\\movement_animation\\right\\2.png")
PROP_BLINKY = pygame.image.load("Resource\\ghosts\\blinky\\right.png")
PROP_INKY = pygame.image.load("Resource\\ghosts\\inky\\right.png")
PROP_PINKY = pygame.image.load("Resource\\ghosts\\pinky\\left.png")
PROP_CLYDE = pygame.image.load("Resource\\ghosts\\clyde\\left.png")
PROP_SCARED_GHOST = pygame.image.load("Resource\\ghosts\\scared.png")
LETTER_C = pygame.image.load("Resource\\pacman\\movement_animation\\right\\1.png")
PACMAN_UP = pygame.image.load("Resource\\pacman\\movement_animation\\up\\1.png")

def pauseScreen(time):
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

# debug mode
def enableDebugMode(screen_width):
    screen_width += 300
    #new screen size
    new_screen = pygame.display.set_mode((screen_width + SCREEN_OFFSET * 2, SCREEN_HEIGHT + SCREEN_OFFSET * 2))
    return new_screen, screen_width

def enableTestMode(screen_width):
    screen_width += 500
    #new screen size
    new_screen = pygame.display.set_mode((screen_width + SCREEN_OFFSET * 2, SCREEN_HEIGHT + SCREEN_OFFSET * 2))
    return new_screen, screen_width

def displayTitleCard(screen, enable_debug):
    TITLE_TEXT = GAME_FONT_LARGE.render("PA MAN", True, (255, 255, 0))
    screen.blit(TITLE_TEXT, (SCREEN_OFFSET * 18, 10))

    screen.blit(pygame.transform.scale(LETTER_C, (23, 23)), (SCREEN_OFFSET * 18 + 41, 14))

    FUNNI_TEXT = GAME_FONT.render("The I stayed up 'til 3AM for this Edition", True, (255, 255, 0))
    screen.blit(FUNNI_TEXT, (SCREEN_OFFSET * 3, SCREEN_OFFSET * 4))
    TM = GAME_FONT_SMALL.render("TM", True, (255, 255, 0))
    screen.blit(TM, (SCREEN_OFFSET * 44, SCREEN_OFFSET * 3.5))

    screen.blit(pygame.transform.scale(PROP_BLINKY, (23, 23)), (SCREEN_OFFSET * 4, SCREEN_OFFSET))
    screen.blit(pygame.transform.scale(PROP_INKY, (23, 23)), (SCREEN_OFFSET * 12, SCREEN_OFFSET))
    screen.blit(pygame.transform.scale(PROP_PINKY, (23, 23)), (SCREEN_OFFSET * 34, SCREEN_OFFSET))
    screen.blit(pygame.transform.scale(PROP_CLYDE, (23, 23)), (SCREEN_OFFSET * 42, SCREEN_OFFSET))

    if enable_debug:
        DEBUG_TEXT = GAME_FONT.render("... DEBUG MODE ...", True, (255, 0, 0))
        screen.blit(DEBUG_TEXT, (SCREEN_OFFSET * 53.5, SCREEN_OFFSET * 2.6))

def displayEndCard(screen, win, tile_map):
    end_card_region = pygame.rect.Rect(SCREEN_OFFSET * 9, SCREEN_OFFSET * 20, SCREEN_OFFSET * 30.5, SCREEN_OFFSET * 20)
    pygame.draw.rect(screen, (0, 0, 0), end_card_region)
    pygame.draw.rect(screen, (255, 255, 0), end_card_region, 2)

    if win:
        victory_sfx = pygame.mixer.Sound("Resource\\sfx\\victory.wav")
        victory_sfx.set_volume(0.3)
        victory_sfx.play()
        
        WIN_TEXT = GAME_FONT_LARGE.render("YOU WIN!", True, (255, 255, 0))
        screen.blit(WIN_TEXT, (SCREEN_OFFSET * 16, SCREEN_OFFSET * 22))
        screen.blit(pygame.transform.scale(LETTER_C, (30, 30)), (SCREEN_OFFSET * 12, SCREEN_OFFSET * 26))
        for i in range(4):
            screen.blit(pygame.transform.scale(PROP_SCARED_GHOST, (30, 30)), (SCREEN_OFFSET * 17 + i * 50, SCREEN_OFFSET * 25.8))
    else:
        LOSE_TEXT = GAME_FONT_LARGE.render("GAME OVER!", True, (255, 0, 0))
        screen.blit(LOSE_TEXT, (SCREEN_OFFSET * 14, SCREEN_OFFSET * 22))
        screen.blit(pygame.transform.scale(PACMAN_UP, (30, 30)), (SCREEN_OFFSET * 23, SCREEN_OFFSET * 26))
        screen.blit(pygame.transform.scale(PROP_BLINKY, (30, 30)), (SCREEN_OFFSET * 17 - 40, SCREEN_OFFSET * 25.8))
        screen.blit(pygame.transform.scale(PROP_INKY, (30, 30)), (SCREEN_OFFSET * 17 + 10, SCREEN_OFFSET * 25.8))
        screen.blit(pygame.transform.scale(PROP_PINKY, (30, 30)), (SCREEN_OFFSET * 17 + 112, SCREEN_OFFSET * 25.8))
        screen.blit(pygame.transform.scale(PROP_CLYDE, (30, 30)), (SCREEN_OFFSET * 17 + 158, SCREEN_OFFSET * 25.8))

    score = GAME_FONT.render("SCORE      : " + str(int(tile_map.score)), True, (255, 150, 0))
    screen.blit(score, (SCREEN_OFFSET * 15, SCREEN_OFFSET * 30))

    time_elapsed = pygame.time.get_ticks() - tile_map.start_time

    time_played = GAME_FONT.render("TIME PLAYED: " + str(time_elapsed // 1000) + " secs", True, (255, 150, 0))
    screen.blit(time_played, (SCREEN_OFFSET * 15, SCREEN_OFFSET * 33))

    exit_text = GAME_FONT_SMALL.render("Press ESC to exit.", True, (0, 150, 255))
    screen.blit(exit_text, (SCREEN_OFFSET * 17, SCREEN_OFFSET * 37))

    return end_card_region

def displayDebugInfo(screen, pacman, ghosts_list):
    STATE_TEXT = GAME_FONT_SMALL.render(". STATE .", True, (255, 255, 255))
    POSITION_TEXT = GAME_FONT_SMALL.render(". POSITION .", True, (255, 255, 255))
    TIMER_TEXT = GAME_FONT_SMALL.render(". TIMER .", True, (255, 255, 255))
    screen.blit(POSITION_TEXT, (SCREEN_OFFSET * 50, SCREEN_OFFSET * 6.8))
    screen.blit(STATE_TEXT, (SCREEN_OFFSET * 61.5, SCREEN_OFFSET * 6.8))
    screen.blit(TIMER_TEXT, (SCREEN_OFFSET * 69.5, SCREEN_OFFSET * 6.8))

    #display pacman info
    PACMAN_NAME = GAME_FONT_SMALL.render("PACMAN", True, (255, 255, 0))
    PACMAN_POS_TEXT = GAME_FONT_SMALL.render(": " +
                                            ("0" if pacman.x < 10 else "") + #single digit is padded
                                            str(pacman.x) + ", " + 
                                            ("0" if pacman.y < 10 else "") + #single digit is padded
                                            str(pacman.y), True, (255, 255, 255))
    
    screen.blit(PACMAN_NAME, (SCREEN_OFFSET * 49, SCREEN_OFFSET * 8.8))
    screen.blit(PACMAN_POS_TEXT, (SCREEN_OFFSET * 54, SCREEN_OFFSET * 8.8))
    screen.blit(GAME_FONT_SMALL.render(("ALIVE" if pacman.dead == False else "DEAD"), True, (255, 255, 255)), (SCREEN_OFFSET * 63, SCREEN_OFFSET * 8.8))

    #display ghosts state
    for i in range(0, len(ghosts_list)):
        GHOST_NAME = GAME_FONT_SMALL.render(str(ghosts_list[i].name), True, ghost_colors[ghosts_list[i].name])
        GHOST_POS_TEXT = GAME_FONT_SMALL.render(": " + 
                                                ("0" if ghosts_list[i].x < 10 else "") + #single digit is padded
                                                str(ghosts_list[i].x) + ", " + 
                                                ("0" if ghosts_list[i].y < 10 else "") + #single digit is padded
                                                str(ghosts_list[i].y), True, (255, 255, 255))
        GHOST_STATE_TEXT = GAME_FONT_SMALL.render(ghosts_list[i].state, True, (255, 255, 255))
        screen.blit(GHOST_NAME, (SCREEN_OFFSET * 49, SCREEN_OFFSET * (12.8 + i * 2)))
        screen.blit(GHOST_POS_TEXT, (SCREEN_OFFSET * 54, SCREEN_OFFSET * (12.8 + i * 2)))
        screen.blit(GHOST_STATE_TEXT, (SCREEN_OFFSET * 63, SCREEN_OFFSET * (12.8 + i * 2)))
    
    #display ghost state timer
    for i in range(0, len(ghosts_list)):
        if ghosts_list[i].state == "SCATTER":
            GHOST_TIMER_TEXT = GAME_FONT_SMALL.render(str(ghosts_list[i].scatter_time), True, (255, 255, 255))
            screen.blit(GHOST_TIMER_TEXT, (SCREEN_OFFSET * 72, SCREEN_OFFSET * (12.8 + i * 2)))
        if ghosts_list[i].state == "CHASE":
            GHOST_TIMER_TEXT = GAME_FONT_SMALL.render(str(ghosts_list[i].chase_time), True, (255, 255, 255))
            screen.blit(GHOST_TIMER_TEXT, (SCREEN_OFFSET * 72, SCREEN_OFFSET * (12.8 + i * 2)))
        if ghosts_list[i].state == "SCARED":
            GHOST_TIMER_TEXT = GAME_FONT_SMALL.render(str(ghosts_list[i].scared_time), True, (255, 255, 255))
            screen.blit(GHOST_TIMER_TEXT, (SCREEN_OFFSET * 72, SCREEN_OFFSET * (12.8 + i * 2)))

def displayTestScreen(screen):
    TEST_TEXT = GAME_FONT_LARGE.render("... TEST MODE ...", True, (0, 255, 255))
    screen.blit(TEST_TEXT, (SCREEN_OFFSET * 53.5, SCREEN_OFFSET * 2.6))

    dc0 = "Welcome to the test screen!"
    dc1 = "This screen is used to show the pathfinding of the ghosts"

    dc2 = "Move Pacman with Arrow keys or Mouse Dragging"
    dc3 = "The ghosts will always chase Pacman"
    dc4 = "A ghost will automatically stop when it reaches pacman"

    dc5 = "Blinky (red) uses A* pathfinding"
    dc6 = "Inky (cyan) uses UCS pathfinding"
    dc7 = "Pinky (pink) uses DFS/IDS pathfinding"
    dc8 = "Clyde (orange) uses BFS pathfinding"

    dc9 =  "            .. Ghost Controls .."
    dc10 = "                   . Mouse .         . Keyboard ."
    dc11 = "Selection:           [NONE]            Number 1-4"
    dc12 = "Change Direction:    RMB               Right Click"
    dc13 = "Move Position:       Drag LMB          W A S D"
    dc14 = "Start Update:        LMB               Number 1-4"
    dc15 = "Reset ALL Position:  [NONE]            R"
    dc16 = "Refresh Screen:      [NONE]            C"
    dc17 = "Select Preset Test:  [NONE]            LSHIFT + Number 1-5"

    description = [dc0, dc1, dc2, dc3, dc4, dc5, dc6, dc7, dc8, dc9, dc10, dc11, dc12, dc13, dc14, dc15, dc16, dc17]
    block = 2
    for i in range(len(description)):
        if(i == 9): dc_text = GAME_FONT.render(description[i], True, (0, 255, 255))
        elif (i == 5): dc_text = GAME_FONT_SMALL.render(description[i], True, (255, 0, 0))
        elif (i == 6): dc_text = GAME_FONT_SMALL.render(description[i], True, (0, 255, 255))
        elif (i == 7): dc_text = GAME_FONT_SMALL.render(description[i], True, (255, 105, 180))
        elif (i == 8): dc_text = GAME_FONT_SMALL.render(description[i], True, (255, 165, 0))
        elif (i == 10): dc_text = GAME_FONT_SMALL.render(description[i], True, (255, 150, 0))
        else: dc_text = GAME_FONT_SMALL.render(description[i], True, (255, 255, 255))
        screen.blit(dc_text, (SCREEN_OFFSET * 50, SCREEN_OFFSET * (4 + block * 1.5)))
        if(i == 1 or i == 4 or i == 8 or i == 9):
            block += 2
        else:
            block += 1
        
def setupTestScreen(screen, pacman, ghosts_list, tilemap, clear_map, update_ghosts, update_region, preset, preset_position):
    if(not clear_map):
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                if(tilemap.tilemap[i][j] < -1 and tilemap.tilemap[i][j] > -9):
                    tilemap.tilemap[i][j] = -1
        clear_map = True

    ghosts_list[0].x, ghosts_list[0].y = preset_position[preset][1][0], preset_position[preset][1][1] #blinky
    ghosts_list[1].x, ghosts_list[1].y = preset_position[preset][2][0], preset_position[preset][2][1] #inky
    ghosts_list[2].x, ghosts_list[2].y = preset_position[preset][3][0], preset_position[preset][3][1] #pinky
    ghosts_list[3].x, ghosts_list[3].y = preset_position[preset][4][0], preset_position[preset][4][1] #clyde

    pacman.x, pacman.y = preset_position[preset][0][0], preset_position[preset][0][1]
    pacman.snapDisplayToGrid()

    update_ghosts[0] = False
    update_ghosts[1] = False
    update_ghosts[2] = False
    update_ghosts[3] = False

    for g in ghosts_list:
        g.MAX_SCATTER_TIME = 0
        g.scatter_time = 0
        g.MAX_CHASE_TIME = 10000
        g.update(tilemap.tilemap, pacman, ghosts_list, True)
        g.snapDisplayToGrid()
    
    screen.fill((0, 0, 0), update_region)
    pygame.display.update()
    
    return clear_map, update_ghosts

def displayGameInfo(screen, pacman, tile_map):
    #display pacman lives
    LIVES_TEXT = GAME_FONT.render("LIVES: ", True, (255, 255, 255))
    screen.blit(LIVES_TEXT, (SCREEN_OFFSET, SCREEN_HEIGHT - 20))
    for i in range(0, pacman.lives):
        screen.blit(lives_image, (SCREEN_OFFSET * 7 + i * 20, SCREEN_HEIGHT - 20))

    #display score
    SCORE_TEXT = GAME_FONT.render("SCORE: " + str(int(tile_map.score)), True, (255, 255, 255)) #placeholder value, replace with score variable
    screen.blit(SCORE_TEXT, (SCREEN_OFFSET * 35, SCREEN_HEIGHT - 20))

    #display pellets left
    PELLETS_COUNT = GAME_FONT_SMALL.render(str(tile_map.pellet_count), True, (255, 255, 255))
    screen.blit(PELLETS_COUNT, (SCREEN_OFFSET * 72, SCREEN_OFFSET * 8.8))

def flashText(screen, last_toggle_time, show_text, text, text2):
    current_time = pygame.time.get_ticks() 
    if current_time - last_toggle_time >= 400: #switch every 200ms
        show_text = not show_text  
        last_toggle_time = current_time  

    if show_text:
        screen.blit(text, (SCREEN_OFFSET * 21.5, SCREEN_OFFSET * 37))
    else:
        screen.blit(text2, (SCREEN_OFFSET * 21.5, SCREEN_OFFSET * 37))

    pygame.display.flip()

    return last_toggle_time, show_text

def ReadMap():
    file = open("Resource\\map\\map.txt")
    m = [[0] * MAP_WIDTH]

    for i in range(1, MAP_HEIGHT + 1):
        line = file.readline()
        m.append([0] + list(map(int, line.split())) + [0])

    m.append([0] * MAP_WIDTH)

    file.close()
    return m

class Tilemap:
    def __init__(self, filename):
        self.tilemap = ReadMap()
        self.tileset = pygame.image.load(filename)
        self.tileset = pygame.transform.scale_by(self.tileset, (TILE_SIZE / TILE_RESU, TILE_SIZE / TILE_RESU))

        pellet = pygame.image.load("Resource\\food\\pellet.png")
        power_pellet = pygame.image.load("Resource\\food\\power_pellet.png")
        cherry = pygame.image.load("Resource\\food\\cherry.png")
        orange = pygame.image.load("Resource\\food\\orange.png")
        apple = pygame.image.load("Resource\\food\\apple.png")
        strawberry = pygame.image.load("Resource\\food\\strawberry.png")

        self.food_list = [pellet, power_pellet, cherry, orange, apple, strawberry]

        for i in range(len(self.food_list)):
            self.food_list[i] = pygame.transform.scale(self.food_list[i], (TILE_SIZE, TILE_SIZE))

        self.pellet_count = 285 + 4 # 4 power pellets 
        self.score = 1000 # starting value

        self.start_time = 0

    def render(self, screen):
        self.score -= 0.1

        for i in range(1, MAP_HEIGHT + 1):
            for j in range(1, MAP_WIDTH + 1):
                # Empty cell
                if (self.tilemap[i][j] < 0):
                    match (self.tilemap[i][j]):
                        case -2:
                            screen.blit(self.food_list[0], (SCREEN_OFFSET + (j - 1) * TILE_SIZE, SCREEN_OFFSET + (i - 1) * TILE_SIZE)) #pellet
                        case -3:
                            screen.blit(self.food_list[1], (SCREEN_OFFSET + (j - 1) * TILE_SIZE, SCREEN_OFFSET + (i - 1) * TILE_SIZE)) #power pellet
                        case -4:
                            screen.blit(self.food_list[2], (SCREEN_OFFSET + (j - 1) * TILE_SIZE, SCREEN_OFFSET + (i - 1) * TILE_SIZE)) #cherry
                        case -5:
                            screen.blit(self.food_list[3], (SCREEN_OFFSET + (j - 1) * TILE_SIZE, SCREEN_OFFSET + (i - 1) * TILE_SIZE)) #orange
                        case -6:
                            screen.blit(self.food_list[4], (SCREEN_OFFSET + (j - 1) * TILE_SIZE, SCREEN_OFFSET + (i - 1) * TILE_SIZE)) #apple
                        case -7:
                            screen.blit(self.food_list[5], (SCREEN_OFFSET + (j - 1) * TILE_SIZE, SCREEN_OFFSET + (i - 1) * TILE_SIZE))
                        case _:
                            continue

                y, x = (self.tilemap[i][j] % 10), (self.tilemap[i][j] // 10)
                src = pygame.Rect(y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                dst = self.tileset.get_rect()
                dst.x = SCREEN_OFFSET + (j - 1) * TILE_SIZE
                dst.y = SCREEN_OFFSET + (i - 1) * TILE_SIZE
                dst.w = TILE_SIZE
                dst.h = TILE_SIZE

                screen.blit(self.tileset, dst, src)
