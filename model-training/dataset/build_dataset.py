from time import sleep
import time
import os
import json

import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from tqdm import tqdm
import numpy as np
from multiprocessing import Process
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

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


def get_landmarks1d(landmarks):
    """
    Convert landmarks to 1d tensor, drop visibility and presence

    Args:
        landmarks: list of dict
    Returns:
        landmarks1d: ndarray
    """
    landmarks1d = []
    # flattten landmarks
    for l in landmarks:
        landmarks1d.append(l["x"])
        landmarks1d.append(l["y"])
        landmarks1d.append(l["z"])

    # convert landmarks to tensor
    landmarks1d = np.array(landmarks1d, dtype=np.float32)

    return landmarks1d


def extract_anim_euler_frames(anim_euler_data, n_frame):
    """
    Read the bone rotation animation data at the n_frame

    Args:
        anim_euler_data: dict
        n_frame: int
    Returns:
        bone_rotations: ndarray
    """
    bone_rotations = []

    # get data from n_frame
    for bone_name in HUMANOID_BONES:

        try:
            rotation = anim_euler_data[bone_name]["values"][int(n_frame)]
        except IndexError as e:
            # print(
            #     f"IndexError: {animation_name} {bone_name} {n_frame}, real length {len(animation_data[bone_name]['values'])}"
            # )
            # raise e
            rotation = anim_euler_data[bone_name]["values"][
                len(anim_euler_data[bone_name]["values"]) - 1
            ]

        bone_rotations.append(rotation[0])
        bone_rotations.append(rotation[1])
        bone_rotations.append(rotation[2])

    # convert bone_rotations to tensor
    bone_rotations = np.array(bone_rotations, dtype=np.float32)

    return bone_rotations.reshape(-1, 3)


# custom process class
class CustomProcess(Process):

    # override the constructor
    def __init__(self, queue_file_path, mediapipe_path, anim_euler_path):
        # execute the base constructor
        Process.__init__(self)

        # An instance of the multiprocessing.Value can be defined in the constructor of a custom class as a shared instance variable.
        # The constructor of the multiprocessing.Value class requires that we specify the data type and an initial value.
        # We can define an instance attribute as an instance of the multiprocessing.Value
        # which will automatically and correctly be shared between processes.
        # initialize integer attribute
        # self.data = Value("i", 0)
        auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())

        endpoint = "oss-ap-southeast-1.aliyuncs.com"

        # oss bucket, timeout 30s
        self.bucket = oss2.Bucket(auth, endpoint, "pose-daten", connect_timeout=30)

        self.queue_file_path = queue_file_path
        self.mediapipe_path = mediapipe_path
        self.anim_euler_path = anim_euler_path

    # override the run function
    def run(self):

        with open(self.queue_file_path, "r") as f:
            queue_data = json.load(f)

        queue_num = int(
            os.path.basename(self.queue_file_path)
            .replace(".json", "")
            .replace("queue", "")
        )

        # for testing, only get 100
        queue_data = queue_data[:1000]

        features = []
        targets = []

        for i, (animation_name, elevation, azimuth, n_frame) in enumerate(queue_data):

            try:
                landmarks_obj = self.bucket.get_object(
                    f"{self.mediapipe_path}{animation_name}/{elevation}/{azimuth}/{n_frame}/world_landmarks.json"
                )
            except oss2.exceptions.NoSuchKey:
                print(
                    f"oss2.exceptions.NoSuchKey: {self.mediapipe_path}{animation_name}/{elevation}/{azimuth}/{n_frame}/world_landmarks.json"
                )
                continue

            try:
                anim_euler_obj = self.bucket.get_object(
                    f"{self.anim_euler_path}{animation_name}"
                )
            except oss2.exceptions.NoSuchKey:
                print(
                    f"oss2.exceptions.NoSuchKey: {self.anim_euler_path}{animation_name}"
                )
                continue

            world_landmarks = json.loads(landmarks_obj.read())

            landmarks1d = get_landmarks1d(world_landmarks)

            features.append(landmarks1d)

            # print(landmarks1d)

            anim_euler = json.loads(anim_euler_obj.read())

            bone_rotations = extract_anim_euler_frames(anim_euler, n_frame)

            targets.append(bone_rotations)

            # print(bone_rotations)

            if i % 100 == 0:
                print(f"queue {queue_num} progress {i}/{len(queue_data)}")

        features = np.array(features)
        targets = np.array(targets)

        if not os.path.exists(
            os.path.join(os.path.dirname(__file__), "data", "inputs")
        ):
            os.makedirs(os.path.join(os.path.dirname(__file__), "data", "inputs"))

        if not os.path.exists(
            os.path.join(os.path.dirname(__file__), "data", "outputs")
        ):
            os.makedirs(os.path.join(os.path.dirname(__file__), "data", "outputs"))

        # save features and targets to npy file
        np.save(
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "inputs",
                f"inputs_{queue_num}.npy",
            ),
            features,
        )

        np.save(
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "outputs",
                f"outputs_{queue_num}.npy",
            ),
            targets,
        )


if __name__ == "__main__":

    queue_nums = [0, 1, 2, 3, 4, 5, 6, 7]

    # Number of processes to use

    queue_dir = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "queues",
    )

    humanoid_name = "dors.glb"
    mediapipe_path = f"mediapipe/{humanoid_name}/"
    anim_euler_path = f"anim-json-euler/"

    processes = [
        CustomProcess(
            queue_file_path=os.path.join(queue_dir, f"queue{i}.json"),
            mediapipe_path=mediapipe_path,
            anim_euler_path=anim_euler_path,
        )
        for i in queue_nums
    ]

    start_time = time.time()

    # run the process,
    for process in processes:
        process.start()

    for process in processes:
        # report the daemon attribute
        print(
            process.daemon,
            process.name,
            process.pid,
            process.exitcode,
            process.is_alive(),
        )

        process.join()

    end_time = time.time()

    print(f"Time taken: {end_time - start_time}")
