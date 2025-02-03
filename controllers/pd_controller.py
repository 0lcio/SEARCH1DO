import numpy as np

class PDController:
    def __init__(self, Kp=1.0, Kd=0.2, threshold=0.3, dt=0.01):
        self.Kp = Kp
        self.Kd = Kd
        self.threshold = threshold
        self.dt = dt
        self.prev_error = np.zeros(2)
    
    def compute_action(self, target, current_pos):
        """
        Calcola l'azione da compiere basata sulla posizione corrente e il target.
        Restituisce un vettore di forza clippato nell'intervallo [-1, 1].
        """
        error = target - current_pos
        distance = np.linalg.norm(error)
        
        if distance < self.threshold:
            return None  # Il waypoint è stato raggiunto
        
        d_error = (error - self.prev_error) / self.dt
        self.prev_error = error
        action = self.Kp * error + self.Kd * d_error
        return np.clip(action, -1.0, 1.0)
