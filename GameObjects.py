class Action:
    # Class for holding the different actions and logic for playing the game
    def __init__(self, name, move_dist=0, strike_min=-1, strike_range=0, end_stance='same', begin_stance='any'):
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

        # Determine the type of the action for prioritisation
        if abs(self.movement) == 1:
            # If the card moves you by 1 it has top priority
            self.type = 'movement'
        elif self.movement == 2:
            # If it moves you by 2 it is charge and has 2nd priority
            self.type = 'charge'
        elif self.end_stance == 'change':
            # If it is the change stance card it has third priority
            self.type = 'stance_change'
        else:
            # If it is an attack it will be resolved last & simultaneously
            self.type = 'attack'


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

    def display_board(self, view=1):
        # Function to show the board, by default from samurai 1's perspective
        baord_spaces = [['', ''] for _ in range(self.board_size)]
        # Hold the values in spaces left & right of the centre line

        close_samurai = self.__getattribute__(f'samurai_{view}')
        # Get the samurai which should be displayed at the bottom of the view
        far_samurai = self.__getattribute__(f'samurai_{3 - view}')
        # Get the samurai which should be displayed at the top of the view
        baord_spaces[self.board_size - 1 - close_samurai.position][
            1] = f'{close_samurai.player} ({close_samurai.stance})'
        # Set index backwards from the last with the player's name and stance
        baord_spaces[far_samurai.position][0] = f'{far_samurai.player} ({far_samurai.stance})'
        # Set index forward from the first with the opponent's name and stance

        for position in baord_spaces:
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
            self.side_2 = args[1]
            # Add the second action as the second side
        else:
            self.name = args[0].name
            # If there is only one action, copy its name

        self.side_1 = args[0]
        # Set the first / only action to the first side


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
        self.stance = 'heaven'
        # Start in heaven stance (for a basic game)
        self.position = 0
        # Stores the current board position of the samurai
        # Set as 0 for a basic game
        self.damaged = False
        # Stores if the samurai is damaged
