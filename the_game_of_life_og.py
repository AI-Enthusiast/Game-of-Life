from turtle import shape
import numpy as np
import pygame # pip install pygame
import time

# Set colors
BG_COLOR = (50, 50, 50)
GRID_COLOR = (0, 0, 0)
DIE_COLOR = (219,112,147)
ALIVE_COLOR = (255, 255, 255)

def update(screen, cells, size, with_progress=False):
    # Set updated cells to a zeros matrix
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        # Find the alive cells by summing the cells in the two adjacent rows and columns and subtracting the cell
        alive_cells = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = BG_COLOR if cells[row, col] == 0 else ALIVE_COLOR

        #Apply rules of the game of life
        # Cell is alive(1)
        if cells[row, col] == 1:
            if alive_cells < 2 or alive_cells > 3:
                if with_progress:
                    color = DIE_COLOR
            elif 2 <= alive_cells <=3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = ALIVE_COLOR
        # Cell is dead(0)
        else:
            if alive_cells == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = ALIVE_COLOR

        pygame.draw.rect(screen, color,
                         (col * size, row * size, size - 1, size - 1))

    return updated_cells

if __name__ == '__main__':
    #Initialize pygame
    pygame.init()
    # Set size of cells
    size= 100
    # Set size of screen
    WIDTH = 1600
    HEIGHT = 900
    cells = np.random.randint(0, 2, size=(216, 384))

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
                if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                if cells[position[1] // size, position[0]// size] == 0:
                    cells[position[1] // size, position[0]// size] = 1
                else:
                    cells[position[1] // size, position[0]// size] = 0
                update(screen, cells, size)
                pygame.display.update()

        if running:
            cells = update(screen, cells, size, with_progress=True)
            pygame.display.update()
        time.sleep(0.1)

