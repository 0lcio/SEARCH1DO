import heapq

def dijkstra(maze, start, goal, rows, cols):
    """
    Esegue l'algoritmo di Dijkstra sul labirinto 'maze'.
    start e goal sono tuple (i, j).
    Restituisce una lista di celle [(i, j), ...] rappresentante il percorso più economico.
    """
    # La coda contiene tuple: (costo, cella, parent)
    open_list = []
    heapq.heappush(open_list, (0, start, None))
    
    came_from = {}
    cost_so_far = {start: 0}
    
    while open_list:
        cost, current, parent = heapq.heappop(open_list)
        
        # Se il nodo è già stato visitato, lo saltiamo
        if current in came_from:
            continue
        
        came_from[current] = parent
        
        if current == goal:
            break
        
        # Espandi i vicini (movimenti: su, giù, sinistra, destra)
        for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + d[0], current[1] + d[1])
            if (0 <= neighbor[0] < rows) and (0 <= neighbor[1] < cols) and (maze[neighbor[0]][neighbor[1]] == 0):
                new_cost = cost_so_far[current] + 1  # costo 1 per ogni mossa
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(open_list, (new_cost, neighbor, current))
    
    # Se il goal non è stato raggiunto
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
