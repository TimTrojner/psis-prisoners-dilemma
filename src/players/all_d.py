from players.base_player import BasePlayer

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
