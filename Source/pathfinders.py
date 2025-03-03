import heapq

# this will hold the pathfinding algorithms like bfs, dfs, a*, etc.
def dfs_recursive_ordered(grid, current_i, current_j, visited, goal_i,goal_j,expanded): 
    rows, cols = len(grid), len(grid[0])
    
    # Check boundaries and if already visited
    if not (0 <= current_i < rows and 0 <= current_j < cols ) or (current_i, current_j) in visited:
        return None
    visited.append((current_i, current_j))
    # if current = finish
    if current_i == goal_i and current_j == goal_j:
        visited.pop()
        return [(current_i,current_j)]
    
    # Directions: left, right, up, down
    directions = [(0, -1), (0, 1),(-1, 0), (1, 0)]
    # for neighbors of current
    for di, dj in directions:
        ni = di + current_i
        nj = dj + current_j
        if 0 <= nj < cols and 0 <= ni < rows and grid[ni][nj] != 0:
           
            if ((ni,nj)) not in visited:
                expanded.append((ni,nj))
                result = dfs_recursive_ordered(grid, ni, nj, visited, goal_i,goal_j,expanded)
                if result is not None: 
                    return [(current_i, current_j)] + result
    return None

def heuristic(a, b):
    # Manhattan distance as a heuristic (suitable for 4-directional movement)
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) # Manhattan = |dx| + |dy|

def a_star(grid, start, goal, expanded):
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
            if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == 1 and neighbor not in expanded:
                #update and add it without needing to update old status
                #because the which one has better priority will be taken first
                #and add into expanded
                new_g = g + 1  # Cost from current to neighbor (assumed to be 1)
                new_f = new_g + heuristic(neighbor, goal)
                new_path = path + [neighbor]
                heapq.heappush(open_list, (new_f, new_g, neighbor, new_path))
    
    return "NONE"  # No path found
def find_direction(path): 

    direction = (-path[0][0] + path[1][0], -path[0][1] + path[1][1])

    return switch_case(direction)

def switch_case(direction):
    
    switcher = {
        (0, -1): "LEFT",
        (0, 1): "RIGHT",
        (-1, 0): "UP",
        (1, 0) : "DOWN"
    }
    return switcher.get(direction, "Invalid")  # Default case

if __name__ == '__main__':
    print("This is a module. Not meant to be run standalone.")