# Example file showing a basic pygame "game loop"
import pygame
import random

# pygame setup
TILE_RESU = 8   # Tile size in .png
TILE_SIZE = 16  # Tile size to render

MAP_WIDTH  = 29
MAP_HEIGHT = 37

SCREEN_OFFSET = 10
SCREEN_WIDTH  = MAP_WIDTH  * TILE_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE

PACMAN_SPEED  = 2
PACMAN_RADIUS = TILE_SIZE - 5

GHOST_SPEED = 1
GHOST_RADIUS = TILE_SIZE - 5

# Utils function for reading tilemap
def ReadMap():
    file = open("Resource/map/map.txt")
    m = [[0] * MAP_WIDTH]

    for i in range(1, MAP_HEIGHT + 1):
        line = file.readline()
        m.append([0] + list(map(int, line.split())) + [0])

    m.append([0] * MAP_WIDTH)

    file.close()
    return m

def loadPacmanFrames():
    frame1UP = pygame.image.load("Resource\\pacman-up\\1.png")
    frame2UP = pygame.image.load("Resource\\pacman-up\\2.png")
    frame3UP = pygame.image.load("Resource\\pacman-up\\3.png")
    frame1DOWN = pygame.image.load("Resource\\pacman-down\\1.png")
    frame2DOWN = pygame.image.load("Resource\\pacman-down\\2.png")
    frame3DOWN = pygame.image.load("Resource\\pacman-down\\3.png")
    frame1LEFT = pygame.image.load("Resource\\pacman-left\\1.png")
    frame2LEFT = pygame.image.load("Resource\\pacman-left\\2.png")
    frame3LEFT = pygame.image.load("Resource\\pacman-left\\3.png")
    frame1RIGHT = pygame.image.load("Resource\\pacman-right\\1.png")
    frame2RIGHT = pygame.image.load("Resource\\pacman-right\\2.png")
    frame3RIGHT = pygame.image.load("Resource\\pacman-right\\3.png")

    frames = [[
                frame1UP, frame2UP, frame3UP
            ], [
                frame1DOWN, frame2DOWN, frame3DOWN
            ], [
                frame1LEFT, frame2LEFT, frame3LEFT
            ], [
                frame1RIGHT, frame2RIGHT, frame3RIGHT
            ]
        ]

    SCALING_FACTOR = 2
    
    for i in range(4):
        for j in range(3):
            frames[i][j] = pygame.transform.scale(frames[i][j], (PACMAN_RADIUS * SCALING_FACTOR, PACMAN_RADIUS * SCALING_FACTOR))

    return frames

def loadGhostFrames(name):
    blinky = pygame.image.load("Resource/ghosts/blinky.png")
    inky = pygame.image.load("Resource/ghosts/inky.png")
    pinky = pygame.image.load("Resource/ghosts/pinky.png")
    clyde = pygame.image.load("Resource/ghosts/clyde.png")
    blue_ghost = pygame.image.load("Resource/ghosts/blue_ghost.png")

    if name == "blinky":
        frames = [blinky, blue_ghost]
    elif name == "inky":
        frames = [inky, blue_ghost]
    elif name == "pinky":
        frames = [pinky, blue_ghost]
    elif name == "clyde":
        frames = [clyde, blue_ghost]

    SCALING_FACTOR = 2
    for i in range(2):
        frames[i] = pygame.transform.scale(frames[i], (GHOST_RADIUS * SCALING_FACTOR, GHOST_RADIUS * SCALING_FACTOR))

    return frames


class Pacman:
    def __init__(self, x, y, radius, direction):
        # animation
        self.frames = loadPacmanFrames()
        self.frame_counter = 0

        # lock turning 
        self.lock_turn_time = 0

        # save the next turn and time before it is reset
        self.queue_turn = "NONE"
        self.MAX_QUEUE_TIME = 3
        self.queue_time = self.MAX_QUEUE_TIME

        # position 
        self.x = x
        self.y = y
        self.display_x = self.x * TILE_SIZE + SCREEN_OFFSET - radius + 3
        self.display_y = self.y * TILE_SIZE + SCREEN_OFFSET - radius + 4
        self.radius = radius
        self.direction = direction
    
    def snapDisplayToGrid(self):
        self.display_x = self.x * TILE_SIZE + SCREEN_OFFSET - self.radius + 3
        self.display_y = self.y * TILE_SIZE + SCREEN_OFFSET - self.radius + 4

    def checkObstructionDirection(self, tile_map, direction):
        OFFSET = 1
        if (direction == "UP"):
            if (tile_map[self.y - OFFSET][self.x] != -1):
                return True
        if (direction == "DOWN"):
            if (tile_map[self.y + OFFSET][self.x] != -1):
                return True
        if (direction == "LEFT"):
            if (tile_map[self.y][self.x - OFFSET] != -1):
                return True
        if (direction == "RIGHT"):
            if (tile_map[self.y][self.x + OFFSET] != -1):
                return True

    
    def canTurn(self, tile_map, wanted_direction):
        if wanted_direction == "NONE":
            return False
        
        if wanted_direction == self.direction:
            return False

        return not self.checkObstructionDirection(tile_map, wanted_direction)

    def update(self, tile_map):
        DEBUG = True
        if (DEBUG): 
            print("Tile Map Cords: X: " + str(self.x) + " Y: " + str(self.y) + 
                " | Queue Turn: " + self.queue_turn +
                " | Direction: " + self.direction +
                " | Obstruction: " + str(self.checkObstructionDirection(tile_map, self.direction)))
        
        if(self.queue_time == 0):
            self.queue_turn = "NONE"
            self.queue_time = self.MAX_QUEUE_TIME

        if(self.canTurn(tile_map, self.queue_turn) == True):
            self.snapDisplayToGrid()
            self.direction = self.queue_turn
            self.queue_turn = "NONE"
            self.lock_turn_time = 1

        if (self.checkObstructionDirection(tile_map, self.direction)):
            self.queue_turn = "NONE"
            return

        VERTICAL_OFFSET = 3
        HORIZONTAL_OFFSET = 2
        
        if (self.direction == "UP"):
            self.display_y -= PACMAN_SPEED
            if(self.display_y / TILE_SIZE < self.y and self.display_y % TILE_SIZE == VERTICAL_OFFSET):   
                self.y -= 1
                self.queue_time -= 1
                if(self.lock_turn_time > 0): self.lock_turn_time -= 1
        if (self.direction == "DOWN"):  
            self.display_y += PACMAN_SPEED
            if(self.display_y / TILE_SIZE > self.y and self.display_y % TILE_SIZE == VERTICAL_OFFSET):
                self.y += 1
                self.queue_time -= 1
                if(self.lock_turn_time > 0): self.lock_turn_time -= 1
        if (self.direction == "LEFT"):  
            self.display_x -= PACMAN_SPEED
            if(self.display_x / TILE_SIZE < self.x and self.display_x % TILE_SIZE == HORIZONTAL_OFFSET):
                self.x -= 1
                self.queue_time -= 1
                if(self.lock_turn_time > 0): self.lock_turn_time -= 1
        if (self.direction == "RIGHT"): 
            self.display_x += PACMAN_SPEED
            if(self.display_x / TILE_SIZE > self.x and self.display_x % TILE_SIZE == HORIZONTAL_OFFSET):
                self.x += 1
                self.queue_time -= 1
                if(self.lock_turn_time > 0): self.lock_turn_time -= 1

        if (self.display_x < SCREEN_OFFSET + self.radius and self.direction == "LEFT"): 
            self.display_x = SCREEN_WIDTH
            self.x = MAP_WIDTH
        if (self.display_x > SCREEN_WIDTH and self.direction == "RIGHT"):  
            self.display_x = SCREEN_OFFSET
            self.x = 0
    
    def render(self, screen):
        direction_mapping = {
            "UP": 0,
            "DOWN": 1,
            "LEFT": 2,
            "RIGHT": 3,
            "NONE" : 1
        }

        # starting frame
        if(self.direction == "NONE"): 
            screen.blit(self.frames[direction_mapping[self.direction]][0], (self.display_x - PACMAN_RADIUS, self.display_y - PACMAN_RADIUS))
            return

        # Draws open mouth if obstructed
        if(self.checkObstructionDirection(tilemap.tilemap, self.direction) == True):   self.frame_counter = 0

        FRAME_DURATION = 8 
        frame_index = (self.frame_counter // FRAME_DURATION) % 3  # Cycles between frame 1 2 and 3

        screen.blit(self.frames[direction_mapping[self.direction]][frame_index], (self.display_x - PACMAN_RADIUS, self.display_y - PACMAN_RADIUS))

        # only increment frame counter if not obstructed
        if not self.checkObstructionDirection(tilemap.tilemap, self.direction):
            self.frame_counter = (self.frame_counter + 1) % (FRAME_DURATION * 3)

class Ghost:
    def __init__(self, x, y, radius, direction, name):
        # animation
        self.frames = loadGhostFrames(name)
        self.feared_state = False

        # lock turning
        self.lock_turn_time = 0

        # position 
        self.x = x
        self.y = y
        self.display_x = self.x * TILE_SIZE + SCREEN_OFFSET - radius + 3
        self.display_y = self.y * TILE_SIZE + SCREEN_OFFSET - radius + 4
        self.radius = radius
        self.direction = direction
    
    def snapDisplayToGrid(self):
        self.display_x = self.x * TILE_SIZE + SCREEN_OFFSET - self.radius + 3
        self.display_y = self.y * TILE_SIZE + SCREEN_OFFSET - self.radius + 4

    def getDirection(self):
        direction_mapping = {
            0: "UP",
            1: "DOWN",
            2: "LEFT",
            3: "RIGHT"
        }

        return direction_mapping[random.randint(0, 3)]

    def checkObstructionDirection(self, tile_map, direction):
        OFFSET = 1
        if (direction == "UP"):
            if (tile_map[self.y - OFFSET][self.x] != -1):
                return True
        if (direction == "DOWN"):
            if (tile_map[self.y + OFFSET][self.x] != -1):
                return True
        if (direction == "LEFT"):
            if (tile_map[self.y][self.x - OFFSET] != -1):
                return True
        if (direction == "RIGHT"):
            if (tile_map[self.y][self.x + OFFSET] != -1):
                return True

    
    def canTurn(self, tile_map, wanted_direction):
        if wanted_direction == "NONE":
            return False
        
        if wanted_direction == self.direction:
            return False

        return not self.checkObstructionDirection(tile_map, wanted_direction)

    def update(self, tile_map):
        if(self.canTurn(tile_map, self.direction) == True):
            self.snapDisplayToGrid()
            self.direction = self.getDirection()
            self.lock_turn_time = 1

        if (self.checkObstructionDirection(tile_map, self.direction)):
            self.direction = self.getDirection()
        
        VERTICAL_OFFSET = 3
        HORIZONTAL_OFFSET = 2
        
        if (self.direction == "UP"):
            self.display_y -= GHOST_SPEED
            if(self.display_y / TILE_SIZE < self.y and self.display_y % TILE_SIZE == VERTICAL_OFFSET):   
                self.y -= 1
                if(self.lock_turn_time > 0): self.lock_turn_time -= 1
        if (self.direction == "DOWN"):  
            self.display_y += GHOST_SPEED
            if(self.display_y / TILE_SIZE > self.y and self.display_y % TILE_SIZE == VERTICAL_OFFSET):
                self.y += 1
                if(self.lock_turn_time > 0): self.lock_turn_time -= 1
        if (self.direction == "LEFT"):  
            self.display_x -= GHOST_SPEED
            if(self.display_x / TILE_SIZE < self.x and self.display_x % TILE_SIZE == HORIZONTAL_OFFSET):
                self.x -= 1
                if(self.lock_turn_time > 0): self.lock_turn_time -= 1
        if (self.direction == "RIGHT"): 
            self.display_x += GHOST_SPEED
            if(self.display_x / TILE_SIZE > self.x and self.display_x % TILE_SIZE == HORIZONTAL_OFFSET):
                self.x += 1
                if(self.lock_turn_time > 0): self.lock_turn_time -= 1

        if (self.display_x < SCREEN_OFFSET + self.radius and self.direction == "LEFT"): 
            self.display_x = SCREEN_WIDTH
            self.x = MAP_WIDTH
        if (self.display_x > SCREEN_WIDTH and self.direction == "RIGHT"):  
            self.display_x = SCREEN_OFFSET
            self.x = 0
    
    def render(self, screen):
        if(self.feared_state == True):
            screen.blit(self.frames[1], (self.display_x - GHOST_RADIUS, self.display_y - GHOST_RADIUS))
        else:
            screen.blit(self.frames[0], (self.display_x - GHOST_RADIUS, self.display_y - GHOST_RADIUS))

      

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
screen = pygame.display.set_mode((SCREEN_WIDTH + SCREEN_OFFSET * 2, SCREEN_HEIGHT + SCREEN_OFFSET * 2))
clock = pygame.time.Clock()
running = True

pacman = Pacman(2, 6, PACMAN_RADIUS, "NONE")
blinky = Ghost(14, 19, GHOST_RADIUS, "UP", "blinky")
tilemap = Tilemap("Resource/map/map.png")

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

    # update pacman
    pacman.update(tilemap.tilemap)

    # update ghosts
    blinky.update(tilemap.tilemap)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # draw your work on the screen
    tilemap.render(screen)
    pacman.render(screen)
    blinky.render(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    FPS = 60
    clock.tick(FPS) 

pygame.quit()
