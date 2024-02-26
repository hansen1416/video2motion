import os
import json
import pickle
from dotenv import load_dotenv
from itertools import islice

import numpy as np
import torch
from torch.utils.data import Dataset
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider

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

HUMANOID_BONES_ALL = [
    "Hips",
    "Spine",
    "Spine1",
    "Spine2",
    "Neck",
    "Head",
    "RightShoulder",
    "RightArm",
    "RightForeArm",
    "RightHand",
    "RightHandThumb1",
    "RightHandThumb2",
    "RightHandThumb3",
    "RightHandIndex1",
    "RightHandIndex2",
    "RightHandIndex3",
    "RightHandMiddle1",
    "RightHandMiddle2",
    "RightHandMiddle3",
    "RightHandRing1",
    "RightHandRing2",
    "RightHandRing3",
    "RightHandPinky1",
    "RightHandPinky2",
    "RightHandPinky3",
    "LeftShoulder",
    "LeftArm",
    "LeftForeArm",
    "LeftHand",
    "LeftHandThumb1",
    "LeftHandThumb2",
    "LeftHandThumb3",
    "LeftHandIndex1",
    "LeftHandIndex2",
    "LeftHandIndex3",
    "LeftHandMiddle1",
    "LeftHandMiddle2",
    "LeftHandMiddle3",
    "LeftHandRing1",
    "LeftHandRing2",
    "LeftHandRing3",
    "LeftHandPinky1",
    "LeftHandPinky2",
    "LeftHandPinky3",
    "RightUpLeg",
    "RightLeg",
    "RightFoot",
    "RightToeBase",
    "LeftUpLeg",
    "LeftLeg",
    "LeftFoot",
    "LeftToeBase",
]

HUMANOID_BONES = [
    "Hips",
    "Spine",
    "Spine1",
    "Spine2",
    "Neck",
    "Head",
    "RightShoulder",
    "RightArm",
    "RightForeArm",
    "RightHand",
    "LeftShoulder",
    "LeftArm",
    "LeftForeArm",
    "LeftHand",
    "RightUpLeg",
    "RightLeg",
    "RightFoot",
    "RightToeBase",
    "LeftUpLeg",
    "LeftLeg",
    "LeftFoot",
    "LeftToeBase",
]


def generate_meidiapipe_paths(humanoid_name, mediapipe_dir):

    # get current absolute path

    filename = os.path.join(os.path.dirname(__file__), "mapping", "mediapipe_paths.pkl")

    if os.path.isfile(filename):
        print(f"{filename} already exists")
        return

    data_paths = []

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

                    data_paths.append((animation_name, elevation, azimuth, n_frame))

    with open(filename, "wb") as f:
        pickle.dump(data_paths, f)

    print(f"Saved {filename}")

    return filename


class MediapipeDataset(Dataset):

    def __init__(self, humanoid_name, mediapipe_dir, animation_dir) -> None:
        """
        iterate over mediapipe_dir folder,
        if for a given azimuth/eleveation/n_frame there is mediapipe result

        find the corresponding animation data from animation_dir

        maintain a index -> animation_name/azimuth/elevation/n_frame mapping
        """

        generate_meidiapipe_paths(humanoid_name, mediapipe_dir)

        # with open(os.path.join("mapping", "mediapipe_paths.json"), "r") as f:
        # mediapipe_paths = json.load(f)
        with open(
            os.path.join(os.path.dirname(__file__), "mapping", "mediapipe_paths.pkl"),
            "rb",
        ) as f:
            mediapipe_paths = pickle.load(f)

        self.data_paths = mediapipe_paths
        self.humanoid_name = humanoid_name
        self.mediapipe_dir = mediapipe_dir
        self.animation_dir = animation_dir

        # display how much memory is used by self.data_paths
        # print(
        #     f"Memory used by self.data_paths: {self.data_paths.__sizeof__() / 1024} KB"
        # )

    def __len__(self):
        return len(self.data_paths)

    def __getitem__(self, idx):
        animation_name, elevation, azimuth, n_frame = self.data_paths[idx]

        landmark_file = os.path.join(
            self.mediapipe_dir,
            self.humanoid_name,
            animation_name,
            elevation,
            azimuth,
            n_frame,
            "world_landmarks.json",
        )

        with open(landmark_file, "r") as f:
            landmarks = json.load(f)

        landmarks1d = []
        # flattten landmarks
        for l in landmarks:
            landmarks1d.append(l["x"])
            landmarks1d.append(l["y"])
            landmarks1d.append(l["z"])

        # convert landmarks to tensor
        landmarks1d = torch.tensor(landmarks1d, dtype=torch.float32)

        with open(os.path.join(self.animation_dir, animation_name), "r") as f:
            animation_data = json.load(f)

        bone_rotations = []

        # get data from n_frame
        for bone_name in HUMANOID_BONES:

            try:
                rotation = animation_data[bone_name]["values"][int(n_frame)]
            except IndexError as e:
                # print(
                #     f"IndexError: {animation_name} {bone_name} {n_frame}, real length {len(animation_data[bone_name]['values'])}"
                # )
                # raise e
                rotation = animation_data[bone_name]["values"][
                    len(animation_data[bone_name]["values"]) - 1
                ]

            bone_rotations.append(rotation[0])
            bone_rotations.append(rotation[1])
            bone_rotations.append(rotation[2])

        # convert bone_rotations to tensor
        bone_rotations = torch.tensor(bone_rotations, dtype=torch.float32)

        return landmarks1d, bone_rotations

        # animation_file = os.path.join(animation_dir, f"{animation_name}.json")

        # with open(landmark_file, "r") as f:
        #     landmarks = json.load(f)

        # with open(animation_file, "r") as f:
        #     animation = json.load(f)

        # return {
        #     "landmarks": landmarks,
        #     "animation": animation,
        # }


"""
Memory-Mapped Files:
import mmap

class MyDataset(Dataset):
    def __init__(self, filepath):
        self.file = open(filepath, "rb")
        self.data_mmap = mmap.mmap(self.file.fileno(), 0, access=mmap.ACCESS_READ)

    def __getitem__(self, index):
        # Calculate offset and size based on your data structure
        offset, size = ...
        data = self.data_mmap[offset:offset+size]
        # Process or return data as needed

    def __len__(self):
        # Calculate total data size or number of elements based on file size and structure

# Close the file when done
dataset = MyDataset("large_file.data")
...
dataset.file.close()
"""


"""
Streaming:
class MyDataset(Dataset):
    def __init__(self, filepath):
        self.file = open(filepath, "rb")

    def __getitem__(self, index):
        # Read data in chunks based on your needs
        data = self.file.read(chunk_size)
        # Process or return data as needed

    def __len__(self):
        # Calculate total data size or number of elements based on file size and structure

# No need to close the file explicitly since it's handled by the garbage collector
dataset = MyDataset("large_file.data")
"""

if __name__ == "__main__":

    # mediapipe_dir = os.path.join(
    #     os.path.dirname(__file__),
    #     "..",
    #     "mediapipe",
    #     "results",
    # )

    # animation_dir = os.path.join(
    #     os.path.dirname(__file__),
    #     "..",
    #     "..",
    #     "anim-player",
    #     "public",
    #     "anim-json-euler",
    # )

    # # print(mediapipe_paths)

    # m_dataset = MediapipeDataset("dors.glb", mediapipe_dir, animation_dir)

    # for i in range(len(m_dataset)):
    #     # print(i)
    #     landmarks, rotations = m_dataset[i]
    #     # print(landmarks.shape, rotations.shape)

    # # get the first item from the dataset
    # # landmarks, rotations = m_dataset[0]

    # # print(landmarks.shape, rotations.shape)

    # Load the environment variables from the .env file
    load_dotenv()

    # 使用环境变量中获取的RAM用户的访问密钥配置访问凭证。
    auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())

    # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
    endpoint = "oss-ap-southeast-1.aliyuncs.com"

    # 填写Bucket名称，并设置连接超时时间为30秒。
    bucket = oss2.Bucket(auth, endpoint, "pose-daten", connect_timeout=30)

    # print(bucket)
