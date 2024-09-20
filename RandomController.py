from random import random

from BaseController import BaseController


class RandomController(BaseController):
    def select_actions(self, input_vector):
        self.output_vector = [random() for _ in range(20)]
        # Return 20 random floats
        return super().rank_actions_weighted()
        # Return the actions ranked by using the output vector as weights for selection

    def choose_setup(self, special_cards):
        chosen_cards = [random() for _ in range(2)]
        # Generates two random numbers between 0 and 1
        return super().choose_setup(chosen_cards)
        # Runs them through the parent class to get them in the right format

    def get_reward(self, agent):
        # Required to be implemented, but will never be used
        return round(random(), 2)
        # Return a random number just in case it would cause an error not to

    def modify_rewards(self, agent):
        # Required to be implemented, but will never be used
        return agent.input_vectors
        # Return the unmodified input vectors
