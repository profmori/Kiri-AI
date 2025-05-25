from BaseController import BaseController
import torch

class FullyConnectedSetup(torch.nn.Module):
    def __init__(self):
        super().__init__()
        mid_layer_size = 5
        layer_1 = torch.nn.Linear(in_features=3, out_features=mid_layer_size)
        layer_2 = torch.nn.Linear(in_features=mid_layer_size, out_features=2)
        self.sequence = torch.nn.Sequential(layer_1, layer_2, torch.nn.Sigmoid())

    def forward(self, x):
        return self.sequence(x)
