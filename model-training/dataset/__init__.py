import os
from .MediapipeDataset import MediapipeDataset

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


__all__ = [DATA_DIR, MediapipeDataset]
