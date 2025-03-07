if __name__ == '__main__':
    print("This is a module, it should not be run standalone!")

import pygame

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

# debug mode
def enableDebugMode(screen_width):
    screen_width += 300
    #new screen size
    screen = pygame.display.set_mode((screen_width + SCREEN_OFFSET * 2, SCREEN_HEIGHT + SCREEN_OFFSET * 2))

def displayDebugInfo(screen, pacman, ghosts_list):
    debug_text = GAME_FONT.render("... DEBUG MODE ...", True, (255, 0, 0))
    screen.blit(debug_text, (SCREEN_OFFSET * 54, SCREEN_OFFSET * 3.8))

    STATE_TEXT = GAME_FONT_SMALL.render(". STATE .", True, (255, 255, 255))
    POSITION_TEXT = GAME_FONT_SMALL.render(". POSITION .", True, (255, 255, 255))
    screen.blit(POSITION_TEXT, (SCREEN_OFFSET * 50.5, SCREEN_OFFSET * 6.8))
    screen.blit(STATE_TEXT, (SCREEN_OFFSET * 65.5, SCREEN_OFFSET * 6.8))

    #display pacman info
    PACMAN_NAME = GAME_FONT_SMALL.render("PACMAN", True, (255, 255, 0))
    PACMAN_POS_TEXT = GAME_FONT_SMALL.render(": " +
                                            ("0" if pacman.x < 10 else "") + #single digit is padded
                                            str(pacman.x) + ", " + 
                                            ("0" if pacman.y < 10 else "") + #single digit is padded
                                            str(pacman.y), True, (255, 255, 255))
    
    screen.blit(PACMAN_NAME, (SCREEN_OFFSET * 49, SCREEN_OFFSET * 8.8))
    screen.blit(PACMAN_POS_TEXT, (SCREEN_OFFSET * 54, SCREEN_OFFSET * 8.8))
    screen.blit(GAME_FONT_SMALL.render(("ALIVE" if pacman.dead == False else "DEAD"), True, (255, 255, 255)), 
                (SCREEN_OFFSET * 67, SCREEN_OFFSET * 8.8))
   
    #display ghosts info
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
        screen.blit(GHOST_STATE_TEXT, (SCREEN_OFFSET * 67, SCREEN_OFFSET * (12.8 + i * 2)))

def displayGameInfo(screen, pacman):
    #display pacman lives
    LIVES_TEXT = GAME_FONT.render("LIVES: ", True, (255, 255, 255))
    screen.blit(LIVES_TEXT, (SCREEN_OFFSET, SCREEN_HEIGHT - 20))
    for i in range(0, pacman.lives):
        screen.blit(lives_image, (SCREEN_OFFSET * 7 + i * 20, SCREEN_HEIGHT - 20))

    #display score
    SCORE_TEXT = GAME_FONT.render("SCORE: " + str(69420), True, (255, 255, 255)) #placeholder value, replace with score variable
    screen.blit(SCORE_TEXT, (SCREEN_OFFSET * 35, SCREEN_HEIGHT - 20))

    #display game name
    GAME_NAME = GAME_FONT_LARGE.render("PACMAN", True, (255, 255, 0))
    screen.blit(GAME_NAME, (SCREEN_OFFSET * 18, 0 + 30))

def flashText(screen, last_toggle_time, show_text, text, text2):
    current_time = pygame.time.get_ticks() 
    if current_time - last_toggle_time >= 400: #switch every 200ms
        show_text = not show_text  
        last_toggle_time = current_time  

    if show_text:
        screen.blit(text, (SCREEN_OFFSET * 21.5, SCREEN_OFFSET * 34.6))
    else:
        screen.blit(text2, (SCREEN_OFFSET * 21.5, SCREEN_OFFSET * 34.6))

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
    
    def render(self, screen):
        for i in range(1, MAP_HEIGHT + 1):
            for j in range(1, MAP_WIDTH + 1):
                # Empty cell
                if (self.tilemap[i][j] < 0):
                    continue

                y, x = (self.tilemap[i][j] % 10), (self.tilemap[i][j] // 10)
                src = pygame.Rect(y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                dst = self.tileset.get_rect()
                dst.x = SCREEN_OFFSET + (j - 1) * TILE_SIZE
                dst.y = SCREEN_OFFSET + (i - 1) * TILE_SIZE
                dst.w = TILE_SIZE
                dst.h = TILE_SIZE

                screen.blit(self.tileset, dst, src)
