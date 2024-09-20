import Card
from BaseController import BaseController
from Board import Board
from Samurai import Samurai


class ManualController(BaseController):
    def select_actions(self, input_vector):
        # The 30 long input vector
        # [0] own health (0,0.5 or 1)
        # [1] own position (between 0 & 1, rounded to 2 dp)
        # [2] Own stance (0 = heaven, 1 = earth)
        # [3-10] cards in hand
        # [11-18] card in discard - also includes own used special card
        # [19] opponent health (0,0.5 or 1)
        # [20] opponent position (between 0 & 1, rounded to 2 dp)
        # [21] opponent stance (0 = heaven, 1 = earth)
        # [22-29] opponent card in discard - also includes used special card

        self_samurai = Samurai('self')
        opponent_samurai = Samurai('opponent')
        # Create saumrai objects for you and your opponent

        self_pos = input_vector[1]
        opponent_pos = input_vector[20]
        # Get the fractional values for you and your opponents position
        # These are used to work out if the game is basic or advanced by checking if they are multiples of 0.25

        if round(self_pos) == self_pos and round(opponent_pos) == opponent_pos:
            print('WARNING: ADVANCED ASSUMED')
            # If both players are at extremes, print a warning for the display
            game_type = 'advanced'
            board_size = 7
        elif (self_pos * 4 // 1 == self_pos * 4) and (opponent_pos * 4 // 1 == opponent_pos * 4):
            game_type = 'basic'
            board_size = 5
        else:
            game_type = 'advanced'
            board_size = 7
        # Estimate the board size from positions
        # Will assume an advanced game if both players are at the extremes

        display_board = Board(game_type, self_samurai, opponent_samurai, display_only=True)
        # Create a dummy board to display the game
        self_samurai.health = input_vector[0] * 2
        self_samurai.position = round(input_vector[1] * (board_size - 1))
        if input_vector[2] > 0:
            self_samurai.stance = 'earth'
        # Set your health, position and stance for display

        opponent_samurai.health = input_vector[19] * 2
        opponent_samurai.position = (board_size - 1) - round(input_vector[20] * (board_size - 1))
        if input_vector[21] > 0:
            opponent_samurai.stance = 'earth'
        # Set your opponent's health, position and stance for display

        display_board.display_board()
        # Show the board

        hand = [Card.all_card_list[in_hand] for in_hand, value in enumerate(input_vector[3:11]) if
                value == 1]
        # Get a list of all cards in your hand
        hand_list = [f' {card.name}[{i}],' for i, card in enumerate(hand)]
        # Make a string of each card name and index
        hand_string = 'Your hand:'
        # Create a string to store your hand
        for card in hand_list:
            hand_string += card
        # Add all card names and indices
        print(hand_string.strip(','))
        # Print the hand string without the trailing comma

        try:
            self_discard = Card.all_card_list[input_vector[11:16].index(1.0)].name
            # Try to get the name of the discarded card
            input_vector[input_vector[11:16].index(1.0) + 11] = 0.0
            # Remove this so the first value of 1.0 will be the special card if it has been used
        except ValueError:
            self_discard = 'None'
            # If there is no discarded card, return None
        print(f'Your discard: {self_discard}')
        # Display your discarded card

        try:
            self_used = Card.all_card_list[input_vector[11:19].index(1.0)].name
            # Try to get the name of the used special card
            print(f'Your used special card: {self_used}')
            # Display your used special card
        except ValueError:
            pass
            # If there is no special card, do nothing

        try:
            opponent_discard = Card.all_card_list[input_vector[22:27].index(1.0)].name
            # Try to get the name of the discarded card
            input_vector[input_vector[22:27].index(1.0) + 22] = 0.0
            # Remove this so the first value of 1.0 will be the special card if it has been used
        except ValueError:
            opponent_discard = 'None'
            # If there is no discarded card, return None
        print(f'Opponent discard: {opponent_discard}')
        # Display your opponent's discarded card

        try:
            opponent_used = Card.all_card_list[input_vector[22:30].index(1.0)].name
            # Try to get the name of the used special card
            print(f'Opponent used special card: {opponent_used}')
            # Display your opponent's used special card
        except ValueError:
            pass
            # If there is no special card, do nothing

        card_index_1, card_index_2 = -1, -1
        # Set the selection indices to invalid values
        action_1, action_2 = None, None
        # Initialise the variable for storing the actions

        while card_index_1 == card_index_2:
            # While the user has not selected 2 different / valid cards to play from their hand
            card_index_1 = int(input('Select the number of the first card you want to play from your hand: '))
            # Ask them to input a number for their card based on their hand
            try:
                if len(hand[card_index_1].actions) > 1:
                    # If that card has multiple actions assigned to it
                    action_index = int(input(
                        f'Select {hand[card_index_1].actions[0].name}[0] or {hand[card_index_1].actions[1].name}[1]:'))
                    # Ask them to select the action from the available actions on the card
                    action_1 = hand[card_index_1].actions[action_index]
                    # Store the chosen action for later
                else:
                    action_1 = hand[card_index_1].actions[0]
                    # If the card only has one available action, store it for later
            except IndexError:
                # If the value is too large, set it to be -1
                card_index_1 = -1

            card_index_2 = int(input('Select the number of the second card you want to play from your hand: '))
            # Ask them to input a number for their card based on their hand
            try:
                if len(hand[card_index_2].actions) > 1:
                    # If that card has multiple actions assigned to it
                    action_index = int(input(
                        f'Select {hand[card_index_2].actions[0].name}[0] or {hand[card_index_2].actions[1].name}[1]:'))
                    # Ask them to select the action from the available actions on the card
                    action_2 = hand[card_index_2].actions[action_index]
                    # Store the chosen action for later
                else:
                    action_2 = hand[card_index_2].actions[0]
                    # If the card only has one available action, store it for later
            except IndexError:
                # If the value is too large, set it to be -1
                card_index_2 = -1

            if card_index_1 < 0 or card_index_2 < 0:
                # If the input number is negative (either from being too large or incorrect input)
                card_index_1 = card_index_2
                # Set the indices equal to restart the loop

        self.output_vector = [0] * 20
        # Create a blank output vector

        for index, action in enumerate(Card.all_action_list):
            # Go through all the possible actions in the action list
            if action == action_1.name:
                # If the action is equal to the first chosen action
                self.output_vector[index] = 1
                # Set the output vector for that action to 1 (must be chosen)
            elif action == action_2.name:
                # If the action is equal to the second chosen action
                self.output_vector[index + 10] = 1
                # Set the output vector for that action (2nd half) to 1 (must be chosen)

            if sum(self.output_vector) == 2:
                # If we've done this twice, then we have no more actions to add to our output vector
                break

        return super().rank_actions_max()
        # Return the actions ranked by the maximum output vector (your selection, which is set to 1)

    def choose_setup(self, special_cards):
        special_index = special_cards.index(1.0)
        special_card = Card.special_card_list[special_index]
        # Get the special card that the player has been given
        start_pos = -1
        while start_pos < 0 or start_pos > 2:
            start_pos = int(
                input(f'Your single-use card is {special_card.name}.\n Choose your start position (0,1 or 2):'))
            # Get the user to input the start position they want to use

        stance = 'null'
        # Initialise the stance as an invalid value
        while stance not in ['heaven', 'earth']:
            # Keep asking until the user gives a valid stance
            stance = input('Select your stance (heaven or earth):').lower()
            # Get the stance and automatically make it lower case

        return [start_pos, stance]
        # Return the start position and stance as input by the user to the game

    def get_reward(self, agent):
        # Required to be implemented, but will never be used
        return round(random(), 2)
        # Return a random number just in case it would cause an error not to

    def modify_rewards(self, agent):
        # Required to be implemented, but will never be used
        return agent.input_vectors
        # Return the unmodified input vectors
