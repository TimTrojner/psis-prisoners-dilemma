from players.base_player import BasePlayer

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