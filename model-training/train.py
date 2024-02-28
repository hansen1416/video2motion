import os

import numpy as np
import torch
from torch import Tensor
from torch import nn
from torch.utils.data import DataLoader

from Model import MyModel
from dataset import DATA_DIR, MediapipeDataset


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
    epochs = 1000

    # # Create a small neural network
    # model = torch.nn.Sequential(
    #     Linear(99, 128),  # Input layer to hidden layer with 32 units
    #     torch.nn.ReLU(),  # Activation function
    #     Linear(128, 66),  # Hidden layer to output layer with 66 units
    # )

    model = MyModel()

    # Define loss function and optimizer
    loss_fn = torch.nn.MSELoss(reduction="none")  # Mean squared error for regression
    loss_fn2 = torch.nn.MSELoss(reduction="mean")  # Mean squared error for regression
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Create data loaders (replace with your actual data paths)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

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

            # euler2vector(outputs)

            # Calculate loss
            loss = loss_fn(
                outputs, targets
            )  # Compare outputs with input data (assume labels unavailable)

            # print(loss)

            # get the sqrt of the sum of the squares `loss_mid`
            loss_result = torch.sqrt(torch.sum(torch.sum(loss, dim=2) ** 2))

            # print(loss_result)

            # Backward pass and optimize
            optimizer.zero_grad()
            loss_result.backward()
            optimizer.step()

            # Print training progress (optional)
            print(f"Epoch {epoch+1}/{epochs}, Loss: {loss_result.item():.4f}")

        #     break
        # break

    # save the model to local file
    torch.save(model.state_dict(), "model.pth")

# # Evaluate the model (assuming you have validation data)
# with torch.no_grad():
#     for data, _ in val_loader:
#         outputs = model(data)
#         # Calculate and print loss or other evaluation metrics
#         ...

# print("Training complete!")
