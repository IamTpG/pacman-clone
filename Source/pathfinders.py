if __name__ == '__main__':
    print("This is a module. Not meant to be run standalone.")

import heapq
import random
from collections import deque
MAX_DEPTH = 1000  # Giới hạn độ sâu tối đa 
def bfs(grid, start, goal, expanded, ghost_list):
    #initialize variable
    rows, cols = len(grid), len(grid[0])
    # Directions: left, right, up, down
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    #used for tracing back the path
    trace = [[(-1, -1) for i in range(0, cols + 1)] for j in range(0, rows + 1)]
    found = False
    
    #have a list act as an heap priority queue
    q = deque()
    q.append(start)
    
    #a set of expanded node
    expanded = set()
    
    #main process
    while q and (not found):
        u = q.popleft()

        for dx, dy in directions:
            v = (u[0] + dx, u[1] + dy)

            if (v[0] < 1 or v[0] > rows):
                continue
            if (v[1] < 1 or v[1] > cols):
                continue
            if (grid[v[0]][v[1]] > -1):
                continue
            if (v in expanded):
                continue

            trace[v[0]][v[1]] = u
            
            # early stopping
            if (v == goal):
                found = True
                break

            expanded.add(v)
            q.append(v)

    if (found == False):
        return None
    
    # tracing back the path
    u = goal
    path = [goal]
    while (u != start):
        u = trace[u[0]][u[1]]
        path.append(u)

    path.reverse()
    return path

def ucs(grid, start, goal, expanded, ghost_list):
    #initialize variable
    rows, cols = len(grid), len(grid[0])
    # Directions: left, right, up, down
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    #d[x][y] = min distance from start to (x, y)
    d = [[int(1e9) for i in range(0, cols + 1)] for j in range(0, rows + 1)]

    #used for tracing back the path
    trace = [[(-1, -1) for i in range(0, cols + 1)] for j in range(0, rows + 1)]
    found = False
    
    #have a list act as an heap priority queue
    q = [(0, start)]
    heapq.heapify(q)
    d[start[0]][start[1]] = 0
    
    #a set of expanded node
    expanded = set()
    
    #main process
    while q and (not found):
        (wu, u) = heapq.heappop(q)

        if (u == goal):
            found = True
            break

        for dx, dy in directions:
            v = (u[0] + dx, u[1] + dy)
            uv = 1 # distance between u and v is always 1

            if (v[0] < 1 or v[0] > rows):
                continue
            if (v[1] < 1 or v[1] > cols):
                continue
            if (grid[v[0]][v[1]] > -1):
                continue
            if (v in expanded):
                continue

            if (d[v[0]][v[1]] > d[u[0]][u[1]] + uv):
                d[v[0]][v[1]] = d[u[0]][u[1]] + uv
                trace[v[0]][v[1]] = u
                expanded.add(v)
                heapq.heappush(q, (d[v[0]][v[1]], v))

    if (found == False):
        return None
    
    # tracing back the path
    u = goal
    path = [goal]
    while (u != start):
        u = trace[u[0]][u[1]]
        path.append(u)

    path.reverse()
    return path



def heuristic(a, b):
    # Manhattan distance as a heuristic (suitable for 4-directional movement)
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) # Manhattan = |dx| + |dy|


def findCycle(trace, u, v):
    while (u != (-1, -1)):
        u = trace[u[0]][u[1]]
        if (u == v):
            return True
    return False

def dls(grid, start, goal, expanded, ghost_list, limit, direction_vector):
    # initialize variables
    rows, cols = len(grid), len(grid[0])

   

    # used for calculating and limiting the DFS depth
    depth = [[0 for i in range(0, cols + 1)] for j in range(0, rows + 1)]

    # used for tracing back the path
    prev_vector = [[(0, 0) for i in range(0, cols + 1)] for j in range(0, rows + 1)]
    prev_vector[start[0]][start[1]] = direction_vector

    # used for tracing back the path
    trace = [[(-1, -1) for i in range(0, cols + 1)] for j in range(0, rows + 1)]
    found = False
    
    # have a list act as a stack
    s = []
    s.append(start)
    depth[start[0]][start[1]] = 0

    #main process
    while (s and (not found)):
        u = s.pop()

        # used for analysis
        expanded.add(u)

         # directions = [left, right, up, down]
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        old_direction = prev_vector[u[0]][u[1]]
        directions.remove((-old_direction[0], -old_direction[1]))


        if (depth[u[0]][u[1]] == limit):
            continue

        for di, dj in directions:
            v = (u[0] + di, u[1] + dj)

            # skip invalid moves
            if (v[0] < 1 or v[0] > rows):   continue
            if (v[1] < 1 or v[1] > cols):   continue
            if (grid[v[0]][v[1]] != -1):    continue
            if (findCycle(trace, u, v)):    continue

            trace[v[0]][v[1]] = u
            prev_vector[v[0]][v[1]] = (di, dj)
            # early stopping
            if (v == goal):
                found = True
                break

            s.append(v)
            depth[v[0]][v[1]] = depth[u[0]][u[1]] + 1

    if (found == False):
        return None
    
    # tracing back the path
    u = goal
    path = [goal]
    while (u != start):
        u = trace[u[0]][u[1]]
        path.append(u)

    path.reverse()
    return path

def ids(grid, start, goal, expanded, ghost_list, self_direction):
    rows, cols = len(grid), len(grid[0])
    direction_vector = direction_to_vector(self_direction)
    for depth in range(rows * cols):
        path = dls(grid, start, goal, expanded, ghost_list, depth, direction_vector)
        if (path is not None):
            return path
    
    return None
def a_star(grid, start, goal, expanded, ghost_list):
    #initialize variable
    rows, cols = len(grid), len(grid[0])
    # Directions: left, right, up, down
    directions = [(0, -1), (0, 1),(-1, 0), (1, 0)]
    
    #have a list act as an heap priority queue
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(start, goal), 0, start, [start])) 
    
    #a set of expanded node
    expanded = set()
    
    #main process
    while open_list:
        #take information of current node and check if it was expanded
        f, g, expanding_node, path = heapq.heappop(open_list)
        if expanding_node in expanded:
            continue
        expanded.add(expanding_node)
        
        #if the current node was not expanded, check if it is goal
        #(late stop)
        if expanding_node == goal:
            return path
        
        i, j = expanding_node
        for di, dj in directions:
            ni, nj = i + di, j + dj 
            neighbor = (ni, nj)
            if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] <= -1 and neighbor not in expanded:
                #update and add it without needing to update old status
                #because the which one has better priority will be taken first
                #and add into expanded
                new_g = g + 1  # Cost from current to neighbor (assumed to be 1)
                new_f = new_g + heuristic(neighbor, goal)
                new_path = path + [neighbor]
                heapq.heappush(open_list, (new_f, new_g, neighbor, new_path))
    
    return None  # No path found


def find_direction(path): 
    direction = (-path[0][0] + path[1][0], -path[0][1] + path[1][1])
    return switch_case(direction)

def switch_case(direction):
    switcher = {
        (0, -1): "LEFT",
        (0, 1):  "RIGHT",
        (-1, 0): "UP",
        (1, 0):  "DOWN",
    }

    return switcher.get(direction, "Invalid")  # Default case 
def direction_to_vector(direction):
    switcher = {
        "LEFT":(0, -1),
        "RIGHT":(0, 1),
        "UP":(-1, 0),
        "DOWN":(1, 0)
    }

    return switcher.get(direction, "Invalid")  # Default case 
