from players.base_player import BasePlayer
import numpy as np

class JOSS(BasePlayer):
    def __init__(self, defection_probability=0.1):
        super().__init__()
        self.defection_probability = defection_probability
        
    def initial_action(self):
        # Start by cooperating (like Tit-for-Tat)
        return "cooperate"
    
    def get_action(self, opponents_history: list):
        if len(opponents_history) == 0:
            action = self.initial_action()
        else:
            action = opponents_history[-1]
            if action == "cooperate" and np.random.random() < self.defection_probability:
                action = "defect"
        
        self.past_actions.append(action)
        self.num_games += 1
        return action
