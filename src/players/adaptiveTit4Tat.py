from players.base_player import BasePlayer

class AdaptiveTitForTat(BasePlayer):
    def __init__(self, cooperation_threshold=5):
        super().__init__()
        self.cooperation_threshold = cooperation_threshold
        self.consecutive_cooperations = 0
        self.exploit_mode = False

    def initial_action(self):
        return "cooperate"

    def get_action(self, opponents_history: list):
        if not opponents_history:
            action = self.initial_action()
        else:
            last_opponent_action = opponents_history[-1]

            if last_opponent_action == "cooperate":
                self.consecutive_cooperations += 1
            else:
                self.consecutive_cooperations = 0
                self.exploit_mode = False  # Reset if opponent retaliates

            if self.exploit_mode:
                action = "defect"
            else:
                if self.consecutive_cooperations >= self.cooperation_threshold:
                    # Test by defecting once
                    action = "defect"
                    self.exploit_mode = True  # Enter exploit mode if opponent continues cooperating
                else:
                    # Mimic Tit-for-Tat
                    action = last_opponent_action

        self.past_actions.append(action)
        return action

    def reset(self):
        super().reset()
        self.consecutive_cooperations = 0
        self.exploit_mode = False