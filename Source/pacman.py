if __name__ == "__main__":
    print("This is a module, it should not be run standalone!")
    exit()

import pygame

# local
import tile_map as TMap 

# constants
TILE_RESU = TMap.TILE_RESU
TILE_SIZE = TMap.TILE_SIZE

MAP_WIDTH = TMap.MAP_WIDTH
MAP_HEIGHT = TMap.MAP_HEIGHT

SCREEN_OFFSET = TMap.SCREEN_OFFSET
SCREEN_WIDTH = TMap.SCREEN_WIDTH

PACMAN_RADIUS = TMap.PACMAN_RADIUS

PACMAN_SPEED = TMap.PACMAN_SPEED
GHOST_SPEED = TMap.GHOST_SPEED
SCALING_FACTOR = 2.3

opposite_direction = {
    "UP": "DOWN",
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT"
}

def loadPacmanDeathFrames():
    frames = [None for _ in range(11)]

    for i in range(11):
        frames[i] = pygame.image.load("Resource\\pacman\\death_animation\\death" + str(i + 1) + ".png")
        frames[i] = pygame.transform.scale(frames[i], (PACMAN_RADIUS * SCALING_FACTOR, PACMAN_RADIUS * SCALING_FACTOR))

    return frames

def loadPacmanMovementFrames():
    frames = [[None for _ in range(3)] for _ in range(4)] 

    for i in range(4):
        for j in range(3):
            frames[i][j] = pygame.image.load("Resource\\pacman\\movement_animation\\" + ["up", "down", "left", "right"][i] + "\\" + str(j + 1) + ".png")
            frames[i][j] = pygame.transform.scale(frames[i][j], (PACMAN_RADIUS * SCALING_FACTOR, PACMAN_RADIUS * SCALING_FACTOR))

    return frames

def loadPacmanSound():
    death_sfx = pygame.mixer.Sound("Resource\\sfx\\pacman_death.wav")
    chomping_sfx = pygame.mixer.Sound("Resource\\sfx\\pacman_chomp.wav")
    eat_fruit_sfx = pygame.mixer.Sound("Resource\\sfx\\pacman_eatfruit.wav")
    eat_ghost_sfx = pygame.mixer.Sound("Resource\\sfx\\pacman_eatghost.wav")
    eat_power_pellet_sfx = pygame.mixer.Sound("Resource\\sfx\\power_up.wav")

    sounds = [death_sfx, chomping_sfx, eat_fruit_sfx, eat_ghost_sfx, eat_power_pellet_sfx]

    VOLUME = 0.5
    for i in range(4):
        sounds[i].set_volume(VOLUME)
        
    return sounds

class Pacman:
    def __init__(self, starting_postion, direction):
        # load frames
        self.movement_frames = loadPacmanMovementFrames()
        self.death_frames = loadPacmanDeathFrames()
        
        # animation
        self.MAX_DEATH_FRAMES_DURATION = 12
        self.death_frames_counter = 0 # used to cycle through death frames

        self.MAX_MOVEMENT_FRAMES_DURATION = 5
        self.movement_frame_counter = 0 # used to cycle through frames
        self.sound = loadPacmanSound()
        self.sound_index = 0 
        self.stopping_counter = 0

        # used to lock turning for a certain amount of time
        self.lock_turn_time = 0 

        # used to queue turning inputs
        self.queue_turn = "NONE" 
        self.MAX_QUEUE_TIME = 3 
        self.queue_time = self.MAX_QUEUE_TIME

        # stuff
        self.invincible = False
        self.dead = False
        self.lives = 3 # default 3
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
        if (tile_map[self.y + dy][self.x + dx] > -1): 
            return True
        return False

    def checkCollision(self, tile_map, ghosts : list, starting_positions : list):
        COLLISION_RADIUS = 8

        for ghost in ghosts:
            if(abs(self.display_x - ghost.display_x) < COLLISION_RADIUS and 
               abs(self.display_y - ghost.display_y) < COLLISION_RADIUS and self.dead == False):
                if(ghost.state == "DEAD"):
                    continue
                elif ghost.state != "SCARED":
                    TMap.pauseScreen(400)
                    self.lives -= 1
                    self.sound[1].stop()
                    self.sound[0].play()
                    self.dead = True
                else:
                    TMap.pauseScreen(200)
                    self.sound[3].play()
                    tile_map.score += 200
                    ghost.state = "DEAD"
                    ghost.speed = TMap.GHOST_SPEED
                    ghost.direction = opposite_direction[ghost.direction]
                    ghost.snapDisplayToGrid()
        
        if self.dead == True and self.death_frames_counter == 1:
            self.speed = 0
            for ghost in ghosts:
                ghost.state = "FROZEN"
                ghost.freeze()
        
        if self.dead == True and self.death_frames_counter == self.MAX_DEATH_FRAMES_DURATION * 10:
            self.resetPosition(starting_positions[0], "NONE")
            self.speed = PACMAN_SPEED
            self.lock_turn_time = 0
            self.queue_turn = "NONE"
            for i in range(4):
                ghosts[i].resetPosition(starting_positions[i + 1], "UP")
                ghosts[i].unfreeze()
                ghosts[i].state = "SCATTER"
                ghosts[i].scatter_time = ghosts[i].MAX_SCATTER_TIME
            self.dead = False
            self.death_frames_counter = 0
            if(self.lives == 0):
                return True

    def canTurn(self, tile_map, wanted_direction):
        if wanted_direction == "NONE" or wanted_direction == self.direction:
            return False

        return not self.checkObstructionDirection(tile_map, wanted_direction)

    def eatFood(self, tile_map, ghost_list):
        if self.dead == True:
            return
        
        score_value = {
        -2: 10,    # Pellet
        -3: 20,    # Power pellet
        -4: 100,   # Cherry
        -5: 200,   # Orange
        -6: 300,   # Apple
        -7: 400,   # Strawberry
        }
        
        value = tile_map.tilemap[self.y][self.x]
        if(value < -1 and value > -9):
            tile_map.score += score_value[value]
            tile_map.tilemap[self.y][self.x] = -1
            if(value == -2):
                tile_map.pellet_count -= 1
            elif (value == -3):
                tile_map.pellet_count -= 1
                self.sound[4].play()
                for ghost in ghost_list:
                    if ghost.state != "DEAD":
                        ghost.state = "SCARED"
                        ghost.speed = TMap.GHOST_SPEED / 2
                        if(ghost.state != "SCARED"):    ghost.snapDisplayToGrid()
                        ghost.scared_time = ghost.MAX_SCARED_TIME
            else:
                self.sound[2].play()

    def update(self, tile_map):
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

        frame_index = (self.movement_frame_counter // self.MAX_MOVEMENT_FRAMES_DURATION) % 3  # Cycles between frame 1 2 and 3
        if(self.dead == False):
            if(self.direction == "NONE"): 
                screen.blit(self.movement_frames[direction_mapping[self.direction]][0], (self.display_x - PACMAN_RADIUS, self.display_y - PACMAN_RADIUS))
                return

            # Draws open mouth if obstructed
            if(self.checkObstructionDirection(tilemap.tilemap, self.direction) == True):   self.movement_frame_counter = 0

            screen.blit(self.movement_frames[direction_mapping[self.direction]][frame_index], (self.display_x - PACMAN_RADIUS, self.display_y - PACMAN_RADIUS))

            # only increment frame counter if not obstructed
            if not self.checkObstructionDirection(tilemap.tilemap, self.direction):
                self.movement_frame_counter = (self.movement_frame_counter + 1) % (self.MAX_MOVEMENT_FRAMES_DURATION * 3)

            SOUND_INTERVAL = 36
            STOPPING_DELAY = 15

            if not self.checkObstructionDirection(tilemap.tilemap, self.direction):
                self.stopping_counter = 0
                if self.sound_index == 0:  
                    self.sound[1].play()

                self.sound_index += 1

                if self.sound_index >= SOUND_INTERVAL: 
                    self.sound[1].play()
                    self.sound_index = 1  
            else:
                self.stopping_counter += 1 
                if self.stopping_counter >= STOPPING_DELAY:
                    self.sound[1].stop()  
                    self.sound_index = 0  
                    self.stopping_counter = 0
        else:
            frame_index = (self.death_frames_counter // self.MAX_DEATH_FRAMES_DURATION) % 11
            screen.blit(self.death_frames[frame_index], (self.display_x - PACMAN_RADIUS, self.display_y - PACMAN_RADIUS))
            self.death_frames_counter += 1
