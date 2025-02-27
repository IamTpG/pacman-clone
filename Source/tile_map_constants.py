# Important constants for the tile map

TILE_RESU = 8   # Tile size in .png
TILE_SIZE = 16  # Tile size to render

MAP_WIDTH  = 29
MAP_HEIGHT = 37

SCREEN_OFFSET = 10
SCREEN_WIDTH  = MAP_WIDTH  * TILE_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE

PACMAN_RADIUS = TILE_SIZE - 5
PACMAN_SPEED = 2

GHOST_RADIUS = TILE_SIZE - 5
GHOST_SPEED = 2

if __name__ == '__main__':
    print("This is a module, it should not be run standalone!")