import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import torch.nn.functional as F

from torchvision import datasets, transforms


# class NET(nn.Module):
#     def __init__(self):
#         super(NET, self).__init__()
#         self.model = nn.Sequential(
#             # 1 layer (64, 16, 28,28)
#             nn.Conv2d(1, 10, kernel_size=3, padding=0, stride=1, dilation=1),
#             nn.ReLU(),
#             nn.MaxPool2d(2),
#             # 2 layer (64, 16, 13, 13)
#             nn.Conv2d(10, 16, kernel_size=4, padding=0, stride=1, dilation=1),
#             nn.ReLU(),
#             nn.MaxPool2d(2),
#             # 3 layer (64, 16, 5, 5)
#             nn.Conv2d(16, 32, kernel_size=3, padding=1, stride=1, dilation=1),
#             nn.Flatten(),
#             nn.Linear(32 * 5 * 5, 128),
#             nn.ReLU(),
#             # Optional: Dropout (to prevent overfitting)
#             nn.Dropout(p=0.5),
#             nn.Linear(128, 10),
#         )

#     def forward(self, x):
#         return self.model(x)


class NET(nn.Module):
    def __init__(self):
        super(NET, self).__init__()
        # First convolutional layer (1 input channel, 10 output channels, 3x3 kernel)
        self.conv1 = nn.Conv2d(1, 10, kernel_size=3, stride=1, padding=0)
        self.maxpool1 = nn.MaxPool2d(2)  # 2x2 max pooling

        # Second convolutional layer (10 input channels, 32 output channels, 4x4 kernel)
        self.conv2 = nn.Conv2d(10, 32, kernel_size=4, stride=1, padding=0)
        self.maxpool2 = nn.MaxPool2d(2)  # 2x2 max pooling

        # Third convolutional layer (32 input channels, 64 output channels, 3x3 kernel)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)

        # Flatten layer to flatten the 2D matrix into a 1D vector
        self.flatten = nn.Flatten()

        # Fully connected layers (FC layers)
        self.fc1 = nn.Linear(64 * 5 * 5, 128)  # 1600 inputs to 128 hidden units
        self.fc2 = nn.Linear(
            128, 10
        )  # 128 hidden units to 10 output units (class predictions)

        # Optional: Dropout (to prevent overfitting)
        self.dropout = nn.Dropout(p=0.5)

    def forward(self, x):
        # Apply first conv layer, ReLU activation, and max pooling
        x = F.relu(self.conv1(x))
        x = self.maxpool1(x)

        # Apply second conv layer, ReLU activation, and max pooling
        x = F.relu(self.conv2(x))
        x = self.maxpool2(x)

        # Apply third conv layer and ReLU activation
        x = F.relu(self.conv3(x))

        # Flatten the feature map into a 1D vector
        x = self.flatten(x)

        # Apply first fully connected layer with ReLU activation
        x = F.relu(self.fc1(x))

        # Apply dropout (optional, helps with regularization)
        x = self.dropout(x)

        # Apply second fully connected layer for classification (logits output)
        x = self.fc2(x)

        return x
