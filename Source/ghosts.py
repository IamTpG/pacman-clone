if __name__ == '__main__':
    print("This is a module, it should not be run standalone!")
    exit()

import pygame
import random
import queue

# local
import tile_map as TMap
import pathfinders as Pfinder  

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

SCALING_FACTOR = 1.2

opposite_direction = {
    "UP": "DOWN",
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT"
}

def loadGhostFrames(name):
    blinky_DOWN     = pygame.image.load("Resource\\ghosts\\" + name + "\\down.png")
    blinky_UP       = pygame.image.load("Resource\\ghosts\\" + name + "\\up.png")
    blinky_LEFT     = pygame.image.load("Resource\\ghosts\\" + name + "\\left.png")
    blinky_RIGHT    = pygame.image.load("Resource\\ghosts\\" + name + "\\right.png")

    inky_DOWN       = pygame.image.load("Resource\\ghosts\\" + name + "\\down.png")
    inky_UP         = pygame.image.load("Resource\\ghosts\\" + name + "\\up.png")
    inky_LEFT       = pygame.image.load("Resource\\ghosts\\" + name + "\\left.png")
    inky_RIGHT      = pygame.image.load("Resource\\ghosts\\" + name + "\\right.png")

    clyde_DOWN      = pygame.image.load("Resource\\ghosts\\" + name + "\\down.png")
    clyde_UP        = pygame.image.load("Resource\\ghosts\\" + name + "\\up.png")
    clyde_LEFT      = pygame.image.load("Resource\\ghosts\\" + name + "\\left.png")
    clyde_RIGHT     = pygame.image.load("Resource\\ghosts\\" + name + "\\right.png")

    pinky_DOWN  = pygame.image.load("Resource\\ghosts\\" + name + "\\down.png")
    pinky_UP    = pygame.image.load("Resource\\ghosts\\" + name + "\\up.png")
    pinky_LEFT  = pygame.image.load("Resource\\ghosts\\" + name + "\\left.png")
    pinky_RIGHT = pygame.image.load("Resource\\ghosts\\" + name + "\\right.png")

    feared      = pygame.image.load("Resource\\ghosts\\scared.png")
    feared2     = pygame.image.load("Resource\\ghosts\\scared2.png")
    deadUP      = pygame.image.load("Resource\\ghosts\\deadUp.png")
    deadDOWN    = pygame.image.load("Resource\\ghosts\\deadDown.png")
    deadLEFT    = pygame.image.load("Resource\\ghosts\\deadLeft.png")
    deadRIGHT   = pygame.image.load("Resource\\ghosts\\deadRight.png")

    blinky_frames   = [blinky_DOWN, blinky_UP, blinky_LEFT, blinky_RIGHT, feared, feared2, deadDOWN, deadUP, deadLEFT, deadRIGHT]
    inky_frames     = [inky_DOWN,   inky_UP,   inky_LEFT,   inky_RIGHT,   feared, feared2, deadDOWN, deadUP, deadLEFT, deadRIGHT]
    clyde_frames    = [clyde_DOWN,  clyde_UP,  clyde_LEFT,  clyde_RIGHT,  feared, feared2, deadDOWN, deadUP, deadLEFT, deadRIGHT]
    pinky_frames    = [pinky_DOWN,  pinky_UP,  pinky_LEFT,  pinky_RIGHT,  feared, feared2, deadDOWN, deadUP, deadLEFT, deadRIGHT]

    for i in range(6):
        blinky_frames[i]    = pygame.transform.scale(blinky_frames[i], (GHOST_RADIUS * SCALING_FACTOR * 2, GHOST_RADIUS * SCALING_FACTOR * 2))
        inky_frames[i]      = pygame.transform.scale(inky_frames[i], (GHOST_RADIUS * SCALING_FACTOR * 2, GHOST_RADIUS * SCALING_FACTOR * 2))
        clyde_frames[i]     = pygame.transform.scale(clyde_frames[i], (GHOST_RADIUS * SCALING_FACTOR * 2, GHOST_RADIUS * SCALING_FACTOR * 2))
        pinky_frames[i]     = pygame.transform.scale(pinky_frames[i], (GHOST_RADIUS * SCALING_FACTOR * 2, GHOST_RADIUS * SCALING_FACTOR * 2))

    ghost_frames = {
        "blinky":   blinky_frames,
        "inky":     inky_frames,
        "clyde":    clyde_frames,
        "pinky":    pinky_frames
    }

    return ghost_frames[name]


class Ghost:
    def __init__(self, starting_position, direction, name):
        # private parent class
        if (type(self) == Ghost):
            raise Exception("Ghost is an abstract class and cannot be instantiated directly!")

        # animation
        self.name   = name
        self.frames = loadGhostFrames(name)

        # ghost states
        self.all_possible_states = ["NONE", "SCARED", "DEAD", "SCATTER", "CHASE"]
        self.state = "SCATTER" # default starting state
        
        self.MAX_SCARED_TIME  = 400
        self.MAX_SCATTER_TIME = 400
        self.MAX_CHASE_TIME   = 800

        self.scatter_time = self.MAX_SCATTER_TIME
        self.scared_time  = 0
        self.chase_time   = 0

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
        # abstract method
        raise NotImplementedError("Subclass must implement abstract method")

    def getRandomDirection(self, tile_map):  
        possible_turns = {
            "UP":    ["LEFT", "RIGHT", "UP"],
            "DOWN":  ["LEFT", "RIGHT", "DOWN"],
            "LEFT":  ["UP",   "DOWN",  "LEFT"],
            "RIGHT": ["UP",   "DOWN",  "RIGHT"]
        }

        # Filter out invalid turns
        valid_turns = [direction for direction in possible_turns[self.direction] if not self.checkObstructionDirection(tile_map, direction)]

        # Return a random valid turn, if no valid turn exist, keep moving straight
        return random.choice(valid_turns) if valid_turns else self.direction

    def checkObstructionDirection(self, tile_map, direction):
        if (direction == "NONE"): return False

        OFFSET = 1
        direction_mapping = {
            "UP":    (0, -OFFSET),
            "DOWN":  (0, OFFSET),
            "LEFT":  (-OFFSET, 0),
            "RIGHT": (OFFSET, 0)
        }

        dx, dy = direction_mapping[direction]
        if (tile_map[self.y + dy][self.x + dx] > -1):
            return True
        return False

    def canTurn(self, tile_map):
        if (self.direction == "NONE"):
            return False

        allowed_turns = {
            "LEFT": ["UP", "DOWN"],
            "RIGHT": ["UP", "DOWN"],
            "UP": ["LEFT", "RIGHT"],
            "DOWN": ["LEFT", "RIGHT"]
        }

        return any(not self.checkObstructionDirection(tile_map, direction) for direction in allowed_turns[self.direction])

    def update(self, tile_map, pacman, ghost_list):
        if (self.state == "FROZEN"):
            return

        if (self.canTurn(tile_map) == True and self.lock_turn_time == 0):
            self.direction = self.getDirection(tile_map, pacman, ghost_list)
            self.lock_turn_time = 2

        if (self.checkObstructionDirection(tile_map, self.direction)):
            self.snapDisplayToGrid()
            self.direction = self.getDirection(tile_map, pacman, ghost_list)
        
        update_direction = {
            "UP":    (0, -self.speed, 0, -1),
            "DOWN":  (0, self.speed, 0, 1),
            "LEFT":  (-self.speed, 0, -1, 0),
            "RIGHT": (self.speed, 0, 1, 0),
        }

        # ghosts move slower when they are in the tunnel
        if (self.state != "SCARED" and self.state != "DEAD"):
            if (self.y == 19 and self.x == 5 and self.direction == "LEFT" and self.speed == 2) or (self.y == 19 and self.x == 24 and self.direction == "RIGHT" and self.speed == 2):
                self.speed = GHOST_SPEED // 2
            
            if (self.y == 19 and self.x == 5 and self.direction == "RIGHT" and self.speed == 1) or (self.y == 19 and self.x == 24 and self.direction == "LEFT" and self.speed == 1):
                self.speed = GHOST_SPEED
                # some weird freaky shit happens when they leave the tunnel leaving self.display_x an odd number even though i called the snap to grid function,
                # making it impossible for them to snap to grid, so this just adjusts for that
                if (self.direction == "RIGHT"): self.display_x += 1
                if (self.direction == "LEFT"):  self.display_x -= 1
            
        VERTICAL_OFFSET = 3
        HORIZONTAL_OFFSET = 2

        if (self.direction in update_direction):
            self.display_x += update_direction[self.direction][0]
            self.display_y += update_direction[self.direction][1]
            
            if (self.direction == "UP" or self.direction == "DOWN"):
                if (self.display_y % TILE_SIZE == VERTICAL_OFFSET):
                    self.x += update_direction[self.direction][2]
                    self.y += update_direction[self.direction][3]
                    if self.lock_turn_time > 0: self.lock_turn_time -= 1

            if (self.direction == "LEFT" or self.direction == "RIGHT"):
                if (self.display_x % TILE_SIZE == HORIZONTAL_OFFSET):
                    self.x += update_direction[self.direction][2]
                    self.y += update_direction[self.direction][3]
                    if self.lock_turn_time > 0: self.lock_turn_time -= 1

        if self.scatter_time > 0: self.scatter_time -= 1
        if self.scared_time > 0: self.scared_time -= 1
        if self.chase_time > 0: self.chase_time -= 1

        # screen wrapping
        if (self.display_x < SCREEN_OFFSET + self.radius and self.direction == "LEFT"): 
            self.display_x = SCREEN_WIDTH
            self.x = MAP_WIDTH
            self.snapDisplayToGrid()
        if (self.display_x > SCREEN_WIDTH and self.direction == "RIGHT"):  
            self.display_x = SCREEN_OFFSET
            self.x = 0
            self.snapDisplayToGrid()

        # change ghost states
        if (self.scatter_time == 0 and self.state == "SCATTER"):
            self.state = "CHASE"
            self.chase_time = self.MAX_CHASE_TIME

        if (self.scared_time == 0 and self.state == "SCARED"):
            self.state = "SCATTER"
            self.scatter_time = int(self.MAX_SCATTER_TIME / 2)
            self.direction = opposite_direction[self.direction]
            self.snapDisplayToGrid()
            self.speed = GHOST_SPEED

        if (self.chase_time == 0 and self.state == "CHASE"):
            self.state = "SCATTER"
            self.scatter_time = self.MAX_SCATTER_TIME - 250

        if (self.state == "DEAD" and self.x == 15 and self.y == 19):
            self.state = "SCATTER"
            self.scatter_time = self.MAX_SCATTER_TIME

    def render(self, screen):
        direction_mapping = {
            "UP": 1,
            "DOWN": 0,
            "LEFT": 2,
            "RIGHT": 3
        }
 
        if (self.state == "SCARED"): # when scared timer is less than 25% of the max time, blink
            if (self.scared_time % 25 < 15 and self.scared_time < 0.25 * self.MAX_SCARED_TIME):
                screen.blit(self.frames[5], (self.display_x - GHOST_RADIUS, self.display_y - GHOST_RADIUS))
            else:
                screen.blit(self.frames[4], (self.display_x - GHOST_RADIUS, self.display_y - GHOST_RADIUS))
        elif (self.state == "DEAD"): 
            screen.blit(self.frames[direction_mapping[self.direction] + 6], (self.display_x - GHOST_RADIUS, self.display_y - GHOST_RADIUS))
        elif (self.state == "FROZEN"):
            pass # display nothing
        else:
            screen.blit(self.frames[direction_mapping[self.direction]], (self.display_x - GHOST_RADIUS, self.display_y - GHOST_RADIUS))
        
class Blinky(Ghost): # blinky (red) use A_star search
    def __init__(self, starting_position, direction):
        super().__init__(starting_position, direction, "blinky")

    def getDirection(self, tile_map, pacman, ghost_list): 
        target = (0, 0)
        if (self.state == "SCATTER" or self.state == "SCARED"):
            return super().getRandomDirection(tile_map)
        elif (self.state == "DEAD"):
            target = (19, 15) #return to ghost house
        else:
            target = (pacman.y, pacman.x)

        expanded = set()
        path = Pfinder.a_star(tile_map, (self.y, self.x), target,  expanded, ghost_list) 
        if (path is None or len(path) <= 1):
            return self.direction # keep moving forward if no path is found
        
        direction = Pfinder.find_direction(path)

        if (not self.state == "SCARED"):
            return direction
        else: 
            return super().getRandomDirection(tile_map)

class Inky(Ghost): # inky (blue) use BFS search
    def __init__(self, starting_position, direction):
        super().__init__(starting_position, direction, "inky")
    
    def getDirection(self, tile_map, pacman, ghost_list):  
        target = (0, 0)

        if (self.state == "SCATTER" or self.state == "SCARED"):
            return super().getRandomDirection(tile_map)
        elif (self.state == "DEAD"):
            target = (19, 15) #return to ghost house
        else:
            target = (pacman.y, pacman.x)

        expanded = set()
        path = Pfinder.bfs(tile_map, (self.y, self.x), target, expanded, ghost_list) 
        if (path is None or len(path) <= 1):
            direction = (0, 0)
            return self.direction # keep moving forward if no path is found
        
        direction = Pfinder.find_direction(path)
        return direction

class Clyde(Ghost): # clyde (orange) use UCS search
    def __init__(self, starting_position, direction):
        super().__init__(starting_position, direction, "clyde")
    
    def getDirection(self, tile_map, pacman, ghost_list):  
        target = (0, 0)

        if (self.state == "SCATTER" or self.state == "SCARED"):
            return super().getRandomDirection(tile_map)
        elif (self.state == "DEAD"):
            target = (19, 15) #return to ghost house
        else:
            target = (pacman.y, pacman.x)

        expanded = set()
        path = Pfinder.ucs(tile_map, (self.y, self.x), target, expanded, ghost_list) 
        if (path is None or len(path) <= 1):
            return self.direction # keep moving forward if no path is found
        
        direction = Pfinder.find_direction(path)
        return direction
    
class Pinky(Ghost): # pinky (pink) use DFS search
    def __init__(self, starting_position, direction):
        super().__init__(starting_position, direction, "pinky")
    
    #override with specific behavior
    def getDirection(self, tile_map, pacman, ghost_list):  
        target = (0, 0)

        if (self.state == "SCATTER" or self.state == "SCARED"):
            return super().getRandomDirection(tile_map)
        elif (self.state == "DEAD"):
            target = (19, 15) #return to ghost house
        else:
            target = (pacman.y, pacman.x)

        visited = set()
        expanded_list = [(self.y,self.x)] #expanded is a list,  i didnt quite understand the meaning of this list yet - Neidy 
        path = Pfinder.dfs_recursive_ordered(tile_map,(self.y,self.x),visited, target,  expanded_list, ghost_list)   
        if path is None :
            direction = (0,0)
            return self.direction #keep moving in the same direction if no path is found
        direction = (-path[0][0] + path[1][0], -path[0][1] + path[1][1])
        #ghost not able to turn 180 degrees
        if(Pfinder.switch_case(direction) == (opposite_direction[self.direction])):
            if(Pfinder.switch_case(direction) == "UP" or Pfinder.switch_case(direction) == "DOWN"):
                #go left
                expanded_list = [(self.y,self.x-1)]
                path = Pfinder.dfs_recursive_ordered(tile_map,(self.y,self.x - 1),visited, (pacman.y,pacman.x),  expanded_list, ghost_list)
                if path is None:
                    #go right
                    expanded_list = [(self.y,self.x+1)]
                    path = Pfinder.dfs_recursive_ordered(tile_map,(self.y,self.x + 1),visited, (pacman.y,pacman.x),  expanded_list, ghost_list)
                    if path is None:
                        return self.direction
                    return "RIGHT"
                return "LEFT"
            else:
                #go up
                expanded_list = [(self.y-1,self.x)]
                path = Pfinder.dfs_recursive_ordered(tile_map,(self.y - 1,self.x),visited, (pacman.y,pacman.x),  expanded_list, ghost_list)
                if path is None:
                    #go down
                    expanded_list = [(self.y+1,self.x)]
                    path = Pfinder.dfs_recursive_ordered(tile_map,(self.y + 1,self.x),visited, (pacman.y,pacman.x),  expanded_list, ghost_list)
                    if path is None:
                        return self.direction
                    return "DOWN"
                return "UP"
        if(not self.state == "SCARED"):
            print (Pfinder.switch_case(direction))  
            return Pfinder.switch_case(direction) 
        expanded_list = [(self.y, self.x)] # expanded is a list, i didnt quite understand the meaning of this list yet - Neidy 
        path = Pfinder.dfs_recursive_ordered(tile_map, (self.y, self.x), visited, (pacman.y, pacman.x), expanded_list, ghost_list)   
        
        if (path is None or len(path) <= 1):
            return self.direction # keep moving forward if no path is found

        direction = Pfinder.find_direction(path)
        return direction
            