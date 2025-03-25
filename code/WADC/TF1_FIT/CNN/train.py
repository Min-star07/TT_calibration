import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
import os
from torchvision import datasets, transforms
from model import NET

# Data transformations (normalization for MNIST)
transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
)

# Load the MNIST dataset
train_data = datasets.MNIST(
    root="./data", train=True, transform=transform, download=True
)
test_data = datasets.MNIST(
    root="./data", train=False, transform=transform, download=True
)

# DataLoader for training and testing
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=1000, shuffle=False)

# Set device to GPU if available, otherwise CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Directory to save the model
model_path = "./model_minist"
os.makedirs(model_path, exist_ok=True)  # Ensure model directory exists

# Initialize model, criterion, and optimizer
model = NET().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-2)

# TensorBoard writer
writer = SummaryWriter("./logs_minist")

# Number of epochs
epochs = 100
best_accuracy = 0.0  # Variable to track the best accuracy for model saving

for epoch in range(epochs):
    model.train()  # Set model to training mode
    total_loss = 0.0
    correct = 0
    total_num = 0.0

    for idx, (inputs, targets) in enumerate(train_loader):
        inputs, targets = inputs.to(device), targets.to(device)

        # Forward pass
        y_pred = model(inputs)
        loss = criterion(y_pred, targets)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        _, predicted = torch.max(y_pred, 1)

        # Track correct predictions
        correct += (predicted == targets).sum().item()
        total_num += targets.size(0)

    # Calculate training accuracy
    train_accuracy = correct / total_num * 100

    # Print training stats
    print(
        f"Epoch {epoch+1}/{epochs}, Loss: {total_loss:.4f}, Accuracy: {train_accuracy:.2f}%"
    )

    # Log metrics to TensorBoard
    writer.add_scalar("Loss/train", total_loss, epoch)
    writer.add_scalar("Accuracy/train", train_accuracy, epoch)
    writer.add_graph(model, inputs)

    # Save the model after every epoch
    model_save_path = os.path.join(model_path, f"model_minist_{epoch+1}.pth")
    torch.save(model.state_dict(), model_save_path)

    # Save the best model based on accuracy
    if train_accuracy > best_accuracy:
        best_accuracy = train_accuracy
        best_model_path = os.path.join(model_path, "best_model.pth")
        torch.save(model.state_dict(), best_model_path)

# Evaluation on test dataset
model.eval()  # Set model to evaluation mode
correct_test = 0.0
total_num_test = 0.0

with torch.no_grad():  # Disable gradient computation for evaluation
    for inputs, targets in test_loader:
        inputs, targets = inputs.to(device), targets.to(device)
        outputs = model(inputs)
        _, predicted = torch.max(outputs, 1)

        correct_test += (predicted == targets).sum().item()
        total_num_test += targets.size(0)

test_accuracy = correct_test / total_num_test * 100
print(f"Test Accuracy: {test_accuracy:.2f}%")

# Close TensorBoard writer
writer.close()
