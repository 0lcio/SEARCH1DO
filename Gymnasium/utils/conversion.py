import numpy as np

def cont_to_disc(x, y, rows, cols):

    #Converte le coordinate continue (x, y) in coordinate discrete (i, j)

    j = int(np.round(x + (cols / 2 - 0.5)))
    i = int(np.round((rows - 1) / 2 - y))
    return (i, j)

def disc_to_cont(i, j, rows, cols):

    #Converte le coordinate discrete (i, j) nel centro della cella in coordinate continue (x, y).

    x = j - (cols / 2 - 0.5)
    y = (rows - 1) / 2 - i
    return np.array([x, y])

def optimize_path(path):

    #Ottimizza un percorso mantenendo solo i punti in cui cambia la direzione.

    if not path or len(path) <= 2:
        return path  # Keep paths with 2 or fewer points unchanged
    
    optimized_path = [path[0]]  # Always include start point
    
    for i in range(1, len(path) - 1):
        prev = path[i-1]
        curr = path[i]
        next_pt = path[i+1]
        
        # Calcola le direzioni tra i punti
        prev_dir = (curr[0] - prev[0], curr[1] - prev[1])
        next_dir = (next_pt[0] - curr[0], next_pt[1] - curr[1])
        
        # Se la direzione cambia, aggiungi il punto al percorso ottimizzato
        if prev_dir != next_dir:
            optimized_path.append(curr)
    
    optimized_path.append(path[-1])  # Aggiungi l'ultimo punto
    
    return optimized_path
