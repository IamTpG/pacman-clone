import pygame
import random
import queue

# local
import tile_map as TMap
import pathfinders as Pfinder  


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

SCALING_FACTOR = 1.1

def loadGhostFrames(name):
    blinky_DOWN = pygame.image.load("Resource\\ghosts\\" + name + "\\down.png")
    blinky_UP = pygame.image.load("Resource\\ghosts\\" + name + "\\up.png")
    blinky_LEFT = pygame.image.load("Resource\\ghosts\\" + name + "\\left.png")
    blinky_RIGHT = pygame.image.load("Resource\\ghosts\\" + name + "\\right.png")

    inky_DOWN = pygame.image.load("Resource\\ghosts\\" + name + "\\down.png")
    inky_UP = pygame.image.load("Resource\\ghosts\\" + name + "\\up.png")
    inky_LEFT = pygame.image.load("Resource\\ghosts\\" + name + "\\left.png")
    inky_RIGHT = pygame.image.load("Resource\\ghosts\\" + name + "\\right.png")

    clyde_DOWN = pygame.image.load("Resource\\ghosts\\" + name + "\\down.png")
    clyde_UP = pygame.image.load("Resource\\ghosts\\" + name + "\\up.png")
    clyde_LEFT = pygame.image.load("Resource\\ghosts\\" + name + "\\left.png")
    clyde_RIGHT = pygame.image.load("Resource\\ghosts\\" + name + "\\right.png")

    pinky_DOWN = pygame.image.load("Resource\\ghosts\\" + name + "\\down.png")
    pinky_UP = pygame.image.load("Resource\\ghosts\\" + name + "\\up.png")
    pinky_LEFT = pygame.image.load("Resource\\ghosts\\" + name + "\\left.png")
    pinky_RIGHT = pygame.image.load("Resource\\ghosts\\" + name + "\\right.png")

    feared = pygame.image.load("Resource\\ghosts\\feared.png")
    dead = pygame.image.load("Resource\\ghosts\\dead.png")

    blinky_frames = [blinky_DOWN, blinky_UP, blinky_LEFT, blinky_RIGHT, feared, dead]
    inky_frames = [inky_DOWN, inky_UP, inky_LEFT, inky_RIGHT, feared, dead]
    clyde_frames = [clyde_DOWN, clyde_UP, clyde_LEFT, clyde_RIGHT, feared, dead]
    pinky_frames = [pinky_DOWN, pinky_UP, pinky_LEFT, pinky_RIGHT, feared, dead]

    for i in range(6):
        blinky_frames[i] = pygame.transform.scale(blinky_frames[i], (GHOST_RADIUS * SCALING_FACTOR * 2, GHOST_RADIUS * SCALING_FACTOR * 2))
        inky_frames[i] = pygame.transform.scale(inky_frames[i], (GHOST_RADIUS * SCALING_FACTOR * 2, GHOST_RADIUS * SCALING_FACTOR * 2))
        clyde_frames[i] = pygame.transform.scale(clyde_frames[i], (GHOST_RADIUS * SCALING_FACTOR * 2, GHOST_RADIUS * SCALING_FACTOR * 2))
        pinky_frames[i] = pygame.transform.scale(pinky_frames[i], (GHOST_RADIUS * SCALING_FACTOR * 2, GHOST_RADIUS * SCALING_FACTOR * 2))
            
    ghost_frames = {
        "blinky": blinky_frames,
        "inky": inky_frames,
        "clyde": clyde_frames,
        "pinky": pinky_frames
    }

    return ghost_frames[name]

class Ghost:
    def __init__(self, starting_position, direction, name):
        # private parent class
        if(type(self) == Ghost):
            raise Exception("Ghost is an abstract class and cannot be instantiated directly!")

        # animation
        self.name = name
        self.frames = loadGhostFrames(name)

        # ghost states
        self.scatter_state = False
        self.scatter_time = 50

        self.feared_state = False
        self.MAX_FEARED_TIME = 300
        self.feared_time = 0

        self.freeze_state = False
        self.dead = False

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

    def freeze(self):
        self.speed = 0

    def unfreeze(self): 
        self.speed = GHOST_SPEED
        self.snapDisplayToGrid()

    def resetPosition(self, starting_position, direction):
        self.x = starting_position[0]
        self.y = starting_position[1]
        self.direction = direction
        self.speed = GHOST_SPEED
        self.snapDisplayToGrid()
    def switch_case(direction):
        
        switcher = {
            (0, -1): "LEFT",
            (0, 1): "RIGHT",
            (-1, 0): "UP",
            (1, 0) : "DOWN"
        }
        return switcher.get(direction, "Invalid")  # Default case 
    
    def getDirection(tile_map,pacman,other_ghost): 
        expanded = set()
        path = Pfinder.a_star(tile_map,self, pacman,  expanded)  
        direction = (-path[0][0] + path[1][0], -path[0][1] + path[1][1])
       
        return switch_case(direction) #1/ tai sao switch case o tren ma bao undefined ?
    
    

    def getDirection2(self, tile_map, pacman, ghost_list):  
        
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

    def canTurn(self, tile_map):
        if(self.direction == "NONE"):
            return False

        allowed_turns = {
            "LEFT": ["UP", "DOWN"],
            "RIGHT": ["UP", "DOWN"],
            "UP": ["LEFT", "RIGHT"],
            "DOWN": ["LEFT", "RIGHT"]
        }

        return any(not self.checkObstructionDirection(tile_map, direction) for direction in allowed_turns[self.direction])

    def update(self, tile_map, pacman, ghost_list):
        if(self.freeze_state == True):
            return

        if(self.canTurn(tile_map) == True and self.lock_turn_time == 0):
            self.direction = self.getDirection(tile_map, pacman, ghost_list)
            self.lock_turn_time = 5

        if (self.checkObstructionDirection(tile_map, self.direction)):
            self.snapDisplayToGrid()
            self.direction = self.getDirection(tile_map, pacman, ghost_list)
        
        VERTICAL_OFFSET = 3
        HORIZONTAL_OFFSET = 2
        
        update_direction = {
            "UP": (0, -self.speed, 0, -1),
            "DOWN": (0, self.speed, 0, 1),
            "LEFT": (-self.speed, 0, -1, 0),
            "RIGHT": (self.speed, 0, 1, 0)  
        }

        if (self.direction in update_direction):
            self.display_x += update_direction[self.direction][0]
            self.display_y += update_direction[self.direction][1]
            
            if(self.direction == "UP" or self.direction == "DOWN"):
                if(self.display_y % TILE_SIZE == VERTICAL_OFFSET):
                    self.x += update_direction[self.direction][2]
                    self.y += update_direction[self.direction][3]
                    if self.lock_turn_time > 0: self.lock_turn_time -= 1
            if(self.direction == "LEFT" or self.direction == "RIGHT"):
                if(self.display_x % TILE_SIZE == HORIZONTAL_OFFSET):
                    self.x += update_direction[self.direction][2]
                    self.y += update_direction[self.direction][3]
                    if self.lock_turn_time > 0: self.lock_turn_time -= 1

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
        direction_mapping = {
            "UP": 1,
            "DOWN": 0,
            "LEFT": 2,
            "RIGHT": 3
        }

        if(self.feared_state == True):
            screen.blit(self.frames[4], (self.display_x - GHOST_RADIUS, self.display_y - GHOST_RADIUS))
        elif(self.dead == True):
            screen.blit(self.frames[5], (self.display_x - GHOST_RADIUS, self.display_y - GHOST_RADIUS))
        else:
            screen.blit(self.frames[direction_mapping[self.direction]], (self.display_x - GHOST_RADIUS, self.display_y - GHOST_RADIUS))
        
class Blinky(Ghost):
    def __init__(self, starting_position, direction):
        super().__init__(starting_position, direction, "blinky")
     
    #override with specific behavior
    def getDirection(self, tile_map, pacman, other_ghosts):  
        return super().getDirection(tile_map, pacman, other_ghosts) #using parent class behavior, remove this when adding specific behavior

class Inky(Ghost):
    def __init__(self, starting_position, direction):
        super().__init__(starting_position, direction, "inky")
    
    #override with specific behavior
    def getDirection(self, tile_map, pacman, other_ghosts):
        return super().getDirection(tile_map, pacman, other_ghosts)

class Clyde(Ghost):
    def __init__(self, starting_position, direction):
        super().__init__(starting_position, direction, "clyde")
    
    #override with specific behavior
    def getDirection(self, tile_map, pacman, other_ghosts):
        return super().getDirection(tile_map, pacman, other_ghosts)
    
class Pinky(Ghost):
    def __init__(self, starting_position, direction):
        super().__init__(starting_position, direction, "pinky")
    
    #override with specific behavior
    def getDirection(self, tile_map, pacman, other_ghosts):
        return super().getDirection(tile_map, pacman, other_ghosts)