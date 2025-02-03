import heapq

def heuristic(a, b):
    """Usa la distanza di Manhattan come euristica."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(maze, start, goal, rows, cols):
    """
    Esegue la ricerca A* sul labirinto 'maze' (lista di liste).
    start e goal sono tuple (i, j).
    Restituisce una lista di celle [(i, j), ...] rappresentante il percorso.
    """
    open_list = []
    heapq.heappush(open_list, (heuristic(start, goal), 0, start, None))
    
    came_from = {}  # Per ricostruire il percorso
    cost_so_far = {start: 0}
    
    while open_list:
        f, cost, current, parent = heapq.heappop(open_list)
        
        if current in came_from:
            continue  # Questa cella è già stata elaborata
        
        came_from[current] = parent
        
        if current == goal:
            break
        
        # Movimenti: su, giù, sinistra, destra
        for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + d[0], current[1] + d[1])
            if (0 <= neighbor[0] < rows) and (0 <= neighbor[1] < cols) and (maze[neighbor[0]][neighbor[1]] == 0):
                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (priority, new_cost, neighbor, current))
    
    if goal not in came_from:
        return None

    # Ricostruzione del percorso
    current = goal
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path
