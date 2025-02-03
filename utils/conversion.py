import numpy as np

def cont_to_disc(x, y, rows, cols):
    """
    Converte le coordinate continue (x, y) in coordinate discrete (i, j)
    in base al sistema di coordinate usato nel maze.
    """
    j = int(np.round(x + (cols / 2 - 0.5)))
    i = int(np.round((rows - 1) / 2 - y))
    return (i, j)

def disc_to_cont(i, j, rows, cols):
    """
    Converte le coordinate discrete (i, j) nel centro della cella in coordinate continue (x, y).
    L'ipotesi è che la cella (i, j) abbia centro:
      x = j - (cols/2 - 0.5)
      y = (rows-1)/2 - i
    """
    x = j - (cols / 2 - 0.5)
    y = (rows - 1) / 2 - i
    return np.array([x, y])
