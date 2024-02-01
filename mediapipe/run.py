import json
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

queue_dir = os.path.join(os.path.dirname(__file__), "../", "video-recorder", "queue")

for file in os.listdir(queue_dir):
    # print(f"Processing {files}")

    with open(os.path.join(queue_dir, file)) as f:
        data = json.load(f)

        for q in data:
            image_file = os.path.join(source_image_dir, *list(map(str, q)))

            if os.path.isfile(image_file + ".png"):
                print(f"Processing {image_file}")

    break


exit()

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
