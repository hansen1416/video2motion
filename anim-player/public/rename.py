import os
import json

data_dir_mixamo = os.path.join(".", "anim-json-mixamo")
data_dir = os.path.join(".", "anim-json")

filenames = []

# iterate ovedr folder /public/anim-json
for filename in os.listdir(data_dir_mixamo):
    if filename.endswith(".json"):
        filenames.append(filename)

# print(filenames)
# print(len(filenames))

# read json file
for fname in filenames:
    with open(os.path.join(data_dir_mixamo, fname), "r") as f:
        data = json.load(f)

        # remove track with name "Hips.position"
        new_tracks = []

        for track in data["tracks"]:
            # replace "mixamorig" with "" in track["name"]
            track["name"] = track["name"].replace("mixamorig", "")

            if track["name"] == "Hips.position":
                continue

            new_tracks.append(track)

        data["tracks"] = new_tracks

        data["name"] = fname.replace(".json", "")

    # write json file.
    with open(os.path.join(data_dir, fname), "w") as f:
        json.dump(data, f, indent=2)

    # break
