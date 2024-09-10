import torch
import torch.nn as nn
import torchvision

class UNetResNet(nn.Module):
    def __init__(self, num_classes):
        super(UNetResNet, self).__init__()
        self.base_model = torchvision.models.resnet34(pretrained=True)
        self.final_layer = nn.Conv2d(512, num_classes, kernel_size=1)

    def forward(self, x):
        x = self.base_model(x)
        x = self.final_layer(x)
        return x
