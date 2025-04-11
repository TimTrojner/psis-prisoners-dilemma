from players.base_player import BasePlayer

class NICE_GUY(BasePlayer):
    def initial_action(self):
        # Always start by defecting
        return "cooperate"
    
    def get_action(self, opponents_history: list):
        # Always cooperate regardless of opponent's history
        action = "cooperate"
        
        self.past_actions.append(action)
        self.num_games += 1
        return action
