if __name__ == '__main__':
    print("This is a module, it should not be run standalone!")
    exit()

import pygame
import random
import time
import tracemalloc

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

# Used for coloring text
class ANSI():
    def background(code):
        return "\33[{code}m".format(code=code)
 
    def style_text(code):
        return "\33[{code}m".format(code=code)
 
    def color_text(code):
        return "\33[{code}m".format(code=code)

# load common ghost frames
scared = pygame.image.load("Resource\\ghosts\\scared.png")
scared2 = pygame.image.load("Resource\\ghosts\\scared2.png")
deadUP = pygame.image.load("Resource\\ghosts\\deadUp.png")
deadDOWN = pygame.image.load("Resource\\ghosts\\deadDown.png")
deadLEFT = pygame.image.load("Resource\\ghosts\\deadLeft.png")
deadRIGHT = pygame.image.load("Resource\\ghosts\\deadRight.png")
extra_frames = [scared, scared2, deadUP, deadDOWN, deadLEFT, deadRIGHT]

def loadGhostFrames(name):
    ghost_frames = [None for _ in range(10)]

    for i in range(4):
        ghost_frames[i] = pygame.image.load("Resource\\ghosts\\" + name + "\\" + ["down", "up", "left", "right"][i] + ".png")
    for i in range(6):
        ghost_frames[i + 4] = extra_frames[i]

    for i in range(10):
        ghost_frames[i] = pygame.transform.scale(ghost_frames[i], (int(GHOST_RADIUS * SCALING_FACTOR * 2), int(GHOST_RADIUS * SCALING_FACTOR * 2)))

    return ghost_frames

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
        self.cooldown_timer = 0
        self.collision_count = 0

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

    import random

    def preventGhostOverlap(self, ghost_list):
        COLLISION_RADIUS = self.radius * 1.5
        if(self.cooldown_timer > 0):
            self.cooldown_timer -= 1
            return

        collision_detected = False

        for i in range(len(ghost_list)):
            if (self == ghost_list[i]): continue
            if (self.state == "DEAD" or ghost_list[i].state == "DEAD"): continue

            if (abs(self.display_x - ghost_list[i].display_x) < COLLISION_RADIUS and 
                abs(self.display_y - ghost_list[i].display_y) < COLLISION_RADIUS):
                self.direction = opposite_direction[self.direction]
                self.collision_count += 1
                self.snapDisplayToGrid()
                self.cooldown_timer = 5
                collision_detected = True

        if (not collision_detected):
            self.collision_count = 0
            
        if (self.collision_count > 5): # if 2 ghosts are stuck inside each other, teleport it to the ghost house
            self.x = random.choice([13, 15, 17])
            self.y = 19
            self.collision_count = 0
            self.snapDisplayToGrid()

    
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

    def update(self, tile_map, pacman, ghost_list, enable_test):
        if (self.state == "FROZEN"):
            return
        
        if(not enable_test): self.preventGhostOverlap(ghost_list)

        if (self.canTurn(tile_map) == True and self.lock_turn_time == 0):
            self.direction = self.getDirection(tile_map, pacman, ghost_list)
            if(self.state != "CHASE"): self.lock_turn_time = 2
            else:   self.lock_turn_time = 1

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


class BFSGhost(Ghost): 
    def __init__(self, starting_position, direction, name):
        super().__init__(starting_position, direction, name)
    
    def getDirection(self, tile_map, pacman, ghost_list):  
        target = (0, 0)

        if (self.state == "SCATTER" or self.state == "SCARED"):
            return super().getRandomDirection(tile_map)
        elif (self.state == "DEAD"):
            target = (19, 15) # return to ghost house
        else:
            target = (pacman.y, pacman.x)

        time_start = time.time()
        tracemalloc.start()

        # expanded nodes = nodes being used to generate successor nodes
        expanded = set()
        path = Pfinder.bfs(tile_map, (self.y, self.x), target, expanded)

        _, memory_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        time_end = time.time()

        # Blue
        Coloring = ANSI.background(0) + ANSI.color_text(91) + ANSI.style_text(34)

        print(Coloring + "\n================= BFS =================")
        print(Coloring + f"Start = {(self.y, self.x)}")
        print(Coloring + f"Goal  = {target}")
        print(Coloring + f"Time usage:        {(time_end - time_start) * 1000:.2f} ms")
        print(Coloring + f"Peak memory usage: {memory_peak} bytes")
        print(Coloring + f"Expanded nodes:    {len(expanded)}")

        if (path is None or len(path) <= 1):
            # keep moving foward if no path was found
            return self.direction
        
        direction = Pfinder.identifyDirection(path)
        return direction


class IDSGhost(Ghost):
    def __init__(self, starting_position, direction, name):
        super().__init__(starting_position, direction, name)
    
    # override with specific behavior
    def getDirection(self, tile_map, pacman, ghost_list):  
        target = (0, 0)

        if ((self.y, self.x) in Pfinder.HOUSE or self.state == "SCATTER" or self.state == "SCARED"):
            return super().getRandomDirection(tile_map)
        elif (self.state == "DEAD"):
            target = (19, 15) # return to ghost house
        else:
            target = (pacman.y, pacman.x)

        time_start = time.time()
        tracemalloc.start()

        # expanded is used for analysis
        # expanded nodes = nodes being used to generate successor nodes
        expanded = set()
        path = Pfinder.ids(tile_map, (self.y, self.x), target, expanded, ghost_list)  

        _, memory_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        time_end = time.time()

        # Pink
        Coloring = ANSI.background(0) + ANSI.color_text(91) + ANSI.style_text(35)

        print(Coloring + "\n================= IDS =================")
        print(Coloring + f"Start = {(self.y, self.x)}")
        print(Coloring + f"Goal  = {target}")
        print(Coloring + f"Time usage:        {(time_end - time_start) * 1000:.2f} ms")
        print(Coloring + f"Peak memory usage: {memory_peak} bytes")
        print(Coloring + f"Expanded nodes:    {len(expanded)}")

        if (path is None or len(path) <= 1):
            # keep moving foward if no path was found
            return self.direction
        
        direction = Pfinder.identifyDirection(path)
        return direction
    

class UCSGhost(Ghost):
    def __init__(self, starting_position, direction, name):
        super().__init__(starting_position, direction, name)
    
    def getDirection(self, tile_map, pacman, ghost_list):  
        target = (0, 0)

        if (self.state == "SCATTER" or self.state == "SCARED"):
            return super().getRandomDirection(tile_map)
        elif (self.state == "DEAD"):
            target = (19, 15) # return to ghost house
        else:
            target = (pacman.y, pacman.x)

        time_start = time.time()
        tracemalloc.start()

        # expanded is used for analysis
        expanded = set()
        path = Pfinder.ucs(tile_map, (self.y, self.x), target, expanded, ghost_list) 

        _, memory_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        time_end = time.time()

        # Orange
        print("\033[93m", "\n================= UCS =================", "\033[m")
        print("\033[93m", f"Start = {(self.y, self.x, "\033[m")}", "\033[m")
        print("\033[93m", f"Goal  = {target}", "\033[m")
        print("\033[93m", f"Time usage:        {(time_end - time_start) * 1000:.5f} ms", "\033[m")
        print("\033[93m", f"Peak memory usage: {memory_peak} bytes", "\033[m")
        print("\033[93m", f"Expanded nodes:    {len(expanded)}", "\033[m")

        if (path is None or len(path) <= 1):
            # keep moving foward if no path was found
            return self.direction
        
        direction = Pfinder.identifyDirection(path)
        return direction


class AStarGhost(Ghost):
    def __init__(self, starting_position, direction, name):
        super().__init__(starting_position, direction, name)

    def getDirection(self, tile_map, pacman, ghost_list): 
        target = (0, 0)
        if (self.state == "SCATTER" or self.state == "SCARED"):
            self.path_found = []
            return super().getRandomDirection(tile_map)
        elif (self.state == "DEAD"):
            target = (19, 15) # return to ghost house
        else:
            target = (pacman.y, pacman.x)

        time_start = time.time()
        tracemalloc.start()

        # expanded nodes = nodes being used to generate successor nodes
        expanded = set()
        path = Pfinder.aStar(tile_map, (self.y, self.x), target, expanded, ghost_list) 

        _, memory_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        time_end = time.time()

        # Red
        Coloring = ANSI.background(0) + ANSI.color_text(91) + ANSI.style_text(31)

        print(Coloring + "\n================= A* =================")
        print(Coloring + f"Start = {(self.y, self.x)}")
        print(Coloring + f"Goal  = {target}")
        print(Coloring + f"Time usage:        {(time_end - time_start) * 1000:.2f} ms")
        print(Coloring + f"Peak memory usage: {memory_peak} bytes")
        print(Coloring + f"Expanded nodes:    {len(expanded)}")

        if (path is None or len(path) <= 1):
            # keep moving foward if no path was found
            return self.direction
        
        direction = Pfinder.identifyDirection(path)
        return direction
