class Action:
    # Class for holding the different actions and logic for playing the game
    def __init__(self, name, move_dist=0, strike_min=-1, strike_range=0, end_stance='same', begin_stance='any',
                 single_use=False):
        # Initialised with all default values to reduce overhead
        self.name = name
        # Name of the action
        self.movement = move_dist
        # How much the card moves you
        self.strike_min = strike_min
        # The close range of the strike
        self.strike_max = strike_min + strike_range
        # The far range of the strike, usually equal to the close range
        self.begin_stance = begin_stance
        # The required beginning stance for the action
        self.end_stance = end_stance
        # The forced end stance of the action
        self.single_use = single_use
        # Whether the card is one of the special single use actions

        # Determine the type of the action for prioritisation
        if abs(self.movement) == 1:
            # If the card moves you by 1 it has top priority
            self.priority = 1
        elif self.movement == 2:
            # If it moves you by 2 it is charge and has 2nd priority
            self.priority = 2
        elif self.end_stance == 'change':
            # If it is the change stance card it has third priority
            self.priority = 3
        else:
            # If it is an attack it will be resolved last & simultaneously
            self.priority = 4
