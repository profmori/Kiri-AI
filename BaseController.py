from copy import copy
from random import choices

from Card import all_action_list


class BaseController:
    # Base class for all controllers to inherit from
    # Includes useful functions that might be needed for general manipulation
    # Also specifies standard formats for input and output of data
    def __init__(self):
        self.output_vector = [0] * 20
        # This is the output of the controller - 20 values between 0 & 1
        # There are 8 cards and 2 double-sided cards, so 10 actions
        self.controller_name = self.__class__.__name__
        # Get the name of the class as the controller name
        # This can be overwritten if you want a more descritive name

    def choose_setup(self, special_cards):
        # Takes an input of 3 values of 0 or 1 (which special card the player has)
        # Returns 2 values for advanced setup
        # [0] position of the samurai - 0,1 or 2
        # [1] stance of the samurai - 'heaven' or 'earth'
        # If you input your vector into super().choose_setup it will fix this from floats (0 -> 'heaven' 1 -> 'earth')
        # This will also map a random value from 0 -> 1 to the start position 0 -> 0, 0.5 -> 1, 1 -> 2
        if len(special_cards) == 2 and type(special_cards) is list:
            # If a list of exactly two "special cards" were input (a super call)
            if round(special_cards[1]) == 0:
                # If the second entry is closer to zero than one
                stance = 'heaven'
                # Set the stance to heaven
            else:
                # If the second entry is closer to one than zero (or exceeds the 0 - 1 range)
                stance = 'earth'
                # Set the stance to earth

            return [round(special_cards[0] * 2), stance]
            # Returns the rounded starting position and the chosen stance
        else:
            # If a different input has been given for 'special_cards'
            raise Exception('GenericController.choose_setup has been called with incorrect input')
            # Raise an exception with the noted error message

    def normalise(self):
        # Function to normalise each set of 10 actions
        # Not currently used but could be useful in the future
        for action in range(2):
            # Iterate through each half of the list
            div_sum = sum(self.output_vector[action * 10:(action + 1) * 10])
            # Get the sum of that set of 10 elements
            for value in range(10):
                # Iterate through the elements
                self.output_vector[action * 10 + value] /= div_sum
                # Normalise each element

    def rank_actions_max(self):
        # Ranks the actions based on the absolute output of the controller - deterministic
        card_1_output = self.output_vector[0:10]
        # The controller output for the first card selected
        card_1_ranks = [card_1_output.index(card) for card in sorted(card_1_output, reverse=True)]
        # The rank of each card being played first, sorted from highest to lowest
        card_2_output = self.output_vector[10:20]
        # The controller output for the second card selected
        card_2_ranks = [card_2_output.index(card) for card in sorted(card_2_output, reverse=True)]
        # The rank of each card being played second, sorted from highest to lowest

        ranked_vector = [None] * 20
        # The vector output of 20 actions, ranked from highest to lowest

        for rank in range(10):
            # Iterates through each set of 10 actions
            ranked_vector[rank] = copy(all_action_list[card_1_ranks[rank]])
            # Adds the top ranked card to be played first to the ranked vector
            ranked_vector[rank + 10] = copy(all_action_list[card_2_ranks[rank]])
            # Adds the top ranked card to be played second to the ranked vector

        return ranked_vector
        # Returns the ranked vector

    def rank_actions_weighted(self):
        # Ranks the actions using the output of the controller as random weights - allows exploration
        card_1_output = self.output_vector[0:10]
        # The controller output for the first card selected
        card_2_output = self.output_vector[10:20]
        # The controller output for the second card selected

        ranked_vector = [None] * 20
        # The vector output of 20 actions, ranked from highest to lowest

        for rank in range(10):
            # Iterates through each set of 10 actions
            action_1 = choices(all_action_list, weights=card_1_output)[0]
            # Choose a random action for card 1, weighted by the output of the neural network
            ranked_vector[rank] = copy(action_1)
            # Adds the top ranked card to be played first to the ranked vector
            card_1_output[all_action_list.index(action_1)] = 0
            # Zero out that action from the input to prevent it being chosen again

            action_2 = choices(all_action_list, weights=card_2_output)[0]
            # Choose a random action for card 2, weighted by the output of the neural network
            ranked_vector[rank + 10] = copy(action_2)
            # Adds the top ranked card to be played second to the ranked vector
            card_2_output[all_action_list.index(action_2)] = 0
            # Zero out that action from the input to prevent it being chosen again

        return ranked_vector
        # Returns the ranked vector

    def select_actions(self, input_vector):
        # Returns a list of 20 values between 0 & 1 (the output vector variable above)
        # [0-9] Outputs for the first card to be played
        # [10-19] Outputs for the second card to be played
        pass
