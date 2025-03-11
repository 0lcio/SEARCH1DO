import heapq
import config

def uniform_cost_search(maze, start, goal, rows, cols):
    
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
            if (0 <= neighbor[0] < rows) and (0 <= neighbor[1] < cols):
                cell_type = maze[neighbor[0]][neighbor[1]]
                
                # Ignora le celle non attraversabili
                if cell_type == 1:
                    continue
                
                # Determina il terreno e il costo associato
                if cell_type == 0:
                    terrain_cost = config.NORMAL_COST
                elif cell_type == config.W:
                    terrain_cost = config.WATER_COST
                elif cell_type == config.S:
                    terrain_cost = config.SAND_COST
                elif cell_type == config.RO:
                    terrain_cost = config.ROAD_COST
                elif cell_type in (config.R, config.G):
                    terrain_cost = config.NORMAL_COST
                else:
                    terrain_cost = config.NORMAL_COST
                
                new_cost = cost_so_far[current] + terrain_cost
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
