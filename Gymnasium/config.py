# Configurazioni globali

# Parametri per l'environment
ENV_RENDER_MODE = "human"
ENV_WIDTH = 1440
ENV_HEIGHT = 900
ENV_SEED = 1

# Parametri per il labirinto
RESET = R = "r"  # Posizione iniziale dell'agente
GOAL = G = "g"
COMBINED = C = "c"  # Posizione a scelta casuale tra R e G

# Parametri per il terreno (Uniform Cost)
NORMAL_COST = 1.0
WATER = W = "w"
WATER_COST = 5.0   
SAND = S = "s"
SAND_COST = 2.0
ROAD = RO = "ro"
ROAD_COST = 0.5    

# Parametri del controllore
KP = 1.0
KD = 0.2
THRESHOLD = 0.3
DT = 0.01
