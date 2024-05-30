from Action import Action


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

        self.actions = list(args)
        # Set the actions to be contained in the list


basic_card_list = [Card(Action('high strike', begin_stance='heaven', strike_min=2)),
                   Card(Action('low strike', begin_stance='earth', strike_min=1)),
                   Card(Action('balanced strike', strike_min=0)),
                   Card(Action('approach', move_dist=1), Action('retreat', move_dist=-1)),
                   Card(Action('charge', move_dist=2), Action('change_stance', end_stance='change'))]
# The list of basic cards

special_card_list = [Card(Action('kesa strike', begin_stance='heaven', end_stance='earth',
                                 strike_min=0, strike_range=1, single_use=True)),
                     Card(Action('zan-tetsu strike', begin_stance='earth', end_stance='heaven',
                                 strike_min=2, strike_range=1, single_use=True)),
                     Card(Action('counterattack', strike_min=0, strike_range=-1, single_use=True))]
# The list of special attacks

all_card_list = basic_card_list + special_card_list

all_action_list = [action.name for card in all_card_list for action in card.actions]
