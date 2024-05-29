from copy import copy


class Board:
    # Class for representing the board state
    def __init__(self, game_type, samurai_1, samurai_2):
        # Initialised with two samurai objects as well as whether it is a basic or advanced game
        self.samurai_1 = samurai_1
        self.samurai_2 = samurai_2
        # Store the samurai objects for later reference

        if game_type == 'basic':
            # If it is a basic game with 5 spaces
            self.board_size = 5
            # Set the board size to 5
        elif game_type == 'advanced':
            # If it is an advanced game
            self.board_size = 7
            # Set the board size to 7
            self.samurai_1.advanced_setup()
            self.samurai_2.advanced_setup()
            # Run the advanced setup from the samurai class
            # This will set the start position and starting stance

        longest_player_name = max(len(self.samurai_1.player), len(self.samurai_2.player))
        # Get the length of the longest player name

        self.display_board()
        # Show the board

    def run_turn(self):
        # Function to run a single 2 card turn
        self.samurai_1.choose_actions()
        self.samurai_2.choose_actions()

        for action_num in range(2):
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
                        self.samurai_1.perform_action(self.samurai_2, self.board_size)
                        # Perform the action of samurai 1
                    else:
                        # If it is samurai 2
                        self.samurai_2.perform_action(self.samurai_1, self.board_size)
                        # Perform the action of samurai 2
                else:
                    # If the two actions are the same priority (which can only be both true)
                    if self.samurai_1.stance == self.samurai_2.stance or curr_priority > 3:
                        # If the samurai are in the same stance, or combat is ocurring
                        self.act_simultaneously()
                        # Enact their moves simultaneously
                    elif self.samurai_1.stance == 'heaven':
                        # If samurai 1 is in heaven stance, they act first
                        self.samurai_1.perform_action(self.samurai_2, self.board_size)
                        self.samurai_2.perform_action(self.samurai_1, self.board_size)
                    else:
                        # Otherwise samurai 2 is in heaven stance, and they act first
                        self.samurai_2.perform_action(self.samurai_1, self.board_size)
                        self.samurai_1.perform_action(self.samurai_1, self.board_size)

            if self.samurai_1.attacking ^ self.samurai_2.attacking:
                # If only one of the samurai attacked this turn (logical XOR)
                self.samurai_1.health -= self.samurai_2.attacking
                self.samurai_2.health -= self.samurai_1.attacking
                # Both samurai take damage depending on whether their opponent attacked
                # This implicitly translates the booleans into integers
            self.samurai_1.attacking, self.samurai_2.attacking = False, False
            # Reset the attack flag on both samurai
            self.samurai_1.counter_attacking, self.samurai_2.counter_attacking = False, False
            # Get rid of the counter attacking variable after checking so a samurai doesn't become invincible
            self.display_board()
            # Show the board after each action

            if min(self.samurai_1.health, self.samurai_2.health) <= 0:
                # If someone is dead after the first card played
                break
                # End the turn (and the game)

    def act_simultaneously(self):
        # Function to allow two samurai actions to be performed simultaneously
        self.samurai_1.perform_action(self.samurai_2, self.board_size, True)
        self.samurai_2.perform_action(self.samurai_1, self.board_size, True)
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
            1: '\033[34m',  # Blue
            0: '\033[31m'   # Red
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
