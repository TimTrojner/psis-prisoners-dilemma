class BasePlayer(object):
    def __init__(self):
        self.past_actions = []
        self.num_games = 0

    def get_action_history(self):
        return self.past_actions

    def initial_action(self):
        pass

    def reset(self):
        self.past_actions = []
        self.num_games = 0

    def get_action(self, opponents_history: list):
        """General function to return an action (cooperate or defect)
        given a list of the opponents actions, if the list of opponents actions is empty then
        use <initial_action()> for the action to choose in the start of the game

        :param list opponents_history: List of actions the opponent took while playing the game.
        :returns str action: string action "cooperate" or "defect".
        :rtype: bool
        """

        # initial move in the game
        if len(opponents_history) == 0:
            action = self.initial_action()

        else:
            # get the last action of the opponent and choose the action by the player
            pass

        self.past_actions.append(action)
        self.num_games += 1

        return action