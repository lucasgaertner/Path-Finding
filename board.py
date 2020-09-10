import pygame
import sys
from time import sleep
import numpy as np
from A import A_Asterics





class Board():
    def __init__(self):
        self.board = []

        self.black = BLACK
        self.white = WHITE
        self.blue = BLUE
        self.green = GREEN
        #self.red = RED

    def Grid(self):
        SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
        CLOCK = pygame.time.Clock()
        pygame.display.set_caption("A* Path Finding Algorithm")
        SCREEN.fill(BLACK)
        return SCREEN, CLOCK

    def draw_squares(self, screen, clock, grid,sleeper=False):
        for row in range(ROWS):
            for col in range(COLS):            
                color = GREY
                rect = pygame.Rect(col*BLOCKSIZE, row*BLOCKSIZE,
                               BLOCKSIZE-MARGIN, BLOCKSIZE-MARGIN)
                if grid[row][col] == 1:
                    color = GREEN
                elif grid[row][col] == 2:
                    color = RED
                elif grid[row][col] == 3:
                    color = BLUE
                pygame.draw.rect(screen, color, rect)
        if sleeper:
            sleep(0.005)
        clock.tick(60)
        #pygame.display.flip()

    def Matrix(self):
        grid = np.zeros((COLS+1,ROWS+1), dtype=int)
        return grid

    def color(self, grid, color, limit, dict):
        limit += 1
        pos = pygame.mouse.get_pos()
        # Change the x/y screen coordinates to grid coordinates
        column, row = pos[0] // BLOCKSIZE, pos[1] // BLOCKSIZE
        # Set that location to one/two
        grid[row][column] = color
        if limit == 1:
            dict["start"] = pos
        elif limit == 2:
            dict["goal"] = pos
        return grid, dict, limit

    def output_draw(self, screen, grid, path, start, goal, show=True):
        start_x, start_y = start
        goal_x, goal_y = goal
        repl_3 = np.where(grid == 1)
        grid[repl_3] = 2
        grid[start_y][start_x] = 1
        grid[goal_y][goal_x] = 1
        if show == True:
            for x_way, y_way in path:
                grid[x_way][y_way] = 1
        else:
            for x_way, y_way in path:
                grid[x_way][y_way] = 3
        for row in range(ROWS):
            for col in range(COLS):            
                color = GREY
                rect = pygame.Rect(col*BLOCKSIZE, row*BLOCKSIZE,
                                BLOCKSIZE-MARGIN, BLOCKSIZE-MARGIN)
                pygame.draw.rect(screen, color, rect)
        return grid


def main():
    #global SCREEN, CLOCK
    LIMIT = 0
    DONE = False
    position_dict = {}
    board = Board()
    SCREEN, CLOCK = board.Grid()
    grid = board.Matrix()

    while not DONE:      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                DONE = True
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and LIMIT < 2:
                grid, position_dict, LIMIT = board.color(grid, 1, LIMIT, position_dict)
            elif event.type == pygame.MOUSEBUTTONDOWN and LIMIT >= 2:
                grid, position_dict, LIMIT = board.color(grid, 2, LIMIT, position_dict)
            elif event.type == pygame.KEYDOWN and LIMIT > 2:
                # get the beginning and end
                start, goal = position_dict["start"], position_dict["goal"]
                start_x, start_y = start[0] // BLOCKSIZE, start[1] // BLOCKSIZE
                goal_x, goal_y = goal[0] // BLOCKSIZE, goal[1] // BLOCKSIZE
                start = (start_x, start_y)
                goal = (goal_x, goal_y)

                #replacing the 1 and 2
                repl_1 = np.where(grid == 1)
                grid[repl_1] = 0
                repl_2 = np.where(grid == 2)
                grid[repl_2] = 1
                
                path, possibilities = A_Asterics(grid, start, goal)

                for k, v in possibilities.items():
                    board.output_draw(SCREEN, grid, v, start, goal,show=False)
                    board.draw_squares(SCREEN, CLOCK, grid)
                    pygame.display.update()
                    sleep(0.1)
               
                board.output_draw(SCREEN, grid, path, start, goal)

        board.draw_squares(SCREEN, CLOCK, grid)
        pygame.display.update()


if __name__ == '__main__':
    
    # Variables
    BLACK = (128, 128, 128)
    WHITE = (200, 200, 200)
    RED = (162,128,137)
    BLUE = (157,249,239)
    GREEN = (104,211,136)
    GREY = (237,247,246)
    MARGIN = 3

    WINDOW_HEIGHT = 800
    WINDOW_WIDTH = 800
    BLOCKSIZE = 50 
    ROWS = 16
    COLS = 16
    pygame.init()
    main()