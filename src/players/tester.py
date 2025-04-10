from players.base_player import BasePlayer

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
