from random import random


class GenericController:
    def __init__(self):
        self.output_vector = [0] * 20
        # These are the likelihoods of each action being chosen
        # There are 8 cards and 2 double-sided cards, so 10 actions

    def select_actions(self, input_vector):
        # Returns a list of 20 values between 0 & 1
        pass

    def normalise(self):
        # Function to normalise each set of 10 actions
        for action in range(2):
            # Iterate through each half of the list
            div_sum = sum(self.output_vector[action * 10:(action + 1) * 10])
            # Get the sum of that set of 10 elements
            for value in range(10):
                # Iterate through the elements
                self.output_vector[action * 10 + value] /= div_sum
                # Normalise each element


class RandomController(GenericController):
    def select_actions(self, input_vector):
        self.output_vector = [random() for _ in range(20)]
        # Return 20 random floats
        self.normalise()
        # Normalise the output vector
        return self.output_vector
        # Return the normalised output vector
