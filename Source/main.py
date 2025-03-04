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

#load pngs
lives = pygame.image.load("Resource\\pacman\\movement_animation\\right\\2.png")

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

starting_positions = [pacman_starting_position, blinky_starting_position, clyde_starting_position, inky_starting_position, pinky_starting_position]

pacman = pacman_m.Pacman(pacman_starting_position, "NONE")
blinky = ghosts.Ghost(blinky_starting_position, "UP", "blinky")
clyde = ghosts.Ghost(clyde_starting_position, "UP", "clyde")
inky = ghosts.Ghost(inky_starting_position, "UP", "inky")
pinky = ghosts.Ghost(pinky_starting_position, "UP", "pinky")

ghosts_list = [blinky, clyde, inky, pinky]

# load map
tilemap = TMap.Tilemap("Resource\\map\\map.png")

# display game info
game_font = pygame.font.Font("Resource\\text_font\\Emulogic-zrEw.ttf", 10)
game_font_LARGE = pygame.font.Font("Resource\\text_font\\Emulogic-zrEw.ttf", 21)
def displayGameInfo(screen, pacman):
    #display pacman lives
    LIVES_TEXT = game_font.render("LIVES: ", True, (255, 255, 255))
    screen.blit(LIVES_TEXT, (SCREEN_OFFSET, SCREEN_HEIGHT - 20))
    for i in range(0, pacman.lives):
        screen.blit(lives, (SCREEN_OFFSET * 7 + i * 20, SCREEN_HEIGHT - 20))

    #display score
    SCORE_TEXT = game_font.render("SCORE: " + str(69420), True, (255, 255, 255)) #placeholder value, replace with score variable
    screen.blit(SCORE_TEXT, (SCREEN_OFFSET * 35, SCREEN_HEIGHT - 20))

    #display game name
    GAME_NAME = game_font_LARGE.render("PACMAN", True, (255, 255, 0))
    screen.blit(GAME_NAME, (SCREEN_OFFSET * 18, 0 + 30))

def flashReadyText(screen, last_toggle_time, show_text):
    current_time = pygame.time.get_ticks() 
    if current_time - last_toggle_time >= 400: #switch every 200ms
        show_text = not show_text  
        last_toggle_time = current_time  

    if show_text:
        screen.blit(READY_TEXT, (SCREEN_OFFSET * 21.5, SCREEN_OFFSET * 34.6))
    else:
        screen.blit(BLACK_READY_TEXT, (SCREEN_OFFSET * 21.5, SCREEN_OFFSET * 34.6))

    pygame.display.flip()

    return last_toggle_time, show_text

#starting sequence
intro_sfx = pygame.mixer.Sound("Resource\\sfx\\intro.wav")
READY_TEXT = game_font.render("READY!", True, (255, 255, 0))
BLACK_READY_TEXT = game_font.render("READY!", True, (0, 0, 0))
start = True
enable_intro = True

# pause time
pause_time = 4500 #milliseconds
pausing = pygame.time.get_ticks() + pause_time

print("something something all those pngs file are corrupted or sth idk man i just work here")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.constants.K_ESCAPE):
                running = False

            if (event.key in input_mapping and pacman.lock_turn_time == 0 and not pacman.dead):
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
    if(pacman.checkCollision(ghosts_list, starting_positions)):
        print("lmao ur so bad on god frfr")
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
    if(not start or not enable_intro):
        screen.fill("black")

    # display game info
    displayGameInfo(screen, pacman)

    # starting sequence
    if start and enable_intro:
        start = False
        intro_sfx.play()
        last_toggle_time = 0
        show_text = True
        while pygame.time.get_ticks() < pausing:
            last_toggle_time, show_text = flashReadyText(screen, last_toggle_time, show_text)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            if not running:
                break

    FPS = 60
    clock.tick(FPS) 

pygame.quit()