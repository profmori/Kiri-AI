from copy import copy

from Board import Board
from Card import basic_card_list, special_card_list
from Samurai import Samurai

if __name__ == '__main__':
    p1 = Samurai('jom')
    # Initialises a samurai called Jom
    p2 = Samurai('rajun')
    # Initialises a samurai called Rajun

    p1.hand = copy(basic_card_list) + copy(special_card_list)
    p2.hand = copy(basic_card_list) + copy(special_card_list)
    new_board = Board('basic', p1, p2)
    # Begins a game on the basic board with these players

    turn = 0
    while min(p1.health, p2.health) > 0:
        turn += 1
        print('Turn', turn)
        new_board.run_turn()
