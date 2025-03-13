if __name__ == '__main__':
    print("This is a module. Not meant to be run standalone.")
    exit()

import heapq
from collections import deque

# DIRECTIONS = [left, right, up, down]
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# Ghosts' house position
GATE  = [(19, 14), (19, 15), (19, 16)]
HOUSE = [(19, 14), (19, 15), (19, 16),
        (20, 12), (20, 13), (20, 14), (20, 15), (20, 16), (20, 17), (20, 18),
        (21, 12), (21, 13), (21, 14), (21, 15), (21, 16), (21, 17), (21, 18)]


# Tracing back the path from start to goal
def tracePath(tracer, start, goal):
    u = goal
    path = [goal]

    while (u != start):
        u = tracer[u[0]][u[1]]
        path.append(u)

    path.reverse()
    return path


def bfs(grid, start, goal, expanded):
    # initialize variables
    # note: the grid indexes start from 1
    rows, cols = len(grid), len(grid[0])

    # tracer[][] is used for tracing back the path
    # tracer[x][y] = parent of (x, y)
    tracer = [[(-1, -1) for _ in range(cols + 1)] for _ in range(rows + 1)]
    found = False
    
    # a frontier using FIFO (queue)
    q = deque()
    q.append(start)

    # reached nodes = expanded nodes + nodes in the frontier
    reached = set()
    reached.add(start)

    # main process
    while (q and (not found)):
        u = q.popleft()

        expanded.add(u)

        for dx, dy in DIRECTIONS:
            # node v is a neighbor of node u
            v = (u[0] + dx, u[1] + dy)

            # skip invalid moves
            if (v[0] < 1 or v[0] > rows):   continue
            if (v[1] < 1 or v[1] > cols):   continue
            if (grid[v[0]][v[1]] > -1):     continue
            if (v in reached):              continue

            tracer[v[0]][v[1]] = u
            
            # early stopping
            if (v == goal):
                found = True
                break

            reached.add(v)
            q.append(v)

    # tracing back the path
    if (found == True):
        return tracePath(tracer, start, goal)

    return None

def ucs(grid, start, goal, expanded, ghost_list):
    # initialize variables
    # note: the grid indexes start from 1
    rows, cols = len(grid), len(grid[0])

    # tracer[][] is used for tracing back the path
    # tracer[x][y] = parent of (x, y)
    tracer = [[(-1, -1) for _ in range(cols + 1)] for _ in range(rows + 1)]
    found = False

    # d[x][y] = min distance from start to (x, y)
    d = [[int(1e9) for _ in range(cols + 1)] for j in range(rows + 1)]
    
    # a frontier using min heap (priority queue)
    q = [(0, start)]
    heapq.heapify(q)
    d[start[0]][start[1]] = 0
        
    # reached nodes = expanded nodes + nodes in the frontier
    reached = set()
    reached.add(start)
        
    # main process
    while (q and (not found)):
        (wu, u) = heapq.heappop(q)

        # expanded is used for analysis
        expanded.add(u)

        if (u == goal):
            found = True
            break

        for dx, dy in DIRECTIONS:
            # node v is a neighbor of node u
            # distance between u and v is always 1
            v = (u[0] + dx, u[1] + dy)
            uv = 1

            # skip in valid moves
            if (v[0] < 1 or v[0] > rows):   continue
            if (v[1] < 1 or v[1] > cols):   continue
            if (grid[v[0]][v[1]] > -1):     continue
            if (v in reached):              continue

            if (d[v[0]][v[1]] > d[u[0]][u[1]] + uv):
                d[v[0]][v[1]] = d[u[0]][u[1]] + uv
                tracer[v[0]][v[1]] = u
                reached.add(v)
                heapq.heappush(q, (d[v[0]][v[1]], v))

    # tracing back the path
    if (found == True):
        return tracePath(tracer, start, goal)
    
    return None


def dlsBacktrack(grid, u, goal, path, expanded, l):
    # initialize variables
    # note: the grid indexes start from 1
    rows, cols = len(grid), len(grid[0])

    # expanded is used for analysis
    expanded.add(u)

    if (u == goal):
        return

    if (len(path) >= l):
        return
    
    for dx, dy in DIRECTIONS:
        # node v is a neighbor of node u
        v = (u[0] + dx, u[1] + dy)

        # skip invalid moves
        if (v[0] < 1 or v[0] > rows):   continue
        if (v[1] < 1 or v[1] > cols):   continue
        if (grid[v[0]][v[1]] > -1):     continue
        if (v in path):                 continue

        # a tiny improvement:
        # no need to check paths in the house while chasing pacman
        if (goal not in HOUSE and v in HOUSE):
            continue

        path.append(v)
        dlsBacktrack(grid, v, goal, path, expanded, l)

        if (path[-1] == goal):
            return
        
        path.pop()


def ids(grid, start, goal, expanded):
    rows, cols = len(grid), len(grid[0])

    for depth in range(heuristic(start, goal), rows * cols):
        path = [start]
        dlsBacktrack(grid, start, goal, path, expanded, depth)

        # return a path to goal if it's found
        if (path[-1] == goal):
            return path
    
    return None


def heuristic(a, b):
    # Manhattan distance as a heuristic (suitable for 4-directional movement)
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) # Manhattan = |dx| + |dy|


def aStar(grid, start, goal, expanded):
    # initialize variables
    # note: the grid indexes start from 1
    rows, cols = len(grid), len(grid[0])

    # having a list act as an heap priority queue
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(start, goal), 0, start, [start])) 
    
    # main process
    while open_list:
        # take information of current node and check if it was expanded
        f, g, expanding_node, path = heapq.heappop(open_list)
        if expanding_node in expanded:
            continue
        expanded.add(expanding_node)
        
        # if the current node was not expanded, check if it is goal
        # (late stop)
        if (expanding_node == goal):
            return path
        
        i, j = expanding_node
        for di, dj in DIRECTIONS:
            ni, nj = i + di, j + dj
            neighbor = (ni, nj)

            if (0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] <= -1 and neighbor not in expanded):
                # update and add it without needing to update old status
                # because the which one has better priority will be taken first
                # and add into expanded
                new_g = g + 1  # Cost from current to neighbor (assumed to be 1)
                new_f = new_g + heuristic(neighbor, goal)
                new_path = path + [neighbor]
                heapq.heappush(open_list, (new_f, new_g, neighbor, new_path))
    
    return None  # no path found


def identifyDirection(path): 
    direction = (-path[0][0] + path[1][0], -path[0][1] + path[1][1])

    switcher = {
        (0, -1): "LEFT",
        (0, 1):  "RIGHT",
        (-1, 0): "UP",
        (1, 0):  "DOWN",
    }
    
    return switcher.get(direction, "Invalid")  # Default case 
