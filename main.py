from FullyConnectedController import FullyConnectedController
from NeuralNetworkTraining import train_controller_list
from RandomController import RandomController
from ray.job_submission import JobSubmissionClient

# You need to install ray which pycharm cannot do automatically
# Run pip install -U "ray[all]"

if __name__ == '__main__':
    controller = FullyConnectedController()

    controller_list = [RandomController]
    # Put all controllers you want to train with in this list
    # Should always have RandomController as a baseline
    # Other deterministic controllers: TBD
    client = JobSubmissionClient("http://127.0.0.1:8265")

    train_controller_list(controller_list, client)
    # Trains the listed controllers
    # Runs 1000 times by default - can set num_loops to cap it to a different value
    # Currently creates 10 of each controller - can set num_agents to change this
    print('done')
