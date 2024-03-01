import os
from typing import Tuple

import numpy as np
import torch
from torch.utils.data import Dataset


class MediapipeDataset(Dataset):

    def __init__(
        self,
        inputs_dir: str,
        outputs_dir: str,
        total_size: int,
        max_file_size: int,
        indices_file_map: dict,
        device="cpu",
    ) -> None:
        """
        Args:
            inputs_dir (str): The directory containing the input data.
            outputs_dir (str): The directory containing the output data.
            total_size (int): The total data size of the dataset.
            max_file_size (int): The maximum data size of a file.
            indices_file_map (dict): A dictionary mapping the indices to the file number.
            device (str, optional): The device to use. Default is "cpu".
        """

        super().__init__()

        self.inputs_dir = inputs_dir
        self.outputs_dir = outputs_dir
        self.total_size = total_size
        self.max_file_size = max_file_size
        self.indices_file_map = indices_file_map
        self.device = device

        # current file data
        self.current_file_idx = None
        self.current_inputs = None
        self.current_outputs = None

    def __len__(self) -> int:
        return self.total_size

    def load_file(self, file_idx) -> None:
        """
        load the data of the file which contains the data of the given index into memory.
        """

        self.current_file_idx = file_idx
        self.current_inputs = np.load(
            os.path.join(self.inputs_dir, f"inputs_{file_idx}.npy")
        )
        self.current_outputs = np.load(
            os.path.join(self.outputs_dir, f"outputs_{file_idx}.npy")
        )

        self.current_inputs = torch.tensor(self.current_inputs, dtype=torch.float32).to(
            self.device
        )

        self.current_outputs = torch.tensor(
            self.current_outputs, dtype=torch.float32
        ).to(self.device)

        print(f"loaded file {file_idx}")

    def __getitem__(self, idx) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Get the input and output data of the given index.
        if the data is not in memory, load the file containing the data into memory.
        """

        file_idx = self.indices_file_map[idx]

        if self.current_file_idx != file_idx:
            self.load_file(file_idx)

        idx -= file_idx * self.max_file_size

        return self.current_inputs[idx], self.current_outputs[idx]


if __name__ == "__main__":

    from torch.utils.data import DataLoader

    from FilewiseShuffleSampler import FilewiseShuffleSampler

    inputs_dir = os.path.join(os.path.dirname(__file__), "data", "inputs")
    outputs_dir = os.path.join(os.path.dirname(__file__), "data", "outputs")

    max_file_size = 0
    total_size = 0

    for f in os.listdir(inputs_dir):
        data = np.load(os.path.join(inputs_dir, f))

        print(data.shape)

        if data.shape[0] > max_file_size:
            max_file_size = data.shape[0]

        total_size += data.shape[0]

    file_idx = 0
    indices_file_map = {}
    accumulated_count = 0
    smapler_data_sizes = []

    for f in os.listdir(inputs_dir):
        data = np.load(os.path.join(inputs_dir, f))

        indices_file_map.update(
            {i + accumulated_count: file_idx for i in range(data.shape[0])}
        )

        smapler_data_sizes.append(
            list(range(accumulated_count, accumulated_count + data.shape[0]))
        )

        file_idx += 1
        accumulated_count += data.shape[0]

    print(f"max_file_size: {max_file_size}")
    print(f"total_size: {total_size}")
    print(f"indices_file_map: {indices_file_map}")

    dataset = MediapipeDataset(
        inputs_dir,
        outputs_dir,
        total_size,
        max_file_size,
        indices_file_map,
        device="cpu",
    )

    for i in range(len(dataset)):
        inputs, outputs = dataset[i]
        print(inputs.shape, outputs.shape)

    dataloader = DataLoader(
        dataset,
        batch_size=16,
        sampler=FilewiseShuffleSampler(data_sizes=smapler_data_sizes),
    )

    for inputs, outputs in dataloader:
        print(inputs.shape, outputs.shape)
        # break
