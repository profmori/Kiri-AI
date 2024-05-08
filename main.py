from GameObjects import Samurai, Board, Card, Action

if __name__ == '__main__':
    basic_card_list = [Card(Action('high strike', begin_stance='heaven', strike_min=2)),
                       Card(Action('low strike', begin_stance='earth', strike_min=1)),
                       Card(Action('balanced strike', strike_min=0)),
                       Card(Action('approach', move_dist=1), Action('retreat', move_dist=-1)),
                       Card(Action('charge', move_dist=2), Action('change_stance', end_stance='change'))]
    # The list of basic cards for both players

    special_card_list = [
        Card(Action('kesa strike', begin_stance='heaven', end_stance='earth', strike_min=0, strike_range=1)),
        Card(Action('zan-tetsu strike', begin_stance='earth', end_stance='heaven', strike_min=2, strike_range=1)),
        Card(Action('counterattack', strike_min=0, strike_range=-1))]
    # The special attacks

    p1 = Samurai('jom')
    # Initialises a samurai called Jom
    p2 = Samurai('rajun')
    # Initialises a samurai called Rajun
    new_board = Board('basic', p1, p2)
    # Begins a game on the basic board with these players
    # No logic or 'game' implemented yet, simply prints the board
