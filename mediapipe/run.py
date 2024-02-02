import json
import os

import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2


def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    # Loop through the detected poses to visualize.
    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

        # Draw the pose landmarks.
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend(
            [
                landmark_pb2.NormalizedLandmark(
                    x=landmark.x, y=landmark.y, z=landmark.z
                )
                for landmark in pose_landmarks
            ]
        )
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style(),
        )
    return annotated_image


def save_pose_visualize_image(annotated_image, image_name="tmp.jpg"):
    bgr_array = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)

    cv2.imwrite(image_name, bgr_array)


def save_mask_image(segmentation_mask):
    visualized_mask = np.repeat(segmentation_mask[:, :, np.newaxis], 3, axis=2) * 255

    cv2.imwrite("tmp_mask.jpg", visualized_mask)


# `models` dir in the current file directory
model_path = os.path.join(
    os.path.dirname(__file__), "models", "pose_landmarker_heavy.task"
)

source_image_dir = os.path.join(
    os.path.dirname(__file__), "../", "video-recorder", "data"
)

queue_dir = os.path.join(os.path.dirname(__file__), "../", "video-recorder", "queue")

charater_names = ["x_bot.fbx"]

results_dor = os.path.join(os.path.dirname(__file__), "results")

# prepare mediapipe settings
BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a pose landmarker instance with the video mode:
options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE,
    output_segmentation_masks=True,
)

with PoseLandmarker.create_from_options(options) as landmarker:

    for char in charater_names:

        for queue_num in [0, 1, 2]:

            queue_file = os.path.join(queue_dir, char, f"queue{queue_num}.json")

            with open(queue_file) as f:
                queue_data = json.load(f)

                for task in queue_data:
                    image_file = os.path.join(
                        source_image_dir, char, *list(map(str, task))
                    )

                    image_file += ".jpg"

                    if os.path.isfile(image_file):
                        print(f"Processing {image_file}")

                        # Load the input image from an image file.
                        mp_image = mp.Image.create_from_file(image_file)

                        # Perform pose landmarking on the provided single image.
                        # The pose landmarker must be created with the image mode.
                        pose_landmarker_result = landmarker.detect(mp_image)

                        pose_landmarks = pose_landmarker_result.pose_landmarks
                        pose_world_landmarks = (
                            pose_landmarker_result.pose_world_landmarks
                        )
                        segmentation_masks = pose_landmarker_result.segmentation_masks

                        # # Convert landmarks to JSON
                        # landmark_data = json.dumps(pose_landmarks, indent=4)

                        # # Save to a JSON file
                        # with open("landmarks.json", "w") as jsonfile:
                        #     jsonfile.write(landmark_data)

                        # world_langmark_data = json.dumps(pose_world_landmarks, indent=4)

                        # # Save to a JSON file
                        # with open("world_landmarks.json", "w") as jsonfile:
                        #     jsonfile.write(landmark_data)

                        for lm in pose_landmarks[0]:
                            print(lm.x, lm.y, lm.z, lm.visibility, lm.presence)

                        print(pose_landmarks)

                        # print(pose_landmarks.landmark)
                        # print(pose_world_landmarks.landmark)
                        # print(segmentation_masks[0])

                        # print(mp_image.numpy_view().shape)

                        # print(mp_image.numpy_view())

                        # STEP 5: Process the detection result. In this case, visualize it.
                        annotated_image = draw_landmarks_on_image(
                            mp_image.numpy_view(), pose_landmarker_result
                        )
                        save_pose_visualize_image(annotated_image)

                        segmentation_mask = segmentation_masks[0].numpy_view()
                        save_mask_image(segmentation_mask)

                    break

            break
