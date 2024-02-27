import os

import torch
from torch.nn import Linear
from torch.utils.data import DataLoader


from dataset import DATA_DIR, MediapipeDataset

if __name__ == "__main__":

    train_dataset = MediapipeDataset(
        os.path.join(DATA_DIR, "inputs_queue0.npy"),
        os.path.join(DATA_DIR, "outputs_queue0.npy"),
    )

    # get the first item from the dataset
    landmarks, rotations = train_dataset[0]

    print(landmarks.shape, rotations.shape)

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

    print(train_loader)

    # val_dataset = CustomDataset("path/to/val/data")
    # val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

    # Train the model
    for epoch in range(epochs):
        for features, targets in train_loader:  # Ignore labels for now
            # Forward pass
            outputs = model(features)

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

# # Evaluate the model (assuming you have validation data)
# with torch.no_grad():
#     for data, _ in val_loader:
#         outputs = model(data)
#         # Calculate and print loss or other evaluation metrics
#         ...

# print("Training complete!")