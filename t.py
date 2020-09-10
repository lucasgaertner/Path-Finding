import pygame
import sys
import numpy as np


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
        #self.grid = np.zeros((cols+1,rows+1), dtype=int)

    def draw_squares(self, win, grid):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(COLS):            
                color = WHITE
                if grid[row][col] == 1:
                    color = GREEN
                elif grid[row][col] == 2:
                    color = BLUE
                rect = pygame.Rect(row*BLOCKSIZE, col*BLOCKSIZE,
                               BLOCKSIZE, BLOCKSIZE)
                pygame.draw.rect(SCREEN, color, rect, 1)
    
    def Matrix(self):
        grid = np.zeros((COLS+1,ROWS+1), dtype=int)
        return grid

    def color(self, grid, color, limit, dict):
        pos = pygame.mouse.get_pos()
        x, y = pos

        # Change the x/y screen coordinates to grid coordinates
        row, column = x // BLOCKSIZE, y // BLOCKSIZE
        # Set that location to one
        grid[row][column] = color
        if limit == 1:
            dict["start"] = pos
        elif limit == 2:
            dict["goal"] = pos
        limit += 1
        return grid, x, y, dict, limit

    # def ouput(self, grid, start, goal):
    #     grid[]

class Node():
    
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position


def A_Asterics(maze, start, goal):
    # Create start and end node
    start_node = Node(None, start)
    start_node.f = start_node.g = start_node.h = 0
    goal_node = Node(None, goal)
    goal_node.f = goal_node.g = goal_node.h = 0

    open_list = []
    closed_list = []

    open_list.append(start_node)

    while len(open_list) > 0:
        # get the node of the current list 
        current_node = open_list[0]
        current_index = 0

        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)


        # Goal output
        if current_node == goal_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children =  []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: 
                            # x x x
                            # x 0 x
                            # x x x
            # get the current node
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] > (len(maze) -1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze) - 1]) -1 ) or node_position[1] < 0:
                continue

            # barricaden
            if maze[node_position[0]][node_position[1]] != 1: #vorher 1
                continue

            # create the new node
            new_node = Node(current_node, node_position)
            children.append(new_node)

            for child in children:
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

            # calc the new distance
            child.g = current_node.g
            print(child.g)
            child.h = ((child.position[0] - goal_node.position[0]) **2) + ((child.position[1] - goal_node.position[1]) **2)
            child.f = child.g + child.h

            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
            open_list.append(child)



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
                grid, x, y, position_dict, LIMIT = board.color(grid, 1, LIMIT, position_dict)
            elif event.type == pygame.MOUSEBUTTONDOWN and LIMIT >= 2:
                grid, x, y, position_dict, LIMIT = board.color(grid, 2, LIMIT, position_dict)
            elif event.type == pygame.KEYDOWN:
                # get the beginning and end
                start, goal = position_dict["start"], position_dict["goal"]
                path = A_Asterics(grid, start, goal)
                print("path", path)

        board.draw_squares(SCREEN, grid)
        pygame.display.update()

main()