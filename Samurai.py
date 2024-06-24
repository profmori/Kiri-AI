import Card
from BaseController import BaseController
from RandomController import RandomController


class Samurai:
    # Class for dealing with Samurai data (health, hand & discard)
    def __init__(self, player_name, controller=None):
        # Initialised with a player name
        self.player = player_name
        # Store the player name
        self.hand = []
        # Stores the cards in hand
        self.discard = None
        # Have no discarded card by default
        self.played_cards = [None, None]
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
        self.board_size = 5
        # Stores the size of the board
        self.opponent = None
        # Stores the opponent samurai object
        self.attacking = False
        # Stores if the samurai is currently attacking (and hitting)
        self.counter_attacking = False
        # Stores if the samurai is currently counter attacking

        if issubclass(type(controller), BaseController):
            # Check if the input controller extends the generic controller class
            self.controller = controller
            # Set that as the controller
        else:
            self.controller = RandomController()
        # Set the controller as the input controller type, or random if unspecified

    def advanced_setup(self):
        self.board_size = 7
        # Set the board size as being the larger board
        special_cards = [0] * 3
        # Create a small vector to store which special card the player starts with
        for i, card in enumerate(Card.special_card_list):
            if card in self.hand:
                special_cards[i] = 1
                break
            # Returns 1 if it is the special card and then exits the loop

        setup = self.controller.choose_setup(special_cards)
        # Get the setup from the controller based on the assigned special card
        self.position = setup[0]
        # Set position based on the setup output
        self.stance = setup[1]
        # Set the stance based on the setup output

    def choose_actions(self):
        # Function to choose the action for the samurai - eventually this will call a brain to make the decision

        input_vector = self.generate_input_vector()
        # Generate the 28 long input vector
        # [0] own health (0,0.5 or 1)
        # [1] own position (between 0 & 1, rounded to 2 dp)
        # [2-9] cards in hand
        # [10-17] card in discard
        # [18] opponent health (0,0.5 or 1)
        # [19] opponent position (between 0 & 1, rounded to 2 dp)
        # [20-27] opponent card in discard

        output_vector = self.controller.select_actions(input_vector)
        # Get the output of the controller as a list of weights for each action

        for card_play in range(2):
            # Iterate through each half of the list
            action_ranks = output_vector[10 * card_play: 10 * card_play + 10]
            # Get the rankings of each action from the controller output
            available_actions = self.return_possible_actions()
            # Get all the possible remaining actions from the cards in hand
            for action_name in action_ranks:
                # Go through the actions in the NN ranked order
                if action_name in available_actions.keys():
                    # if the chosen action is valid
                    chosen_action = available_actions[action_name]
                    # Store the chosen action
                    chosen_card = self.get_hand_card(chosen_action)
                    # Store the chosen card

                    self.played_actions += [chosen_action]
                    # Add the chosen action to the played card list
                    self.played_cards[card_play] = chosen_card
                    # Add the chosen card to the correct index of chosen card list
                    self.hand.remove(chosen_card)
                    # Remove the chosen card from the player hand
                    break
                    # Break out of the while loop

    def generate_input_vector(self):
        input_vector = [0.0] * 28
        # Create a list to store the cards in hand in a network readable format
        # The structure is:
        # [0] own health (0,0.5 or 1)
        # [1] own position (between 0 & 1, rounded to 2 dp)
        # [2-9] cards in hand
        # [10-17] card in discard
        # [18] opponent health (0,0.5 or 1)
        # [19] opponent position (between 0 & 1, rounded to 2 dp)
        # [20-27] opponent card in discard

        input_vector[0] = self.health / 2
        input_vector[18] = self.opponent.health / 2
        # Health as a fraction
        input_vector[1] = round(self.position / (self.board_size - 1), 2)
        opponent_position = self.board_size - 1 - self.opponent.position
        input_vector[19] = round(opponent_position / (self.board_size - 1), 2)
        # Position as a fraction

        for i, card in enumerate(Card.all_card_list):
            # Run through every card in the game
            input_vector[i + 2] = float(card in self.hand)
            # If it's in your hand
            input_vector[i + 10] = float(card == self.discard)
            # If it's in your discard
            input_vector[i + 20] = float(card == self.opponent.discard)
            # If it is the opponent's discard

        return input_vector
        # Return the value

    def get_card(self, action):
        # Get a card from an action name
        card = self.get_played_card(action)
        # Check the played cards first

        if card is not None:
            # If the card was found
            return card
            # Return it
        else:
            return self.get_hand_card(action)
            # If you don't find the card in the played cards, look through the hand

    def get_hand_card(self, action):
        for card in self.hand:
            # Iterate through the cards in hand
            if action in card.actions:
                # If the action is assigned to that card
                return card
                # Return the card
        return None
        # If no card is found, return None

    def get_played_card(self, action) -> Card:
        # Get the card from the action
        if self.played_cards[0] is None:
            # If the first played card is None
            return None
            # Return invalid

        for card in self.played_cards:
            # Iterate through the currently played cards
            if action in card.actions:
                # If the action is assigned to that card
                return card
                # Return the card
        return None
        # If no card is found, return None

    def perform_action(self, simultaneous=False):
        # Perform the currently selected action of the samurai
        action = self.played_actions[0]
        # Get the first action in the action queue

        if self.stance == action.begin_stance or action.begin_stance == 'any':
            # If you are in the correct beginning stance or the beginning stance doesn't matter
            print(self.player, action.name)
            # Print the action being performed
            opponent_position = self.board_size - 1 - self.opponent.position
            # Get the opponent's position relative to you

            #################################
            # Handle movement actions first #
            #################################
            self.position += action.movement
            # Move yourself by the movement of the action
            self.position = min(max(0, self.position), self.board_size - 1)
            # Constrain your position to be within the board
            if not simultaneous and self.position > opponent_position:
                # If the movement is not occurring simultaneously, and you have moved past the opponent position
                self.position = opponent_position
                # Set your position to the opponent position (sharing a space)

            #################################
            # Handle attacking actions next #
            #################################

            if (self.position + action.strike_min) <= opponent_position <= (self.position + action.strike_max):
                # If the opponent position is between your minimum attack range and maximum attack range
                self.attacking = True
                # You are successfully attacking
                print('attacking')
                # Return this for testing
            elif action.strike_min > action.strike_max:
                # If your attack has a negative range
                self.counter_attacking = True
                # You are counterattacking
                print('counter attacking')
                # Return this for testing

            ##############################
            # Handle stance changes next #
            ##############################

            if action.end_stance != 'same':
                # If the action does change your stance
                if action.end_stance == 'change':
                    # If it swaps stances
                    end_stance = ['heaven', 'earth']
                    # Create a list of all stances
                    end_stance.remove(self.stance)
                    # Remove the current stance
                    self.stance = end_stance[0]
                    # Set the stance to the remaining stance
                else:
                    # If the end stance is set
                    self.stance = action.end_stance
                    # Set your stance to the end stance
        else:
            # If you are in the wrong stance for the action, and the action has a specific stance
            print(self.player, action.name, 'failed')
            # Report that the action has failed

        ###############################################################################
        # Once all action effects have resolved, discard the card / return it to hand #
        ###############################################################################

        if not action.single_use:
            # If an action is not one of the single use special cards, it needs to be kept in the game
            played_card = self.get_played_card(action)
            # Get the played card that corresponds to the action
        else:
            played_card = None
            # Special cards should just be blanked from the game

        if len(self.played_actions) == 2:
            # If this is the first card played
            if played_card is not None:
                # Check there is a card to add back to the hand
                self.hand.append(played_card)
                # Return it to your hand
        else:
            # If it is the second card played
            if self.discard is not None:
                # If there is a card in the discard pile
                self.hand.append(self.discard)
                # Add that card back into your hand
            self.discard = played_card
            # Put the played card into the discard pile (special cards reset it to None)

        self.played_actions.pop(0)
        # Remove the played action from the played_actions list

    def return_possible_actions(self):
        # Function to return all the available actions for the samurai
        actions = {}
        # Create an empty dictionary
        for card in self.hand:
            # For each card in the samurai's hand
            actions = actions | {action.name: action for action in card.actions}
            # Add all that cards actions to the action dictionary
        return actions
        # Return the list of actions

    def return_cards(self):
        # Function to return all the available cards to the samurai
        return self.hand
        # Just returns the hand at the moment
