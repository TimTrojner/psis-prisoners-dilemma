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