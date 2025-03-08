if __name__ == '__main__':
    print("This is a module. Not meant to be run standalone.")

import heapq
import random
from collections import deque

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


def dfs_recursive_ordered(grid, start, visited, goal,expanded_list, ghost_list):
    rows, cols = len(grid), len(grid[0])
    
    # Check boundaries and if already visited
    if not (1 <= start[0] <= rows and 1 <= start[1] <= cols ) or (start[0], start[1]) in visited:
        return None
    visited.add((start[0], start[1]))
    # if current = finish
    if start == goal:
        
        return [(start[0],start[1])]
    
   
    directions = [(1, 0),(0, 1), (-1, 0), (0, -1) ]
    # for neighbors of current
    for di, dj in directions:
        ni = di + start[0]
        nj = dj + start[1]
        if 1 <= nj <= cols and 1 <= ni <= rows and grid[ni][nj] <= -1:
           
            if ((ni,nj)) not in visited:
                expanded_list.append((ni,nj))
                result = dfs_recursive_ordered(grid, (ni, nj), visited, (goal[0],goal[1]),expanded_list,ghost_list)
                if result is not None: 
                    return [(start[0], start[1])] + result
    return None

def heuristic(a, b):
    # Manhattan distance as a heuristic (suitable for 4-directional movement)
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) # Manhattan = |dx| + |dy|

def dfs_limited(grid, start, goal, depth, limit, visited, expanded_list):
    rows, cols = len(grid), len(grid[0])
    if start == goal:  # if goal
        return [(start[0],start[1])]
    if depth >= limit:  # reach limit
        return None
    
    visited.add(start)  
    
    # up, down, left, right 
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = start[0] + di, start[1] + dj # consider this neighbor
        if (1 <= ni <= len(grid) and 1 <= nj <= len(grid[0]) and grid[ni][nj] <=-1): # valid index and not wall
            if ((ni, nj)) not in visited: 
                expanded_list.append(start)
                result = dfs_limited(grid, (ni,nj),goal, depth + 1, limit, visited,expanded_list)
                if result is not None: 
                    return [(start[0], start[1])] + result
    return None

def ids(grid, start, goal,expanded_list, ghost_list):
    depth_limit = 0
    while True:  #depth increase until find the goal
        visited = set()
        path = dfs_limited(grid, start, goal, 0, depth_limit, visited,expanded_list)
        if(path is not None):
            return path
        depth_limit += 1  #increase depth
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
