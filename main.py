from Board import Board
from RandomController import RandomController
from Samurai import Samurai

if __name__ == '__main__':
    p1 = Samurai('jom', RandomController())
    # Initialises a samurai called Jom
    p2 = Samurai('rajun')
    # Initialises a samurai called Rajun

    new_board = Board('advanced', p1, p2)
    # Begins a game on the basic board with these players

    new_board.run_game()
    # Runs the game on that board
