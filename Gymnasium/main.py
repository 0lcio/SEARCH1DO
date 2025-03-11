import time
import numpy as np
import argparse
from envs.maze import create_maze_env, get_maze, get_maze_dimensions
from utils.conversion import cont_to_disc, disc_to_cont, optimize_path
from algorithms.astar import astar
from algorithms.dijkstra import dijkstra
from algorithms.uniform_cost import uniform_cost_search
from controllers.pd_controller import PDController
import config

def main():
    # Parsing degli argomenti da riga di comando
    parser = argparse.ArgumentParser(description='Run maze simulation with different pathfinding algorithms')
    parser.add_argument('--algorithm', '-a', 
                        choices=['astar', 'dijkstra', 'uniform_cost'], 
                        default='astar',
                        help='Pathfinding algorithm to use (default: astar)')
    args = parser.parse_args()

    # Crea l'environment e recupera l'osservazione iniziale
    env, observation, _ = create_maze_env(
        render_mode=config.ENV_RENDER_MODE,
        width=config.ENV_WIDTH,
        height=config.ENV_HEIGHT
    )
    
    # Recupera la mappa e le sue dimensioni
    if args.algorithm == 'uniform_cost':
        maze = get_maze(custom_terrain=True)
    else: 
        maze = get_maze(custom_terrain=False)
    rows, cols = get_maze_dimensions(maze)

    # Ottieni le posizioni continue dall'osservazione
    agent_cont = observation["observation"][:2]
    goal_cont = observation["desired_goal"]
    
    # Converte le coordinate in posizione discreta
    agent_disc = cont_to_disc(agent_cont[0], agent_cont[1], rows, cols)
    goal_disc = cont_to_disc(goal_cont[0], goal_cont[1], rows, cols)
    
    print("Cella agente (i, j):", agent_disc)
    print("Cella goal (i, j):", goal_disc)
    
    # Calcola il percorso con A*
    start_time = time.time()
    path_astar, expanded_astar = astar(maze, agent_disc, goal_disc, rows, cols)
    end_time = time.time()
    print("A* runtime:", end_time - start_time)
    print("A* nodes expanded:", expanded_astar)

    # Calcola il percorso con Uniform Cost
    start_time = time.time()
    path_uniform, expanded_uniform = uniform_cost_search(maze, agent_disc, goal_disc, rows, cols)
    end_time = time.time()
    print("Cost_Uniform runtime:", end_time - start_time)
    print("Cost_Uniform nodes expanded:", expanded_uniform)

    # Calcola il percorso con Dijkstra
    start_time = time.time()
    path_dijkstra, expanded_dijkstra = dijkstra(maze, agent_disc, goal_disc, rows, cols)
    end_time = time.time()
    print("Dijkstra runtime:", end_time - start_time)
    print("Dijkstra nodes expanded:", expanded_dijkstra)
    
    # Se non è stato trovato alcun percorso, termina l'esecuzione
    if path_astar is None and args.algorithm == 'astar':
        print("Nessun percorso trovato!")
        env.close()
        return
    elif path_dijkstra is None and args.algorithm == 'dijkstra':
        print("Nessun percorso trovato!")
        env.close()
        return
    elif path_uniform is None and args.algorithm == 'uniform_cost':
        print("Nessun percorso trovato!")
        env.close()
        return

    # Converte il percorso in coordinate continue
    if args.algorithm == 'astar':
        # Ottimizza il percorso
        optimized_path = optimize_path(path_astar)
    elif args.algorithm == 'dijkstra':
        optimized_path = optimize_path(path_dijkstra)
    elif args.algorithm == 'uniform_cost':
        optimized_path = optimize_path(path_uniform)

    continuous_path = [disc_to_cont(i, j, rows, cols) for (i, j) in optimized_path]
    # Per un movimento più preciso, usiamo i waypoint intermedi e il goal osservato
    intermediate_waypoints = continuous_path[:-1]
    final_goal = goal_cont  # goal osservato (che tiene conto del noise)
    all_waypoints = intermediate_waypoints + [final_goal]
    
    # Inizializza il controllore PD
    controller = PDController(Kp=config.KP, Kd=config.KD, threshold=config.THRESHOLD, dt=config.DT)
    
    current_waypoint_idx = 0
    max_steps = 200000
    step = 0
    
    while step < max_steps:
        step += 1
        # Aggiorna lo stato (usiamo un'azione nulla per avere l'osservazione aggiornata)
        observation, reward, terminated, truncated, _ = env.step(np.array([0.0, 0.0]))
        current_pos = observation["observation"][:2]
        
        if current_waypoint_idx >= len(all_waypoints):
            print("Percorso completato!")
            break
        
        target = all_waypoints[current_waypoint_idx]
        error = target - current_pos
        distance = np.linalg.norm(error)
        
        if distance < config.THRESHOLD:
            current_waypoint_idx += 1
            continue
        
        action = controller.compute_action(target, current_pos)
        if action is None:
            current_waypoint_idx += 1
            continue
        
        observation, reward, terminated, truncated, _ = env.step(action)
        if terminated:
            observation, _ = env.reset()
    
    env.close()

if __name__ == '__main__':
    main()
