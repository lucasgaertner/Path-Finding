import numpy as np
import operator

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self, other):
        return self.position == other.position


maze = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
       ,[0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
       ,[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
       ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
       ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
       ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
       ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
       ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
       ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
       ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
       ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
       ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
       ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
       ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
       ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
       ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
       ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

start = (0,0)
start_row, start_col = start
goal = (2,2)
goal_row, goal_col = goal


def A_Asterics(maze, start, goal):
    start_node = Node(None, start)
    start_node.f = start_node.g = start_node.h = 0
    goal_node = Node(None, goal)
    goal_node.f = goal_node.g = goal_node.h = 0
    
    open_list = []
    closed_list = []
    
    open_list.append(start_node)
    
    successors = [(0,1),(0,-1),(-1,0),(-1,-1),(-1,1),(1,-1),(1,0),(1,1)] #middle, top, bottom
    #0 0 0
    #0 1 0
    #0 0 0
    
    while len(open_list) > 0:
        #q = get_q(open_list)
        current_node = open_list[0]
        q = 0
    # filtering all f which are getting higher result than the min Distance calculation f
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                q = index
    
        open_list.pop(q)
        closed_list.append(current_node)
    
        if current_node == goal_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []
        for square in successors:
            x_c, y_c = square
            node_position = (current_node.position[0] + x_c, current_node.position[1] + y_c)

            # barricaden
            if maze[node_position[0]][node_position[1]] != 0: #vorher 1
                continue
    
            if node_position[0] > (len(maze) -1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze) - 1]) -1 ) or node_position[1] < 0:
                continue
            
            new_node = Node(current_node, node_position)
            children.append(new_node)
    
        for child in children:
            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    break
            else:
                # Create the f, g, and h values
                child.g = current_node.g + 1
                # H: Manhattan distance to end point
                child.h = abs(child.position[0] - goal_node.position[0]) + abs(child.position[1] - goal_node.position[1])
                child.f = child.g + child.h
        
                # Child is already in the open list
                for open_node in open_list:
                    # check if the new path to children is worst or equal 
                    # than one already in the open_list (by measuring g)
                    if child == open_node and child.g >= open_node.g:
                        break
                else:
                    # Add the child to the open list
                    open_list.append(child)

path = A_Asterics(maze,start,goal)
print("The result is", path)