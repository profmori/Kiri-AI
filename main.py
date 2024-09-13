from Board import Board
from ManualController import ManualController
from Samurai import Samurai

if __name__ == '__main__':
    p1 = Samurai('jom', ManualController())
    # Initialises a samurai called Jom with a manual controller
    p2 = Samurai('rajun')
    # Initialises a samurai called Rajun (random controller by default)

    new_board = Board('advanced', p1, p2)
    # Begins a game on the advanced board with these players

    result = new_board.run_game()
    # Runs the game on that board

    print(result)
    # Prints the dictionary of the result
