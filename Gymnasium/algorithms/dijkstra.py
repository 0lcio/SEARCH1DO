import heapq
import config

def dijkstra(maze, start, goal, rows, cols):

    open_list = []
    heapq.heappush(open_list, (0, start, None))
    
    came_from = {}
    cost_so_far = {start: 0}
    nodes_expanded = 0

    while open_list:
        cost, current, parent = heapq.heappop(open_list)
        
        if current in came_from:
            continue
        
        came_from[current] = parent
        nodes_expanded += 1
        
        if current == goal:
            break
        
        for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + d[0], current[1] + d[1])
            if (0 <= neighbor[0] < rows) and (0 <= neighbor[1] < cols) and \
               (maze[neighbor[0]][neighbor[1]] in (0, config.R, config.G, config.C)):
                new_cost = cost_so_far[current] + 1  # costo costante per spostamento
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(open_list, (new_cost, neighbor, current))
    
    if goal not in came_from:
        return None, nodes_expanded

    current = goal
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path, nodes_expanded