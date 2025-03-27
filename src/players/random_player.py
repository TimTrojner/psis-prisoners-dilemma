import numpy as np
from players.base_player import BasePlayer

class Random(BasePlayer):
    def initial_action(self):
        return np.random.choice(["cooperate", "defect"])

    def get_action(self, opponents_history: list):

        if len(opponents_history) == 0:
            action = self.initial_action()

        else:
            action = np.random.choice(["cooperate", "defect"])

        self.past_actions.append(action)
        self.num_games += 1
        return action
    
class TIT_FOR_TAT(BasePlayer):
    def initial_action(self):
        # Start by cooperating (classic TitForTat)
        return "cooperate"
    
    def get_action(self, opponents_history: list):
        if len(opponents_history) == 0:
            action = self.initial_action()
        else:
            # Copy the opponent's last move
            action = opponents_history[-1]
        
        self.past_actions.append(action)
        self.num_games += 1
        return action

class ALL_D(BasePlayer):
    def initial_action(self):
        # Always start by defecting
        return "defect"
    
    def get_action(self, opponents_history: list):
        # Always defect regardless of opponent's history
        action = "defect"
        
        self.past_actions.append(action)
        self.num_games += 1
        return action

class Tester(BasePlayer):
    def initial_action(self):
        # Start with defection to test the opponent
        return "defect"
    
    def get_action(self, opponents_history: list):
        if len(opponents_history) == 0:
            action = self.initial_action()
        elif len(opponents_history) == 1:
            # Second move: cooperate to see how opponent responds after being defected against
            action = "cooperate"
        else:
            # If opponent retaliated against our initial defection, play tit-for-tat
            if opponents_history[1] == "defect":
                action = opponents_history[-1]  # Copy opponent's last move
            else:
                # If opponent forgave our defection, exploit them by defecting
                action = "defect"
        
        self.past_actions.append(action)
        self.num_games += 1
        return action

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
            # If opponent defected, always defect
            if opponents_history[-1] == "defect":
                action = "defect"
            else:
                # Opponent cooperated
                # With probability defection_probability, defect anyway
                if np.random.random() < self.defection_probability:
                    action = "defect"
                else:
                    # Otherwise cooperate (follow Tit-for-Tat)
                    action = "cooperate"
        
        self.past_actions.append(action)
        self.num_games += 1
        return action