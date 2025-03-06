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
    def __init__(self, starting_position, direction, name, starting_state):
        # private parent class
        if(type(self) == Ghost):
            raise Exception("Ghost is an abstract class and cannot be instantiated directly!")

        # animation
        self.name = name
        self.frames = loadGhostFrames(name)

        # ghost states
        self.all_possible_states = ["NONE", "SCARED", "DEAD", "SCATTER", "CHASE"]
        self.state = starting_state[1]
        
        self.MAX_FEARED_TIME = 300
        self.MAX_SCATTER_TIME = starting_state[0]

        self.scatter_time = starting_state[0]
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
    
    def getDirection(self, tile_map, pacman, ghost_list):  
        expanded = set()
        path = Pfinder.a_star(tile_map,(self.y,self.x), (pacman.y,pacman.x),  expanded, ghost_list) 
        if path is 'NONE' :
            direction = (0,0)
            # debug print("No path found")
            return "STAY"
        direction = (-path[0][0] + path[1][0], -path[0][1] + path[1][1])
        return Pfinder.switch_case(direction) #1/ why switched_case undifined ? - Neidy 

    def getRandomDirection(self, tile_map):  
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
        if(self.state == "FROZEN"):
            return

        if(self.canTurn(tile_map) == True and self.lock_turn_time == 0):
            self.direction = self.getDirection(tile_map, pacman, ghost_list)
            self.lock_turn_time = 3

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
                    if self.scatter_time > 0: self.scatter_time -= 1
            if(self.direction == "LEFT" or self.direction == "RIGHT"):
                if(self.display_x % TILE_SIZE == HORIZONTAL_OFFSET):
                    self.x += update_direction[self.direction][2]
                    self.y += update_direction[self.direction][3]
                    if self.lock_turn_time > 0: self.lock_turn_time -= 1
                    if self.scatter_time > 0: self.scatter_time -= 1

        if (self.display_x < SCREEN_OFFSET + self.radius and self.direction == "LEFT"): 
            self.display_x = SCREEN_WIDTH
            self.x = MAP_WIDTH
        if (self.display_x > SCREEN_WIDTH and self.direction == "RIGHT"):  
            self.display_x = SCREEN_OFFSET
            self.x = 0

        if(self.scatter_time == 0 and self.state == "SCATTER"):
            self.state = "CHASE"

        if(self.state == "SCARED"):
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

        if(self.state == "SCARED"):
            screen.blit(self.frames[4], (self.display_x - GHOST_RADIUS, self.display_y - GHOST_RADIUS))
        elif(self.state == "DEAD"):
            screen.blit(self.frames[5], (self.display_x - GHOST_RADIUS, self.display_y - GHOST_RADIUS))
        else:
            screen.blit(self.frames[direction_mapping[self.direction]], (self.display_x - GHOST_RADIUS, self.display_y - GHOST_RADIUS))
        
class Blinky(Ghost): # blinky (red) use A_star search
    def __init__(self, starting_position, direction, starting_scatter_time):
        super().__init__(starting_position, direction, "blinky", starting_scatter_time)

    def getDirection(self, tile_map, pacman, ghost_list):  
        opposite_direction = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }

        if (self.state == "SCATTER" or self.state == "SCARED"):
            return super().getRandomDirection(tile_map)
        else:
            expanded = set()
            path = Pfinder.a_star(tile_map,(self.y,self.x), (pacman.y,pacman.x),  expanded, ghost_list) 
            if path is None : 
                direction = (0,0)
                return self.direction #keep moving in the same direction if no path is found
            direction = (-path[0][0] + path[1][0], -path[0][1] + path[1][1])
            if(not self.state == "SCARED"):
                return Pfinder.switch_case(direction)
            else:
                return opposite_direction[Pfinder.switch_case(direction)]
                #run away from pacman if scared

class Inky(Ghost): # inky (blue) use BFS search
    def __init__(self, starting_position, direction, starting_scatter_time):
        super().__init__(starting_position, direction, "inky", starting_scatter_time)
    
    def getDirection(self, tile_map, pacman, ghost_list):  
        opposite_direction = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }

        if (self.state == "SCATTER" or self.state == "SCARED"):
            return super().getRandomDirection(tile_map)
        else:
            expanded = set()
            path = Pfinder.bfs(tile_map, (self.y,self.x), (pacman.y,pacman.x), expanded, ghost_list) 
            if path is None:
                direction = (0, 0)
                return self.direction # keep moving in the same direction if no path is found
            
            direction = (-path[0][0] + path[1][0], -path[0][1] + path[1][1])

            if (not self.state == "SCARED"):
                return Pfinder.switch_case(direction)
            else:
                #run away from pacman if scared
                return opposite_direction[Pfinder.switch_case(direction)]

class Clyde(Ghost): # clyde (orange) use UCS search
    def __init__(self, starting_position, direction, starting_scatter_time):
        super().__init__(starting_position, direction, "clyde", starting_scatter_time)
    
    def getDirection(self, tile_map, pacman, ghost_list):  
        opposite_direction = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }

        if (self.state == "SCATTER" or self.state == "SCARED"):
            return super().getRandomDirection(tile_map)
        else:
            expanded = set()
            path = Pfinder.ucs(tile_map, (self.y,self.x), (pacman.y,pacman.x), expanded, ghost_list) 
            if path is None:
                direction = (0, 0)
                return self.direction # keep moving in the same direction if no path is found
            
            direction = (-path[0][0] + path[1][0], -path[0][1] + path[1][1])

            if (not self.state == "SCARED"):
                return Pfinder.switch_case(direction)
            else:
                #run away from pacman if scared
                return opposite_direction[Pfinder.switch_case(direction)]
    
class Pinky(Ghost): # pinky (pink) use DFS search
    def __init__(self, starting_position, direction, starting_scatter_time):
        super().__init__(starting_position, direction, "pinky", starting_scatter_time)
    
    #override with specific behavior
    def getDirection(self, tile_map, pacman, ghost_list):  
        opposite_direction = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }

        if(self.state == "SCATTER"):
            return super().getRandomDirection(tile_map)
        else:
            visited = set()
            expanded_list = [(self.y,self.x)] #expanded is a list,  i didnt quite understand the meaning of this list yet - Neidy 
            path = Pfinder.dfs_recursive_ordered(tile_map,(self.y,self.x),visited, (pacman.y,pacman.x),  expanded_list, ghost_list)   
            if path is None :
                direction = (0,0)
                return self.direction #keep moving in the same direction if no path is found
            direction = (-path[0][0] + path[1][0], -path[0][1] + path[1][1])
            if(not self.state == "SCARED"):
                return Pfinder.switch_case(direction) 
            else:
                return opposite_direction[Pfinder.switch_case(direction)]
                #run away from pacman if scared