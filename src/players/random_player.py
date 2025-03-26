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