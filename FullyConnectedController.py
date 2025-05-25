from FullyConnectedNN import FullyConnectedSetup
from BaseController import BaseController
import torch


class FullyConnectedController(BaseController):

    def __init__(self):
        super().__init__()
        self.setup_model = FullyConnectedSetup()
        self.turn_model = None

    def select_actions(self, input_vector) -> list:
        pass

    def get_reward(self, agent) -> float:
        pass

    def modify_rewards(self, agent) -> dict:
        pass

    def choose_setup(self, special_cards) -> list:
        input_vec = torch.tensor(special_cards)
        return_vec = self.setup_model(input_vec)
        return_list = return_vec.tolist()
        return super().choose_setup(return_list)
