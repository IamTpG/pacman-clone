# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
TILE_SIZE     = 20

MAP_WIDTH  = 29
MAP_HEIGHT = 31

SCREEN_OFFSET = 10
SCREEN_WIDTH  = (MAP_WIDTH  + 0) * TILE_SIZE
SCREEN_HEIGHT = (MAP_HEIGHT + 6) * TILE_SIZE

PACMAN_SPEED  = 4
PACMAN_RADIUS = TILE_SIZE

class Pacman:
    def __init__(self, x, y, radius, direction):
        self.x = x
        self.y = y
        self.display_x = self.x * TILE_SIZE + SCREEN_OFFSET
        self.display_y = self.y * TILE_SIZE + SCREEN_OFFSET
        self.radius = radius
        self.direction = direction
    
    def Update(self):
        if (self.direction == "UP"):    self.display_y -= PACMAN_SPEED
        if (self.direction == "DOWN"):  self.display_y += PACMAN_SPEED
        if (self.direction == "LEFT"):  self.display_x -= PACMAN_SPEED
        if (self.direction == "RIGHT"): self.display_x += PACMAN_SPEED

        if (pacman.display_x < 0): pacman.display_x = SCREEN_WIDTH
        if (pacman.display_x > SCREEN_WIDTH): pacman.display_x = 0
        if (pacman.display_y < 0): pacman.display_y = SCREEN_HEIGHT
        if (pacman.display_y > SCREEN_HEIGHT): pacman.display_y = 0


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH + SCREEN_OFFSET * 2, SCREEN_HEIGHT + SCREEN_OFFSET * 2))
clock = pygame.time.Clock()
running = True

pacman = Pacman(MAP_WIDTH // 2, MAP_HEIGHT // 2, PACMAN_RADIUS, "LEFT")

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.constants.K_ESCAPE):
                running = False

            if (event.key == pygame.constants.K_UP):
                pacman.direction = "UP"
            if (event.key == pygame.constants.K_DOWN):
                pacman.direction = "DOWN"
            if (event.key == pygame.constants.K_LEFT):
                pacman.direction = "LEFT"
            if (event.key == pygame.constants.K_RIGHT):
                pacman.direction = "RIGHT"

    # Update
    pacman.Update()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "yellow", (pacman.display_x, pacman.display_y), PACMAN_RADIUS)

    # RENDER YOUR GAME HERE


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
