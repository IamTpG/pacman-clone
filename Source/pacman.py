import pygame

# local
import tile_map as TMap

if __name__ == "__main__":
    print("This is a module, it should not be run standalone!")

# constants
TILE_RESU = TMap.TILE_RESU
TILE_SIZE = TMap.TILE_SIZE

MAP_WIDTH = TMap.MAP_WIDTH
MAP_HEIGHT = TMap.MAP_HEIGHT

SCREEN_OFFSET = TMap.SCREEN_OFFSET
SCREEN_WIDTH = TMap.SCREEN_WIDTH

PACMAN_RADIUS = TMap.PACMAN_RADIUS

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

def loadPacmanSound():
    death_sfx = pygame.mixer.Sound("Resource\\sfx\\pacman_death.wav")
    chomping_sfx = pygame.mixer.Sound("Resource\\sfx\\pacman_chomp.wav")
    eat_fruit_sfx = pygame.mixer.Sound("Resource\\sfx\\pacman_eatfruit.wav")
    eat_ghost_sfx = pygame.mixer.Sound("Resource\\sfx\\pacman_eatghost.wav")

    sounds = [death_sfx, chomping_sfx, eat_fruit_sfx, eat_ghost_sfx]

    VOLUME = 0.5
    for i in range(4):
        sounds[i].set_volume(VOLUME)
        
    return sounds

class Pacman:
    def __init__(self, starting_postion, direction):
        # animation
        self.frames = loadPacmanFrames()
        self.frame_counter = 0 # used to cycle through frames
        self.sound = loadPacmanSound()
        self.sound_index = 0 # used to play sound at intervals

        # used to lock turning for a certain amount of time
        self.lock_turn_time = 0 

        # used to queue turning inputs
        self.queue_turn = "NONE" 
        self.MAX_QUEUE_TIME = 3 
        self.queue_time = self.MAX_QUEUE_TIME

        # stuff
        self.lives = 3
        self.direction = direction
        self.speed = 2 
        self.x = starting_postion[0]
        self.y = starting_postion[1]

        # display
        self.radius = PACMAN_RADIUS
        self.display_x = self.x * TILE_SIZE + SCREEN_OFFSET - self.radius + 3
        self.display_y = self.y * TILE_SIZE + SCREEN_OFFSET - self.radius + 4
    
    def snapDisplayToGrid(self):
        self.display_x = self.x * TILE_SIZE + SCREEN_OFFSET - self.radius + 3
        self.display_y = self.y * TILE_SIZE + SCREEN_OFFSET - self.radius + 4

    def resetPosition(self, starting_position, direction):
        self.x = starting_position[0]
        self.y = starting_position[1]
        self.direction = direction
        self.snapDisplayToGrid()

    def checkObstructionDirection(self, tile_map, direction):
        if(direction == "NONE"): return False

        OFFSET = 1
        direction_mapping = {
            "UP": (0, -OFFSET),
            "DOWN": (0, OFFSET),
            "LEFT": (-OFFSET, 0),
            "RIGHT": (OFFSET, 0)
        }

        dx, dy = direction_mapping[direction]
        if (tile_map[self.y + dy][self.x + dx] != -1):
            return True
        return False

    def checkCollision(self, ghosts : list):
        if any(self.x == ghost.x and self.y == ghost.y for ghost in ghosts):
            self.lives -= 1
            self.sound[1].stop()
            self.sound[0].play()
            return True
        return False

    def canTurn(self, tile_map, wanted_direction):
        if wanted_direction == "NONE" or wanted_direction == self.direction:
            return False

        return not self.checkObstructionDirection(tile_map, wanted_direction)

    def update(self, tile_map):
        DEBUG = True
        if (DEBUG): 
            print("Tile Map Cords: X: " + str(self.x) + " Y: " + str(self.y) + 
                " | Queue Turn: " + self.queue_turn +
                " | Direction: " + self.direction +
                " | Obstruction: " + str(self.checkObstructionDirection(tile_map, self.direction)))
        
        # reset queue turn if time runs out
        if(self.queue_time == 0):
            self.queue_turn = "NONE"
            self.queue_time = self.MAX_QUEUE_TIME

        # turn pacman if possible
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
        
        update_direction = {
            "UP": (0, -self.speed, 0, -1),
            "DOWN": (0, self.speed, 0, 1),
            "LEFT": (-self.speed, 0, -1, 0),
            "RIGHT": (self.speed, 0, 1, 0)  
        }

        # update position
        if (self.direction in update_direction):
            self.display_x += update_direction[self.direction][0]
            self.display_y += update_direction[self.direction][1]
            
            if(self.direction == "UP" or self.direction == "DOWN"):
                if(self.display_y % TILE_SIZE == VERTICAL_OFFSET):
                    self.x += update_direction[self.direction][2]
                    self.y += update_direction[self.direction][3]
                    self.queue_time -= 1
                    if(self.lock_turn_time > 0): self.lock_turn_time -= 1
            if(self.direction == "LEFT" or self.direction == "RIGHT"):
                if(self.display_x % TILE_SIZE == HORIZONTAL_OFFSET):
                    self.x += update_direction[self.direction][2]
                    self.y += update_direction[self.direction][3]
                    self.queue_time -= 1
                    if(self.lock_turn_time > 0): self.lock_turn_time -= 1
            
        # wrap around screen
        if (self.display_x < SCREEN_OFFSET + self.radius and self.direction == "LEFT"): 
            self.display_x = SCREEN_WIDTH
            self.x = MAP_WIDTH
        if (self.display_x > SCREEN_WIDTH and self.direction == "RIGHT"):  
            self.display_x = SCREEN_OFFSET
            self.x = 0
    
    def render(self, screen, tilemap):
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

        SOUND_INTERVAL = 36

        if not self.checkObstructionDirection(tilemap.tilemap, self.direction):
            self.sound_index += 1
            if(self.sound_index == SOUND_INTERVAL):
                self.sound[1].play()
                self.sound_index = 0
