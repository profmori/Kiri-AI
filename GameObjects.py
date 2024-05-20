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
        self.name_width = longest_player_name + 9
        # Centre the board correctly for the longest player name plus 9 characters
        # This centres everything for '|' + name + ' (heaven)' which is the longest printed string
        # This is probably only a temporary measure

        self.display_board()
        # Show the board

    def run_turn(self):
        # Function to run a single 2 card turn
        for action_num in range(2):
            # Iterate through both actions being played
            s1_action = self.samurai_1.played_actions[action_num]
            s2_action = self.samurai_2.played_actions[action_num]
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
                        self.samurai_1.perform_action(action_num)
                        # Perform the action of samurai 1
                    else:
                        # If it is samurai 2
                        self.samurai_2.perform_action(action_num)
                        # Perform the action of samurai 2
                else:
                    # If the two actions are the same priority (which can only be both true)
                    if self.samurai_1.stance == self.samurai_2.stance or curr_priority > 3:
                        # If the samurai are in the same stance, or combat is ocurring
                        self.act_simultaneously(action_num)
                        # Enact their moves simultaneously
                    elif self.samurai_1.stance == 'heaven':
                        # If samurai 1 is in heaven stance, they act first
                        self.samurai_1.perform_action(action_num, self.samurai_2)
                        self.samurai_2.perform_action(action_num, self.samurai_1)
                    else:
                        # Otherwise samurai 2 is in heaven stance, and they act first
                        self.samurai_2.perform_action(action_num, self.samurai_1)
                        self.samurai_1.perform_action(action_num, self.samurai_2)

            if self.samurai_1.attacked ^ self.samurai_2.attacked:
                # If only one of the samurai attacked this turn (logical XOR)
                self.samurai_1.health -= self.samurai_2.attacked
                self.samurai_2.health -= self.samurai_1.attacked
                # Both samurai take damage depending on whether their opponent attacked
                # This implicitly translates the booleans into integers

            self.samurai_1.attacked, self.samurai_2.attacked = False, False
            # Reset the attack flag on both samurai

    def act_simultaneously(self, action_num):
        # Function to allow two samurai actions to be performed simultaneously
        self.samurai_1.perform_action(action_num, None)
        self.samurai_2.perform_action(action_num, None)
        # Perform actions as normal, ignoring opponent position & simultaneous factor
        while self.samurai_1.position > (self.board_size - self.samurai_2.position - 1):
            # If the samurai have tried to move past one another
            self.samurai_1.position -= 1
            self.samurai_2.position -= 1
            # Move both back one space and check again

        if (self.samurai_1.counter_attack and self.samurai_2.attacked
                or self.samurai_2.counter_attack and self.samurai_1.attacked):
            # If one character is attacking and the other is counter attacking
            self.samurai_1.attacked = not self.samurai_1.attacked
            self.samurai_2.attacked = not self.samurai_2.attacked
            # Invert the attack variables so the counter attacking samurai deals damage

        self.samurai_1.counter_attack, self.samurai_2.counter_attack = False, False
        # Get rid of the counter attacking variable after checking so a samurai doesn't become invincible

    def display_board(self, view=1):
        # Function to show the board, by default from samurai 1's perspective
        board_spaces = [['', ''] for _ in range(self.board_size)]
        # Hold the values in spaces left & right of the centre line

        close_samurai = self.__getattribute__(f'samurai_{view}')
        # Get the samurai which should be displayed at the bottom of the view
        far_samurai = self.__getattribute__(f'samurai_{3 - view}')
        # Get the samurai which should be displayed at the top of the view
        board_spaces[self.board_size - 1 - close_samurai.position][
            1] = f'{close_samurai.player} ({close_samurai.stance})'
        # Set index backwards from the last with the player's name and stance
        board_spaces[far_samurai.position][0] = f'{far_samurai.player} ({far_samurai.stance})'
        # Set index forward from the first with the opponent's name and stance

        for position in board_spaces:
            # Iterate through the board spaces
            print(f'{position[0].rjust(self.name_width)}|{position[1].ljust(self.name_width)}')
            # Print the values in each position, spaced out so everything aligns down the middle


class Card:
    # Class for holding a generic card object
    # This usually maps directly to an action, but some cards have multiple actions
    def __init__(self, *args):
        # Cna be initialised with 1 or 2 arguments
        if len(args) == 2:
            # If the card has two actions
            self.name = f'{args[0].name} / {args[1].name}'
            # Combine the names of the two actions for the card name
        else:
            self.name = args[0].name
            # If there is only one action, copy its name

        self.actions = args
        # Set the actions to be contained in the list


class Samurai:
    # Class for dealing with Samurai data (health, hand & discard)
    def __init__(self, player_name):
        # Initialised with a player name
        self.player = player_name
        # Store the player name
        self.hand = []
        # Stores the cards in hand
        self.discard = None
        # Have no discarded card by default
        self.played_cards = []
        # Cards played with index 0 being returned & index 1 being put into discard
        self.played_actions = []
        # Actions played for the corresponding cards
        self.stance = 'heaven'
        # Start in heaven stance (for a basic game)
        self.position = 0
        # Stores the current board position of the samurai
        # Set as 0 for a basic game
        self.health = 2
        # Stores the samurai's health (2: healthy, 1: flipped, 0: dead)
        self.attacked = False
        # Stores if the samurai is currently attacking

    def return_actions(self):
        # Function to return all the available actions for the samurai
        # This may be updated in the future to return a vector of 1s and 0s for NN input
        actions = []
        # Create an empty list
        for card in self.hand:
            # For each card in the samurai's hand
            actions.append(card.actions)
            # Add all that cards actions to the action list

        return actions
        # Return the list of actions

    def return_cards(self):
        # Function to return all the available cards to the samurai
        return self.hand
        # Just returns the hand at the moment
