import pygame
import sys
import numpy as np
from A import A_Asterics


# Variables
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
BLOCKSIZE = 50 
ROWS = 16
COLS = 16



class Board():
    def __init__(self):
        self.board = []

    def draw_squares(self, win, grid):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(COLS):            
                color = WHITE
                if grid[row][col] == 1:
                    color = GREEN
                elif grid[row][col] == 2:
                    color = BLUE
                rect = pygame.Rect(col*BLOCKSIZE, row*BLOCKSIZE,
                               BLOCKSIZE, BLOCKSIZE)
                pygame.draw.rect(SCREEN, color, rect, 1)
        pygame.display.flip()

    def Matrix(self):
        grid = np.zeros((COLS+1,ROWS+1), dtype=int)
        return grid

    def color(self, grid, color, limit, dict):
        pos = pygame.mouse.get_pos()
        # Change the x/y screen coordinates to grid coordinates
        column, row = pos[0] // BLOCKSIZE, pos[1] // BLOCKSIZE
        # Set that location to one/two
        grid[row][column] = color
        if limit == 1:
            dict["start"] = pos
        elif limit == 2:
            dict["goal"] = pos
        limit += 1
        return grid, dict, limit

    def output_draw(self, grid, path, start, goal):
        pass


def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    CLOCK = pygame.time.Clock()
    LIMIT = 0
    SCREEN.fill(BLACK)
    position_dict = {}

    board = Board()
    grid = board.Matrix()

    while True:      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and LIMIT < 2:
                grid, position_dict, LIMIT = board.color(grid, 1, LIMIT, position_dict)
            elif event.type == pygame.MOUSEBUTTONDOWN and LIMIT >= 2:
                grid, position_dict, LIMIT = board.color(grid, 2, LIMIT, position_dict)
            elif event.type == pygame.KEYDOWN:
                # get the beginning and end
                start, goal = position_dict["start"], position_dict["goal"]
                start_x, start_y = start[0] // BLOCKSIZE, start[1] // BLOCKSIZE
                goal_x, goal_y = goal[0] // BLOCKSIZE, goal[1] // BLOCKSIZE
                print(goal_x, goal_y,"Staaaart")
                start = (start_x, start_y)
                goal = (goal_x, goal_y)
                #replacing the 1 and 2
                repl_1 = np.where(grid == 1)
                grid[repl_1] = 0
                repl_2 = np.where(grid == 2)
                grid[repl_2] = 1
                path = A_Asterics(grid, start, goal)
                repl_3 = np.where(grid == 1)
                grid[repl_3] = 2
                print(start_y,start_x,"startx", goal_x, goal_y,"goaly")
                grid[start_y][start_x] = 1
                grid[goal_y][goal_x] = 1
                print(grid)
                print(path)
                #output_draw(grid, path, start, goal)

        board.draw_squares(SCREEN, grid)
        pygame.display.update()

main()