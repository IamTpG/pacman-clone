# Example file showing a basic pygame "game loop"
import pygame

# Load PNGS
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

class Pacman:
    def __init__(self, x, y, radius, direction):
        self.frame_counter = 0
        self.x = x
        self.y = y
        self.display_x = self.x * TILE_SIZE + SCREEN_OFFSET - radius + 3
        self.display_y = self.y * TILE_SIZE + SCREEN_OFFSET - radius + 9
        self.radius = radius
        self.direction = direction
    
    def snapDisplayToGrid(self):
        self.display_x = self.x * TILE_SIZE + SCREEN_OFFSET - self.radius + 3
        self.display_y = self.y * TILE_SIZE + SCREEN_OFFSET - self.radius + 9

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

        return False
    
    def moveInDirection(self, tile_map, direction):
        if(direction == "UP" and self.direction == "DOWN" and self.checkObstructionDirection(tile_map, "DOWN") == False): return False
        if(direction == "DOWN" and self.direction == "UP" and self.checkObstructionDirection(tile_map, "UP") == False): return False
        if(direction == "LEFT" and self.direction == "RIGHT" and self.checkObstructionDirection(tile_map, "RIGHT") == False): return False
        if(direction == "RIGHT" and self.direction == "LEFT" and self.checkObstructionDirection(tile_map, "LEFT") == False): return False

        if (direction == "UP"):
            if(self.checkObstructionDirection(tile_map, "UP") == False):
                return True
            else:   return False
        
        if (direction == "DOWN"):
            if(self.checkObstructionDirection(tile_map, "DOWN") == False):
                return True
            else:   return False

        if (direction == "LEFT"):
            if(self.checkObstructionDirection(tile_map, "LEFT") == False):
                return True
            else:   return False

        if (direction == "RIGHT"):
            if(self.checkObstructionDirection(tile_map, "RIGHT") == False):
                return True
            else:   return False

    def update(self, tile_map):
        DEBUG = False
        if (DEBUG): return

        print("X: " + str(self.x) + " Y: " + str(self.y) + " | Tile map value: " +
              str(tile_map[self.y][self.x]) + " | Direction: " + self.direction +
                " | Obstruction: " + str(self.checkObstructionDirection(tile_map, self.direction)))

        if (self.checkObstructionDirection(tile_map, self.direction)):
            return

        VERTICAL_OFFSET = 6
        HORIZONTAL_OFFSET = 2

        if (self.direction == "UP"):    
            self.display_y -= PACMAN_SPEED
            if(self.display_y / TILE_SIZE < self.y and self.display_y % TILE_SIZE == VERTICAL_OFFSET):    
                self.y -= 1
                self.snapDisplayToGrid()
        if (self.direction == "DOWN"):  
            self.display_y += PACMAN_SPEED
            if(self.display_y / TILE_SIZE > self.y and self.display_y % TILE_SIZE == VERTICAL_OFFSET):    
                self.y += 1 
                self.snapDisplayToGrid()
        if (self.direction == "LEFT"):  
            self.display_x -= PACMAN_SPEED
            if(self.display_x / TILE_SIZE < self.x and self.display_x % TILE_SIZE == HORIZONTAL_OFFSET):    
                self.x -= 1
                self.snapDisplayToGrid()
        if (self.direction == "RIGHT"): 
            self.display_x += PACMAN_SPEED
            if(self.display_x / TILE_SIZE > self.x and self.display_x % TILE_SIZE == HORIZONTAL_OFFSET):   
                self.x += 1  
                self.snapDisplayToGrid()

        if (self.display_x < SCREEN_OFFSET + self.radius): 
            self.display_x = SCREEN_WIDTH - SCREEN_OFFSET
            self.x = MAP_WIDTH
        if (self.display_x > SCREEN_WIDTH):  
            self.display_x = SCREEN_OFFSET + SCREEN_OFFSET
            self.x = 2
    
    def render(self, screen):

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

        direction_mapping = {
            "UP": 0,
            "DOWN": 1,
            "LEFT": 2,
            "RIGHT": 3,
            "NONE" : 1
        }

        if(self.frame_counter == 0): #draw 2nd frame
            screen.blit(frames[direction_mapping[self.direction]][0], (self.display_x - PACMAN_RADIUS, self.display_y - PACMAN_RADIUS))
            if(self.checkObstructionDirection(tilemap.tilemap, self.direction) == False):   self.frame_counter = 1
            return
        if(self.frame_counter == 1):
            screen.blit(frames[direction_mapping[self.direction]][1], (self.display_x - PACMAN_RADIUS, self.display_y - PACMAN_RADIUS))
            if(self.checkObstructionDirection(tilemap.tilemap, self.direction) == False):   self.frame_counter = 2
            return
        if(self.frame_counter == 2):
            screen.blit(frames[direction_mapping[self.direction]][2], (self.display_x - PACMAN_RADIUS, self.display_y - PACMAN_RADIUS))
            if(self.checkObstructionDirection(tilemap.tilemap, self.direction) == False):   self.frame_counter = 0
            return

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

            if (event.key == pygame.constants.K_UP and pacman.moveInDirection(tilemap.tilemap, "UP")):
                    pacman.direction = "UP"
            if (event.key == pygame.constants.K_DOWN and pacman.moveInDirection(tilemap.tilemap, "DOWN")):
                    pacman.direction = "DOWN"
            if (event.key == pygame.constants.K_LEFT and pacman.moveInDirection(tilemap.tilemap, "LEFT")):
                    pacman.direction = "LEFT"
            if (event.key == pygame.constants.K_RIGHT and pacman.moveInDirection(tilemap.tilemap, "RIGHT")):
                    pacman.direction = "RIGHT"

    # update
    pacman.update(tilemap.tilemap)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    tilemap.render(screen)
    pacman.render(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    FPS = 60
    clock.tick(FPS) 

pygame.quit()
