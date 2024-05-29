from random import sample


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
        self.attacking = False
        # Stores if the samurai is currently attacking (and hitting)
        self.counter_attacking = False
        # Stores if the samurai is currently counter attacking

    def choose_actions(self):
        # Function to choose the action for the samurai - eventually this will call a brain to make the decision
        self.played_cards = sample(self.hand, 2)
        # Choose 2 cards at random from the cards available in the hand
        for card in self.played_cards:
            # Iterate through the chosen cards
            action = sample(card.actions, 1)
            # Choose one of the actions that card can do
            self.played_actions += action
            # Add the action to the played actions list
            self.hand.remove(card)
            # Remove the card from the stored hand

    def get_card(self, action):
        # Get a card from an action name
        card = self.get_played_card(action)
        # Check the played cards first

        if card is not None:
            # If the card was found
            return card
            # Return it
        else:
            # If you don't find the card in the played cards, look through the hand
            for card in self.hand:
                # Iterate through the cards in hand
                if action in card.actions:
                    # If the action is assigned to that card
                    return card
                    # Return the card
            return None
            # If no card is found, return None

    def get_played_card(self, action):
        for card in self.played_cards:
            # Iterate through the currently played cards
            if action in card.actions:
                # If the action is assigned to that card
                return card
                # Return the card
        return None
        # If no card is found, return None

    def perform_action(self, opponent, board_size, simultaneous=False):
        # Perform the currently selected action of the samurai
        action = self.played_actions[0]
        # Get the first action in the action queue

        if self.stance == action.begin_stance or action.begin_stance == 'any':
            # If you are in the correct beginning stance or the beginning stance doesn't matter
            print(self.player, action.name)
            # Print the action being performed
            opponent_position = board_size - opponent.position - 1
            # Get the opponent's position relative to you

            #################################
            # Handle movement actions first #
            #################################
            self.position += action.movement
            # Move yourself by the movement of the action
            self.position = min(max(0, self.position), board_size - 1)
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
                # If your attack has a negative range (this will probably cause issues down the line)
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

    def return_actions(self):
        # Function to return all the available actions for the samurai
        # This may be updated in the future to return a vector of 1s and 0s for NN input
        actions = []
        # Create an empty list
        for card in self.hand:
            # For each card in the samurai's hand
            actions += card.actions
            # Add all that cards actions to the action list

        return actions
        # Return the list of actions

    def return_cards(self):
        # Function to return all the available cards to the samurai
        return self.hand
        # Just returns the hand at the moment
