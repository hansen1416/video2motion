import os

import numpy as np
import torch
from torch import Tensor
from torch import nn
from torch.utils.data import DataLoader

from Model import MyModel
from dataset import DATA_DIR, MediapipeDataset

# load model saved by `torch.save(model.state_dict(), "model.pth")`
model = MyModel()

model.load_state_dict(torch.load("model.pth"))

model.eval()  # set the model to evaluation mode

print(model)

train_dataset = MediapipeDataset(
    os.path.join(DATA_DIR, "inputs_queue0.npy"),
    os.path.join(DATA_DIR, "outputs_queue0.npy"),
)

inputs, outputs = train_dataset[0]

# add one more dimension to inputs and outputs
inputs = inputs.unsqueeze(0)
outputs = outputs.unsqueeze(0)

print(inputs.shape)

# predict inputs[0] using the model
with torch.no_grad():  # no need to track the gradients
    prediction = model(inputs)

# calculate mse between prediction and outputs

loss_fn = torch.nn.MSELoss(reduction="mean")  # Mean squared error for regression
loss = loss_fn(prediction, outputs)

# print(prediction)
# print(outputs)
print(loss.item())
