import numpy as np
import torch
from torch.utils.data import Dataset


class MediapipeDataset(Dataset):

    def __init__(self, inputs_file, outputs_file, device="cpu") -> None:
        super().__init__()

        self.inputs = np.load(inputs_file)
        self.outputs = np.load(outputs_file)

        self.inputs = torch.tensor(self.inputs, dtype=torch.float32).to(device)
        self.outputs = torch.tensor(self.outputs, dtype=torch.float32).to(device)

    def __len__(self):
        return self.inputs.shape[0]

    def __getitem__(self, idx):
        return self.inputs[idx], self.outputs[idx]


if __name__ == "__main__":

    import os

    dataset = MediapipeDataset(
        os.path.join("data", "inputs_queue0.npy"),
        os.path.join("data", "outputs_queue0.npy"),
        device="cpu",
    )

    print(dataset[0])
