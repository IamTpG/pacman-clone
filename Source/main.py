# imports
import pygame
import time

# local
import pacman as pacman_m
import ghosts
import tile_map_constants

# Constants
TILE_RESU = tile_map_constants.TILE_RESU
TILE_SIZE = tile_map_constants.TILE_SIZE

MAP_WIDTH = tile_map_constants.MAP_WIDTH
MAP_HEIGHT = tile_map_constants.MAP_HEIGHT

SCREEN_OFFSET = tile_map_constants.SCREEN_OFFSET
SCREEN_WIDTH = tile_map_constants.SCREEN_WIDTH
SCREEN_HEIGHT = tile_map_constants.SCREEN_HEIGHT

# Utils function for reading tilemap
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

ghosts = [blinky, clyde, inky, pinky]

tilemap = Tilemap("Resource\\map\\map.png")

while running:
    if not start:
        #intro_sfx.play()
        start = True
    
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
                for ghost in ghosts: ghost.unfreeze()
            if (event.key == pygame.constants.K_DOWN and pacman.lock_turn_time == 0):
                pacman.queue_turn = "DOWN"
                pacman.queue_time = pacman.MAX_QUEUE_TIME
                for ghost in ghosts: ghost.unfreeze()
            if (event.key == pygame.constants.K_LEFT and pacman.lock_turn_time == 0):
                pacman.queue_turn = "LEFT"
                pacman.queue_time = pacman.MAX_QUEUE_TIME
                for ghost in ghosts: ghost.unfreeze()
            if (event.key == pygame.constants.K_RIGHT and pacman.lock_turn_time == 0):
                pacman.queue_turn = "RIGHT"
                pacman.queue_time = pacman.MAX_QUEUE_TIME
                for ghost in ghosts: ghost.unfreeze()

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
    if pacman.checkCollision(ghosts):
        for ghost in ghosts:
            if not ghost.feared_state:
                if pacman.lives == 0:
                    running = False
                pacman.reset(pacman_starting_position, "NONE")
                blinky.reset(blinky_starting_position, "UP")
                clyde.reset(clyde_starting_position, "UP")
                inky.reset(inky_starting_position, "UP")
                pinky.reset(pinky_starting_position, "UP")
                break
        
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