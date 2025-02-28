import pygame
import random

# local
import tile_map as TMap

if __name__ == '__main__':
    print("This is a module, it should not be run standalone!")

# map constants
TILE_RESU = TMap.TILE_RESU
TILE_SIZE = TMap.TILE_SIZE

MAP_WIDTH = TMap.MAP_WIDTH
MAP_HEIGHT = TMap.MAP_HEIGHT

SCREEN_OFFSET = TMap.SCREEN_OFFSET
SCREEN_WIDTH = TMap.SCREEN_WIDTH
SCREEN_HEIGHT = TMap.SCREEN_HEIGHT

GHOST_RADIUS = TMap.GHOST_RADIUS
GHOST_SPEED = TMap.GHOST_SPEED

def loadGhostFrames(name):
    blinky = pygame.image.load("Resource/ghosts/blinky.png")
    inky = pygame.image.load("Resource/ghosts/inky.png")
    pinky = pygame.image.load("Resource/ghosts/pinky.png")
    clyde = pygame.image.load("Resource/ghosts/clyde.png")
    blue_ghost = pygame.image.load("Resource/ghosts/blue_ghost.png")

    ghost_frames = {
        "blinky": [blinky, blue_ghost],
        "inky": [inky, blue_ghost],
        "pinky": [pinky, blue_ghost],
        "clyde": [clyde, blue_ghost]
    }

    SCALING_FACTOR = 2

    for i in range(2):
        ghost_frames[name][i] = pygame.transform.scale(ghost_frames[name][i], (GHOST_RADIUS * SCALING_FACTOR, GHOST_RADIUS * SCALING_FACTOR))

    return ghost_frames[name]

class Ghost:
    def __init__(self, starting_position, direction, name):
        # animation
        self.frames = loadGhostFrames(name)

        # ghost states
        self.scatter_state = False
        self.scatter_time = 50

        self.feared_state = False
        self.MAX_FEARED_TIME = 300
        self.feared_time = 0

        # lock turning
        self.lock_turn_time = 0

        # movement
        self.direction = direction
        self.speed = GHOST_SPEED
        self.x = starting_position[0]
        self.y = starting_position[1]

        # display
        self.radius = GHOST_RADIUS
        self.display_x = self.x * TILE_SIZE + SCREEN_OFFSET - self.radius + 3
        self.display_y = self.y * TILE_SIZE + SCREEN_OFFSET - self.radius + 4 
    
    def snapDisplayToGrid(self):
        self.display_x = self.x * TILE_SIZE + SCREEN_OFFSET - self.radius + 3
        self.display_y = self.y * TILE_SIZE + SCREEN_OFFSET - self.radius + 4

    def reset(self, starting_position, direction):
        self.x = starting_position[0]
        self.y = starting_position[1]
        self.direction = direction
        self.speed = GHOST_SPEED
        self.snapDisplayToGrid()

    def getDirection(self, tile_map):
        possible_turns = {
            "UP": ["LEFT", "RIGHT", "UP"],
            "DOWN": ["LEFT", "RIGHT", "DOWN"],
            "LEFT": ["UP", "DOWN", "LEFT"],
            "RIGHT": ["UP", "DOWN", "RIGHT"]
        }

        # Filter out invalid turns
        valid_turns = [direction for direction in possible_turns[self.direction] if not self.checkObstructionDirection(tile_map, direction)]
    
        # Return a random valid turn, if no valid turn exist, keep moving straight
        return random.choice(valid_turns) if valid_turns else self.direction

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

    #wip
    def preventCollisionWithOtherGhosts(self, ghost):
        '''
        opposite_direction = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }

        direction_mapping = {
            "UP": (0, 1),
            "DOWN": (0, -1),
            "LEFT": (1, 0),
            "RIGHT": (-1, 0)
        }

        if self.x == ghost.x and self.y == ghost.y:
            self.direction = opposite_direction[self.direction]
            self.x = self.x + direction_mapping[opposite_direction[self.direction]][0]
            self.y = self.y + direction_mapping[opposite_direction[self.direction]][1]
            ghost.x = ghost.x + direction_mapping[opposite_direction[ghost.direction]][0]
            ghost.y = ghost.y + direction_mapping[opposite_direction[ghost.direction]][1]
            self.snapDisplayToGrid()
        '''

    def canTurn(self, tile_map):
        allowed_turns = {
            "LEFT": ["UP", "DOWN"],
            "RIGHT": ["UP", "DOWN"],
            "UP": ["LEFT", "RIGHT"],
            "DOWN": ["LEFT", "RIGHT"]
        }

        return any(not self.checkObstructionDirection(tile_map, direction) for direction in allowed_turns[self.direction])

    def update(self, tile_map):
        if(self.canTurn(tile_map) == True and self.lock_turn_time == 0):
            self.direction = self.getDirection(tile_map)
            self.lock_turn_time = 5

        if (self.checkObstructionDirection(tile_map, self.direction)):
            self.snapDisplayToGrid()
            self.direction = self.getDirection(tile_map)
        
        VERTICAL_OFFSET = 3
        HORIZONTAL_OFFSET = 2
        
        if (self.direction == "UP"):
            self.display_y -= self.speed
            if(self.display_y / TILE_SIZE < self.y and self.display_y % TILE_SIZE == VERTICAL_OFFSET):   
                self.y -= 1
                if(self.lock_turn_time > 0): self.lock_turn_time -= 1
        if (self.direction == "DOWN"):  
            self.display_y += self.speed
            if(self.display_y / TILE_SIZE > self.y and self.display_y % TILE_SIZE == VERTICAL_OFFSET):
                self.y += 1
                if(self.lock_turn_time > 0): self.lock_turn_time -= 1
        if (self.direction == "LEFT"):  
            self.display_x -= self.speed
            if(self.display_x / TILE_SIZE < self.x and self.display_x % TILE_SIZE == HORIZONTAL_OFFSET):
                self.x -= 1
                if(self.lock_turn_time > 0): self.lock_turn_time -= 1
        if (self.direction == "RIGHT"): 
            self.display_x += self.speed
            if(self.display_x / TILE_SIZE > self.x and self.display_x % TILE_SIZE == HORIZONTAL_OFFSET):
                self.x += 1
                if(self.lock_turn_time > 0): self.lock_turn_time -= 1

        if (self.display_x < SCREEN_OFFSET + self.radius and self.direction == "LEFT"): 
            self.display_x = SCREEN_WIDTH
            self.x = MAP_WIDTH
        if (self.display_x > SCREEN_WIDTH and self.direction == "RIGHT"):  
            self.display_x = SCREEN_OFFSET
            self.x = 0

        if(self.feared_state == True):
            self.feared_time -= 1
            self.speed = 1
            if(self.feared_time == 0):
                self.feared_state = False
                self.snapDisplayToGrid()
                self.speed = 2
    
    def render(self, screen):
        if(self.feared_state == True):
            screen.blit(self.frames[1], (self.display_x - GHOST_RADIUS, self.display_y - GHOST_RADIUS))
        else:
            screen.blit(self.frames[0], (self.display_x - GHOST_RADIUS, self.display_y - GHOST_RADIUS))
