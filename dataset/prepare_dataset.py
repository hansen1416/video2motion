import os
import json

import torch
from torch.utils.data import Dataset, DataLoader
from pathlib import Path

BlazePoseKeypoints = {
    0: "NOSE",
    1: "LEFT_EYE_INNER",
    2: "LEFT_EYE",
    3: "LEFT_EYE_OUTER",
    4: "RIGHT_EYE_INNER",
    5: "RIGHT_EYE",
    6: "RIGHT_EYE_OUTER",
    7: "LEFT_EAR",
    8: "RIGHT_EAR",
    9: "LEFT_RIGHT",
    10: "RIGHT_LEFT",
    11: "LEFT_SHOULDER",
    12: "RIGHT_SHOULDER",
    13: "LEFT_ELBOW",
    14: "RIGHT_ELBOW",
    15: "LEFT_WRIST",
    16: "RIGHT_WRIST",
    17: "LEFT_PINKY",
    18: "RIGHT_PINKY",
    19: "LEFT_INDEX",
    20: "RIGHT_INDEX",
    21: "LEFT_THUMB",
    22: "RIGHT_THUMB",
    23: "LEFT_HIP",
    24: "RIGHT_HIP",
    25: "LEFT_KNEE",
    26: "RIGHT_KNEE",
    27: "LEFT_ANKLE",
    28: "RIGHT_ANKLE",
    29: "LEFT_HEEL",
    30: "RIGHT_HEEL",
    31: "LEFT_FOOT_INDEX",
    32: "RIGHT_FOOT_INDEX",
}


class MediapipeDataset(Dataset):

    def __init__(self, humanoid_name, mediapipe_dir, animation_dir) -> None:
        """
        iterate over mediapipe_dir folder,
        if for a given azimuth/eleveation/n_frame there is mediapipe result

        find the corresponding animation data from animation_dir

        maintain a index -> animation_name/azimuth/elevation/n_frame mapping
        """

        self.data_paths = []

        humanoid_path = os.path.join(mediapipe_dir, humanoid_name)

        for animation_name in os.listdir(humanoid_path):

            animation_name_path = os.path.join(humanoid_path, animation_name)

            for elevation in os.listdir(animation_name_path):

                elevation_path = os.path.join(animation_name_path, elevation)

                for azimuth in os.listdir(elevation_path):

                    azimuth_path = os.path.join(elevation_path, azimuth)

                    for n_frame in os.listdir(azimuth_path):

                        landmark_file = os.path.join(
                            azimuth_path, n_frame, "world_landmarks.json"
                        )

                        if not os.path.isfile(landmark_file):
                            continue

                        # world_landmarks = json.load(landmark_file)

                        # print(landmarks)

                        # print(world_landmarks)

                        self.data_paths.append(
                            (animation_name, azimuth, elevation, n_frame)
                        )

        # display how much memory is used by self.data_paths
        # print(
        #     f"Memory used by self.data_paths: {self.data_paths.__sizeof__() / 1024} KB"
        # )

    def __len__(self):
        return len(self.data_paths)

    def __getitem__(self, idx):
        animation_name, azimuth, elevation, n_frame = self.data_paths[idx]

        landmark_file = os.path.join(
            mediapipe_dir,
            "dors.glb",
            animation_name,
            elevation,
            azimuth,
            n_frame,
            "world_landmarks.json",
        )

        with open(landmark_file, "r") as f:
            landmarks = json.load(f)

        # todo convert landmarks to tensor

        with open(os.path.join(animation_dir, animation_name), "r") as f:
            animation_data = json.load(f)

        # todo get data from n_frame

        return landmarks, animation_data

        # animation_file = os.path.join(animation_dir, f"{animation_name}.json")

        # with open(landmark_file, "r") as f:
        #     landmarks = json.load(f)

        # with open(animation_file, "r") as f:
        #     animation = json.load(f)

        # return {
        #     "landmarks": landmarks,
        #     "animation": animation,
        # }


mediapipe_dir = os.path.join(
    os.path.dirname(__file__),
    "..",
    "mediapipe",
    "results",
)

animation_dir = os.path.join(
    os.path.dirname(__file__), "..", "anim-player", "public", "anim-json-euler"
)

m_dataset = MediapipeDataset("dors.glb", mediapipe_dir, animation_dir)

# get the first item from the dataset
item = m_dataset[0]

print(item)
