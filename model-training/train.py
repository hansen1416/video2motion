import os

import numpy as np
import torch
from torch import Tensor
from torch.nn import Linear
from torch.utils.data import DataLoader

from dataset import DATA_DIR, MediapipeDataset
from lib3d.lib import vector_apply_euler_tensor


def euler2vector(t: Tensor):
    # v1.view(-1, 3)
    # v2 = v2.reshape(-1, 3)

    # # apply vector_apply_euler_arr along axis 2
    # v1 = torch.Tensor.apply_along_dim(vector_apply_euler_tensor, 2, v1)

    print(t)

    for i in range(t.shape[0]):
        for j in range(t.shape[1]):
            tmp = t.view(-1, 22, 3)[i, j]
            print(tmp)


if __name__ == "__main__":

    train_dataset = MediapipeDataset(
        os.path.join(DATA_DIR, "inputs_queue0.npy"),
        os.path.join(DATA_DIR, "outputs_queue0.npy"),
    )

    # get the first item from the dataset
    landmarks, rotations = train_dataset[0]

    # print(landmarks.shape, rotations.shape)

    # Assuming you have your CustomDataset class defined

    # Hyperparameters (adjust based on your needs)
    learning_rate = 0.01
    epochs = 10

    # Create a small neural network
    model = torch.nn.Sequential(
        Linear(99, 128),  # Input layer to hidden layer with 32 units
        torch.nn.ReLU(),  # Activation function
        Linear(128, 66),  # Hidden layer to output layer with 66 units
    )

    # Define loss function and optimizer
    loss_fn = torch.nn.MSELoss()  # Mean squared error for regression
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Create data loaders (replace with your actual data paths)
    train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)

    # print(train_loader)

    # val_dataset = CustomDataset("path/to/val/data")
    # val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

    # Train the model
    for epoch in range(epochs):
        for features, targets in train_loader:  # Ignore labels for now
            # Forward pass
            outputs = model(features)

            # # reshape the outputs from (bacth_size, 66) to (batch_size, 22, 3)
            # outputs = outputs.reshape(-1, 22, 3)
            # targets = targets.reshape(-1, 22, 3)

            euler2vector(outputs)

            # Calculate loss
            loss = loss_fn(
                outputs, targets
            )  # Compare outputs with input data (assume labels unavailable)

            # Backward pass and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # Print training progress (optional)
            print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")

            break
        break

# # Evaluate the model (assuming you have validation data)
# with torch.no_grad():
#     for data, _ in val_loader:
#         outputs = model(data)
#         # Calculate and print loss or other evaluation metrics
#         ...

# print("Training complete!")
