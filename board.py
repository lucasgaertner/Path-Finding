import pygame
import sys
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

        # self.width = WIDTH
        # self.height = HEIGHT
        
    def Grid(self):
        SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
        CLOCK = pygame.time.Clock()
        pygame.display.set_caption("A* Path Finding Algorithm")
        SCREEN.fill(BLACK)
        return SCREEN, CLOCK

    def draw_squares(self, screen, clock, grid):
        for row in range(ROWS):
            for col in range(COLS):            
                color = WHITE
                rect = pygame.Rect(col*BLOCKSIZE, row*BLOCKSIZE,
                               BLOCKSIZE-MARGIN, BLOCKSIZE-MARGIN)
                if grid[row][col] == 1:
                    color = GREEN
                elif grid[row][col] == 2:
                    color = BLUE
                pygame.draw.rect(screen, color, rect)
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

    def output_draw(self, screen, grid, path, start, goal):

        start_x, start_y = start
        goal_x, goal_y = goal
        repl_3 = np.where(grid == 1)
        grid[repl_3] = 2
        grid[start_y][start_x] = 1
        grid[goal_y][goal_x] = 1
        for x_way, y_way in path:
            print("A* calculated:", x_way,y_way)
            grid[x_way][y_way] = 1
        
        for row in range(ROWS):
            for col in range(COLS):            
                color = GREY
                rect = pygame.Rect(col*BLOCKSIZE, row*BLOCKSIZE,
                                BLOCKSIZE-MARGIN, BLOCKSIZE-MARGIN)
                if grid[row][col] == 1:
                    color = GREEN
                elif grid[row][col] == 2:
                    color = BLUE
                # elif grid[row][col] == 3:
                #     color = GREEN
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
                print("Passing x:",goal_x, "and y:" ,goal_y, "to grid:\n",grid)
                print("Passing x:",start_x, "and y:" ,start_y)
                path = A_Asterics(grid, start, goal)

                
                #print(path)
                board.output_draw(SCREEN, grid, path, start, goal)

        board.draw_squares(SCREEN, CLOCK, grid)
        pygame.display.update()


if __name__ == '__main__':
    
    # Variables
    BLACK = (0, 0, 0)
    WHITE = (200, 200, 200)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    GREY = (128,128,128)
    MARGIN = 3

    WINDOW_HEIGHT = 800
    WINDOW_WIDTH = 800
    BLOCKSIZE = 50 
    ROWS = 16
    COLS = 16
    pygame.init()
    main()