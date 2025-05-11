import random
import pygame

pygame.init()

BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 4
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
grid = None
hue_value = 200
clock = pygame.time.Clock()


def make_2d_array(cols, rows):
    arr = [[0 for i in range(cols)] for i in range(rows)]
    return arr


def within_cols(i):
    return i >= 0 and i < GRID_WIDTH


def within_rows(i):
    return i >= 0 and i < GRID_HEIGHT


def draw_grid():
    global grid
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            if grid[i][j] > 0:
                top_left = (i * TILE_SIZE, j * TILE_SIZE)
                color = pygame.Color(0)
                color.hsva = (grid[i][j], 100, 100, 100)
                pygame.draw.rect(screen, color, (*top_left, TILE_SIZE, TILE_SIZE))
    
    next_grid = make_2d_array(GRID_WIDTH, GRID_HEIGHT)
    
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            state = grid[i][j]
            if state > 0:
                if j + 1 < GRID_HEIGHT:
                    below = grid[i][j + 1]
                    direction = 1 if random.randint(1, 10) > 5 else -1

                    below_a = grid[i + direction][j + 1] if within_cols(i + direction) and within_rows(j + 1) else -1
                    below_b = grid[i - direction][j + 1] if within_cols(i - direction) and within_rows(j + 1) else -1

                    if below == 0:
                        next_grid[i][j + 1] = state
                    elif below_a == 0:
                        next_grid[i + direction][j + 1] = state
                    elif below_b == 0:
                        next_grid[i - direction][j + 1] = state
                    else:
                        next_grid[i][j] = state
                else:
                    # at the bottom
                    next_grid[i][j] = state
    grid = next_grid
        
        
def mouse_dragged():
    global grid, hue_value
    x, y = pygame.mouse.get_pos()
    mouse_row = y // TILE_SIZE
    mouse_col = x // TILE_SIZE
        
    # randomly add an area of sand particles
    matrix = 5
    extent = matrix // 2
    for i in range(-extent, extent + 1, 1):
        for j in range(-extent, extent + 1, 1):
            if random.randint(1, 4) <= 3:
                col = mouse_col + i
                row = mouse_row + j
                if within_cols(col) and within_rows(row):
                    grid[col][row] = hue_value
    
    # change the color of the sand over time
    hue_value = hue_value + 1 if hue_value < 360 else 1          


def main():
    running = True
    global grid
    grid = make_2d_array(GRID_WIDTH, GRID_HEIGHT)
    
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            mouse_dragged()
        
        screen.fill(BLACK)
        draw_grid()
        pygame.display.update()
    
    pygame.quit()


if __name__ == "__main__":
    main()