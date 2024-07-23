from turtle import shape
import numpy as np
import pygame # pip install pygame
import time
from math import cos, sin, pi, sqrt

# Set colors
BG_COLOR = (50, 50, 50)
GRID_COLOR = (0, 0, 0)
DIE_COLOR = (219,112,147)
ALIVE_COLOR = (255, 255, 255)

def draw_hexagon(screen, x, y, size, color):
    points = [(x + size * cos(theta), y + size * sin(theta)) for theta in [pi / 3 * i for i in range(6)]]
    pygame.draw.polygon(screen, color, points)

def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        # Calculate the six neighbors for a hexagonal grid
        neighbors = [(row + dr, col + dc) for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]]
        alive_cells = sum(cells[nr % cells.shape[0], nc % cells.shape[1]] for nr, nc in neighbors)
        color = BG_COLOR if cells[row, col] == 0 else ALIVE_COLOR

        if cells[row, col] == 1:
            if alive_cells < 2 or alive_cells > 3:
                if with_progress:
                    color = DIE_COLOR
            elif 2 <= alive_cells <=3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = ALIVE_COLOR
        else:
            if alive_cells == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = ALIVE_COLOR

        draw_hexagon(screen, col * size * 1.5, row * size * sqrt(3) * (0.5 if col % 2 == 0 else 1), size, color)

    return updated_cells

if __name__ == '__main__':
    #Initialize pygame
    pygame.init()
    # Set size of cells
    size=10
    # Set size of screen
    WIDTH = 800
    HEIGHT = 600
    cells = np.random.randint(0, 2, size=(60, 80))

    #Init surface/screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Fill the screen with the grid
    screen.fill(GRID_COLOR)

    update(screen, cells, size)

    #Update the full screen
    pygame.display.flip()
    #Update only portions of the screen
    pygame.display.update()

    # Initialize running as false, so it won't immediately start the game
    running = False

    # Create infinite while loop to listen to keys
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # If space key is pressed, change running in true/flase
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, size)
                    pygame.display.update()
                    # Listen to mouse clicks
            # In the main loop, update the mouse click handling
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                col = int(position[0] // (size * 1.5))
                row = int(position[1] // (size * sqrt(3) * (0.5 if col % 2 == 0 else 1)))
                if cells[row, col] == 0:
                    cells[row, col] = 1
                else:
                    cells[row, col] = 0
                update(screen, cells, size)
                pygame.display.update()

        if running:
            cells = update(screen, cells, size, with_progress=True)
            pygame.display.update()
        time.sleep(0.1)


