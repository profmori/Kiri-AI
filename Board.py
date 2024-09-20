import random
from copy import copy

from Card import special_card_list, basic_card_list


class Board:
    # Class for representing the board state
    def __init__(self, game_type, samurai_1, samurai_2, display_only=False):
        # Initialised with two samurai objects as well as whether it is a basic or advanced game
        self.samurai_1 = samurai_1
        self.samurai_2 = samurai_2
        # Store the samurai objects for later reference
        samurai_1.opponent = samurai_2
        samurai_2.opponent = samurai_1
        # Tell the samurai who their opponents are

        assigned_cards = random.sample(special_card_list, 2)
        # Choose two of the three special cards to assign to players

        samurai_1.hand = copy(basic_card_list) + copy([assigned_cards[0]])
        # Create samurai 1's hand with all the basic cards and the first of the special cards
        samurai_2.hand = copy(basic_card_list) + copy([assigned_cards[1]])
        # Create samurai 2's hand with all the basic cards and the second of the special cards

        if game_type == 'basic':
            # If it is a basic game with 5 spaces
            self.board_size = 5
            # Set the board size to 5
        elif game_type == 'advanced':
            # If it is an advanced game
            self.board_size = 7
            # Set the board size to 7
            if not display_only:
                # If the board is not being used for displaying for manual choice
                self.samurai_1.advanced_setup()
                self.samurai_2.advanced_setup()
                # Run the advanced setup from the samurai class
                # This will set the start position and starting stance

        self.log_string = ''
        # Create the human-readable log string
        self.turn = 0
        # Count the current turn of the battle

    def act_simultaneously(self):
        # Function to allow two samurai actions to be performed simultaneously
        self.log_string = self.samurai_1.perform_action(self.log_string, simultaneous=True)
        self.log_string = self.samurai_2.perform_action(self.log_string, simultaneous=True)
        # Perform actions as normal, ignoring opponent position & simultaneous factor

        while self.samurai_1.position > (self.board_size - self.samurai_2.position - 1):
            # If the samurai have tried to move past one another
            self.samurai_1.position -= 1
            self.samurai_2.position -= 1
            # Move both back one space and check again

        if (self.samurai_1.counter_attacking and self.samurai_2.attacking
                or self.samurai_2.counter_attacking and self.samurai_1.attacking):
            # If one character is attacking and the other is counter attacking
            self.samurai_1.attacking = not self.samurai_1.attacking
            self.samurai_2.attacking = not self.samurai_2.attacking
            # Invert the attack variables so the counter attacking samurai deals damage

    def display_board(self, view=1):
        # Function to show the board, by default from samurai 1's perspective
        board_spaces = [['', ''] for _ in range(self.board_size)]
        # Hold the values in spaces left & right of the centre line

        close_samurai = self.__getattribute__(f'samurai_{view}')
        # Get the samurai which should be displayed at the bottom of the view
        far_samurai = self.__getattribute__(f'samurai_{3 - view}')
        # Get the samurai which should be displayed at the top of the view

        colour_dict = {
            2: '\033[32m',  # Green
            1: '\033[31m',  # Red
            0: ''  # No colour change / Black
        }
        # Dictionary to store text colours based on health value

        close_text = f'{close_samurai.player} ({close_samurai.stance})'
        far_text = f'{far_samurai.player} ({far_samurai.stance})'
        # Get the length of the text being entered on both sides in order to correctly align the board

        board_spaces[self.board_size - 1 - close_samurai.position][
            1] = f'{colour_dict[close_samurai.health]}{close_text}'
        # Set index backwards from the last space with the player's name and stance

        board_spaces[far_samurai.position][0] = f'{colour_dict[far_samurai.health]}{far_text}'
        # Set index forward from the first with the opponent's name and stance

        for position in board_spaces:
            # Iterate through the board spaces
            print(f'{position[0]: >{len(far_text)}}\033[0m|{position[1]: <{len(close_text)}}\033[0m')
            # Print the values in each position, spaced out so everything aligns down the middle
            # Uses the '\033[0m|' code to reset the colour of the text after each section

    def run_game(self):
        # Function to run the game all the way through

        while min(self.samurai_1.health, self.samurai_2.health) > 0:
            # Runs until someone dies
            self.turn += 1
            # Increment the turns by 1
            self.run_turn()
            # Run the turn

        if self.samurai_1.health == 0:
            winner = self.samurai_2
        else:
            winner = self.samurai_1
        # Set the winner based on which samuari has 0 health

        if self.samurai_1.controller.controller_name == 'ManualController' or self.samurai_2.controller.controller_name == 'ManualController':
            self.display_board()
        # If either samurai has a manual controller, display the final state of the board

        loser_list = [self.samurai_1, self.samurai_2]
        loser_list.remove(winner)
        loser = loser_list[0]
        # Set the loser as the other samurai who is not the winner

        winner.update_win()
        loser.update_win()
        # Update the winner and loser input vectors to have the correct reward (as denoted by the controller)
        # Win detection from agent health remaining so no input is required for which is which

        return {'winner': winner.controller.controller_name, 'winner_vectors': winner.input_vectors,
                'loser': loser.controller.controller_name, 'loser_vectors': loser.input_vectors,
                'readable_log': self.log_string}
        # Return a dictionary of the winning controller, losing controller, and their input vectors for network training
        # Also returns the human-readable action log

    def run_turn(self):
        # Function to run a single 2 card turn
        self.samurai_1.choose_actions()
        # Ask samurai 1 to choose an action
        self.samurai_2.choose_actions()
        # Ask samurai 2 to choose an action
        # These should be run simultaneously eventually (ray?)

        for action_num in range(2):
            stage = ['a', 'b'][action_num]
            self.log_string += f'Turn {self.turn}{stage}\n'
            # Iterate through both actions being played
            s1_action = copy(self.samurai_1.played_actions[0])
            s2_action = copy(self.samurai_2.played_actions[0])
            # Get the relevant action for this stage of the turn
            priorities = {s1_action.priority, s2_action.priority}
            # Make a set of the priorities - removes duplicates & orders the values
            for curr_priority in priorities:
                # Run through the priorities

                s1_act = s1_action.priority == curr_priority
                s2_act = s2_action.priority == curr_priority
                # Check if the samurai is set to act in the current priority bracket

                if s1_act != s2_act:
                    # If there is only one of the two samurai acting
                    if s1_act:
                        # If it is samurai 1
                        self.log_string = self.samurai_1.perform_action(self.log_string)
                        # Perform the action of samurai 1
                    else:
                        # If it is samurai 2
                        self.log_string = self.samurai_2.perform_action(self.log_string)
                        # Perform the action of samurai 2
                else:
                    # If the two actions are the same priority (which can only be both true)
                    if self.samurai_1.stance == self.samurai_2.stance or curr_priority > 3:
                        # If the samurai are in the same stance, or combat is occurring
                        self.act_simultaneously()
                        # Enact their moves simultaneously
                    elif self.samurai_1.stance == 'heaven':
                        # If samurai 1 is in heaven stance, they act first
                        self.log_string = self.samurai_1.perform_action(self.log_string)
                        self.log_string = self.samurai_2.perform_action(self.log_string)
                    else:
                        # Otherwise samurai 2 is in heaven stance, and they act first
                        self.log_string = self.samurai_2.perform_action(self.log_string)
                        self.log_string = self.samurai_1.perform_action(self.log_string)

            if self.samurai_1.attacking ^ self.samurai_2.attacking:
                # If only one of the samurai attacked this turn (logical XOR)
                self.samurai_1.update_reward()
                self.samurai_2.update_reward()
                # Generate the correct reward for this turn for both samurai, and put it in the dictionary
                self.samurai_1.health -= self.samurai_2.attacking
                self.samurai_2.health -= self.samurai_1.attacking
                # Both samurai take damage depending on whether their opponent attacked
                # This implicitly translates the booleans into integers

            self.samurai_1.attacking, self.samurai_2.attacking = False, False
            # Reset the attack flag on both samurai
            self.samurai_1.counter_attacking, self.samurai_2.counter_attacking = False, False
            # Get rid of the counter attacking variable after checking so a samurai doesn't become invincible

            if min(self.samurai_1.health, self.samurai_2.health) <= 0:
                # If someone is dead after the first card has been resolved
                break
                # End the turn (and the game)
