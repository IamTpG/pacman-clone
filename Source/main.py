# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
TILE_RESU = 8   # Tile size in .png
TILE_SIZE = 20  # Tile size to render

MAP_WIDTH  = 29
MAP_HEIGHT = 37

SCREEN_OFFSET = 10
SCREEN_WIDTH  = MAP_WIDTH  * TILE_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE

PACMAN_SPEED  = 3
PACMAN_RADIUS = TILE_SIZE - 5

# Utils function for reading tilemap
def ReadMap():
    file = open("D:/06_Program Files/Github/pacman-clone/Resource/map/map.txt")
    m = [[0] * MAP_WIDTH]

    for i in range(1, MAP_HEIGHT + 1):
        line = file.readline()
        m.append([0] + list(map(int, line.split())) + [0])

    m.append([0] * MAP_WIDTH)

    file.close()
    return m

class Pacman:
    def __init__(self, x, y, radius, direction):
        self.x = x
        self.y = y
        self.display_x = self.x * TILE_SIZE + SCREEN_OFFSET - radius + 5
        self.display_y = self.y * TILE_SIZE + SCREEN_OFFSET - radius + 15
        self.radius = radius
        self.direction = direction
    
    def update(self):
        if (self.direction == "UP"):    self.display_y -= PACMAN_SPEED
        if (self.direction == "DOWN"):  self.display_y += PACMAN_SPEED
        if (self.direction == "LEFT"):  self.display_x -= PACMAN_SPEED
        if (self.direction == "RIGHT"): self.display_x += PACMAN_SPEED

        if (pacman.display_x < 0): pacman.display_x = SCREEN_WIDTH
        if (pacman.display_x > SCREEN_WIDTH): pacman.display_x = 0
        if (pacman.display_y < 0): pacman.display_y = SCREEN_HEIGHT
        if (pacman.display_y > SCREEN_HEIGHT): pacman.display_y = 0
    
    def render(self, screen):
        pygame.draw.circle(screen, "yellow", (self.display_x, self.display_y - self.radius + 5), PACMAN_RADIUS)

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

pacman = Pacman(15, 28, PACMAN_RADIUS, "NONE")
tilemap = Tilemap("D://06_Program Files//Github//pacman-clone//Resource//map//map.png")

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

    # update
    pacman.update()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    tilemap.render(screen)
    pacman.render(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
