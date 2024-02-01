import os

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# `models` dir in the current file directory
model_path = os.path.join(
    os.path.dirname(__file__), "models", "pose_landmarker_heavy.task"
)


source_image_dir = os.path.join(
    os.path.dirname(__file__), "../", "video-recorder", "data"
)


def traver_folder_recursivly(folder):
    for root, dirs, files in os.walk(folder):
        for dir in dirs:
            traver_folder_recursivly(dir)

        for file in files:
            yield os.path.join(root, file)


# get all the files in the folder
all_files = traver_folder_recursivly(source_image_dir)

print(list(all_files))


BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a pose landmarker instance with the video mode:
options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,
)

with PoseLandmarker.create_from_options(options) as landmarker:
    # The landmarker is initialized. Use it here.
    # ...
    # iterate over `source_image_dir` recursively
    for root, dirs, files in os.walk(source_image_dir):
        print(f"Processing {root}, {dirs}, {files}")

        for file in files:
            # get the file path
            file_path = os.path.join(root, file)

            if os.path.isfile(file_path):
                # process the image
                print(f"Processing {file_path}")
            else:
                print(f"Skipping {file_path}")

        break
