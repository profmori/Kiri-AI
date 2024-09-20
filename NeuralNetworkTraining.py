from random import shuffle

import ray

from Board import Board
from Samurai import Samurai


def train_controller_list(controller_list, num_loops=1000, num_agents=10):
    # Function to run the training of agents from a list of available agents

    loops_completed = 0
    # Variable to track the number of loops completed
    while loops_completed < num_loops:
        # Runs for a number of loops as input, or 1000 by default

        agent_list = []
        # Regenerate the agents every loop to keep model weights up to date
        for agent in range(num_agents):
            # Creates a number of agents of each controller equal to the input value, or 10 by default
            for controller in controller_list:
                # Iterates through all the input controllers to make a new instance
                name = f'{controller.__name__}_{agent}'
                # Set the name equal to the controller name and number
                agent_list += [Samurai(name, controller)]
                # Add to the agent list

        if len(agent_list) // 2 == 1:
            # If there is an odd number of agents created
            agent_list += [Samurai(f'RandomController_{num_agents + 1}')]
            # Create one additional agent with a random controller to fill out the list

        num_games = len(agent_list) // 2
        # Get the number of battles as half the number of agents generated
        shuffle(agent_list)
        # Shuffle the agent list so game matchups are random

        board_list = [Board('advanced', agent_list[i], agent_list[i + num_games]) for i in
                      range(num_games)]
        # Generate a number of game boards equal to num_games
        # by using the first half and second half of the list for matches
        # In the future, if we want to go longer between training steps, we could make it so each agent
        # fights one of each other agent before training - won't work until we have more agents

        run_list = [run_game.remote(board) for board in board_list]
        # Creates a list of ray remote functions (effectively functions that can be parallelised) to be run
        # The run_game function could also automatically train the network after finishing
        games = ray.get(run_list)
        # Run the games and collect the outputs from the run game function
        loops_completed += 1
        # Increment the loop count by 1

    print(games)


@ray.remote
def run_game(board):
    # Parallelisable function (@ray.remote decorator) that runs each board in a thread
    # Might be worth extending this to also run the back propagation of the neural network
    return board.run_game()
    # Currently just returns the dictionary output of the Board run_game function
