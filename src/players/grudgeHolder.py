from players.base_player import BasePlayer


class GrudgeHolder(BasePlayer):
    """
    A player that cooperates until the opponent defects.
    Once defected against, it holds a grudge and defects for a fixed number
    of rounds, then offers one chance for forgiveness by cooperating.
    If the opponent defects during the forgiveness round, the grudge continues.
    """
    def __init__(self, grudge_duration=5):
        super().__init__()
        self.grudge_duration = grudge_duration
        self.holding_grudge = False
        self.grudge_counter = 0

    def initial_action(self):
        action = "cooperate"
        self.past_actions.append(action)
        return action

    def get_action(self, opponents_history: list):
        if not opponents_history:
            return self.initial_action()

        last_opponent_action = opponents_history[-1]
        my_action = "cooperate" # Default optimistic action

        if self.holding_grudge:
            self.grudge_counter += 1
            if self.grudge_counter <= self.grudge_duration:
                # Still holding the grudge
                my_action = "defect"
            else:
                # Offer forgiveness
                my_action = "cooperate"
                # We will check opponent's response in the *next* round
        else:
            # Not holding a grudge currently
            if last_opponent_action == "defect":
                # Opponent just defected! Start the grudge.
                self.holding_grudge = True
                self.grudge_counter = 1 # Start counting grudge rounds
                my_action = "defect"
            else:
                # Opponent cooperated, so we cooperate too.
                my_action = "cooperate"

        # Check if we just offered forgiveness and how the opponent responded
        if self.grudge_counter == self.grudge_duration + 1: # We just played the forgiveness COOPERATE
            if last_opponent_action == "defect":
                # They defected on our forgiveness! Grudge continues.
                self.grudge_counter = 1 # Reset counter for another cycle
                my_action = "defect" # Defect immediately
            else:
                # They cooperated! Forgiveness accepted. Drop the grudge.
                self.holding_grudge = False
                self.grudge_counter = 0
                my_action = "cooperate" # Cooperate next round

        self.past_actions.append(my_action)
        return my_action

    def reset(self):
        super().reset()
        self.holding_grudge = False
        self.grudge_counter = 0